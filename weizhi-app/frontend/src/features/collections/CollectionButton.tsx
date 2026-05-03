"use client";

import { useMemo, useState } from "react";
import { AuthDialog, type SimulatedUser } from "@/features/auth/AuthDialog";
import { readLocalUser, writeLocalUser } from "@/features/auth/localSession";
import { addCollection, removeCollection } from "./api";
import type { CollectionEntityType } from "./types";

type CollectionButtonProps = {
  citySlug: string;
  entityId: string;
  entityType: CollectionEntityType;
};

type PendingAction = "collect" | null;

export function CollectionButton({ citySlug, entityId, entityType }: CollectionButtonProps) {
  const collectionKey = useMemo(
    () => `weizhi.collection.${citySlug}.${entityType}.${entityId}`,
    [citySlug, entityId, entityType],
  );

  const [currentUser, setCurrentUser] = useState<SimulatedUser | null>(() => readLocalUser());
  const [isCollected, setIsCollected] = useState(() => readLocalCollection(collectionKey));
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const [pendingAction, setPendingAction] = useState<PendingAction>(null);

  async function collect(user: SimulatedUser) {
    setIsSaving(true);
    setStatus(null);
    try {
      await addCollection(user.userId, { citySlug, entityId, entityType });
      collectLocally();
    } catch {
      setStatus("收藏暂时没有同步成功，请稍后再试。");
    } finally {
      setIsSaving(false);
    }
  }

  async function remove(user: SimulatedUser) {
    setIsSaving(true);
    setStatus(null);
    try {
      await removeCollection(user.userId, entityType, entityId);
      removeLocally();
    } catch {
      setStatus("取消收藏暂时没有同步成功，请稍后再试。");
    } finally {
      setIsSaving(false);
    }
  }

  function collectLocally() {
    window.localStorage.setItem(collectionKey, "true");
    setIsCollected(true);
  }

  function removeLocally() {
    window.localStorage.removeItem(collectionKey);
    setIsCollected(false);
  }

  async function handleClick() {
    if (isCollected) {
      if (currentUser) {
        await remove(currentUser);
      } else {
        removeLocally();
      }
      return;
    }

    if (!currentUser) {
      setPendingAction("collect");
      setIsAuthOpen(true);
      return;
    }

    await collect(currentUser);
  }

  async function handleAuthenticated(user: SimulatedUser) {
    writeLocalUser(user);
    setCurrentUser(user);

    if (pendingAction === "collect") {
      await collect(user);
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

function readLocalCollection(collectionKey: string) {
  if (typeof window === "undefined") {
    return false;
  }

  return window.localStorage.getItem(collectionKey) === "true";
}
