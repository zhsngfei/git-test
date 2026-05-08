"use client";

import { useCallback, useEffect, useState } from "react";
import { AuthDialog } from "@/features/auth/AuthDialog";
import { getAuthSession, type AuthSession } from "@/features/auth/session";
import { isSupabaseConfigured, supabase } from "@/features/auth/supabaseClient";
import { addCollection, getCollections, removeCollection } from "./api";
import type { CollectionEntityType } from "./types";

type CollectionButtonProps = {
  citySlug: string;
  entityId: string;
  entityType: CollectionEntityType;
};

type PendingAction = "collect" | null;

export function CollectionButton({ citySlug, entityId, entityType }: CollectionButtonProps) {
  const [authSession, setAuthSession] = useState<AuthSession | null>(null);
  const [isCollected, setIsCollected] = useState(false);
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [pendingAction, setPendingAction] = useState<PendingAction>(null);

  const syncCollectedState = useCallback(
    async (accessToken: string) => {
      try {
        const collections = await getCollections(accessToken);
        setIsCollected(
          collections.items.some(
            (item) =>
              item.entityType === entityType &&
              item.entityId === entityId &&
              item.citySlug === citySlug,
          ),
        );
      } catch {
        setStatus("收藏状态暂时无法同步。");
      }
    },
    [citySlug, entityId, entityType],
  );

  useEffect(() => {
    let isMounted = true;

    void getAuthSession()
      .then((session) => {
        if (isMounted) {
          setAuthSession(session);
          if (session) {
            void syncCollectedState(session.accessToken);
          }
        }
      })
      .catch(() => {
        if (isMounted) {
          setStatus("登录状态暂时无法读取。");
        }
      });

    if (!isSupabaseConfigured) {
      return () => {
        isMounted = false;
      };
    }

    const { data } = supabase.auth.onAuthStateChange((_event, session) => {
      if (!isMounted) {
        return;
      }

      const nextSession = session
        ? {
            accessToken: session.access_token,
            user: session.user,
          }
        : null;
      setAuthSession(nextSession);
      if (nextSession) {
        void syncCollectedState(nextSession.accessToken);
      } else {
        setIsCollected(false);
      }
    });

    return () => {
      isMounted = false;
      data.subscription.unsubscribe();
    };
  }, [syncCollectedState]);

  async function collect(session: AuthSession) {
    setIsSaving(true);
    setStatus(null);
    try {
      await addCollection(session.accessToken, { citySlug, entityId, entityType });
      setIsCollected(true);
    } catch {
      setStatus("收藏暂时没有同步成功，请稍后再试。");
    } finally {
      setIsSaving(false);
    }
  }

  async function remove(session: AuthSession) {
    setIsSaving(true);
    setStatus(null);
    try {
      await removeCollection(session.accessToken, entityType, entityId);
      setIsCollected(false);
    } catch {
      setStatus("取消收藏暂时没有同步成功，请稍后再试。");
    } finally {
      setIsSaving(false);
    }
  }

  async function handleClick() {
    if (isCollected) {
      if (authSession) {
        await remove(authSession);
      } else {
        setIsCollected(false);
      }
      return;
    }

    if (!authSession) {
      setPendingAction("collect");
      setIsAuthOpen(true);
      return;
    }

    await collect(authSession);
  }

  async function handleAuthenticated() {
    const nextSession = await getAuthSession();
    setAuthSession(nextSession);

    if (pendingAction === "collect" && nextSession) {
      await collect(nextSession);
      setPendingAction(null);
    }

    setIsAuthOpen(false);
  }

  return (
    <>
      <button
        aria-pressed={isCollected}
        disabled={isSaving}
        className={
          isCollected
            ? "min-h-12 w-full rounded-xl border border-neutral-950 bg-white px-4 text-sm font-medium text-neutral-950"
            : "min-h-12 w-full rounded-xl bg-neutral-950 px-4 text-sm font-medium text-white"
        }
        onClick={handleClick}
        type="button"
      >
        {isSaving ? "保存中" : isCollected ? "已收藏" : "收藏"}
      </button>
      {status && <p className="mt-2 text-sm leading-6 text-neutral-600">{status}</p>}
      <AuthDialog
        isOpen={isAuthOpen}
        onAuthenticated={handleAuthenticated}
        onClose={() => setIsAuthOpen(false)}
      />
    </>
  );
}
