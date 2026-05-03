"use client";

import { useMemo, useState } from "react";
import { AuthDialog, type SimulatedUser } from "@/features/auth/AuthDialog";
import { readLocalUser, writeLocalUser } from "@/features/auth/localSession";
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
  const [pendingAction, setPendingAction] = useState<PendingAction>(null);

  function collectLocally() {
    window.localStorage.setItem(collectionKey, "true");
    setIsCollected(true);
  }

  function removeLocally() {
    window.localStorage.removeItem(collectionKey);
    setIsCollected(false);
  }

  function handleClick() {
    if (isCollected) {
      removeLocally();
      return;
    }

    if (!currentUser) {
      setPendingAction("collect");
      setIsAuthOpen(true);
      return;
    }

    collectLocally();
  }

  function handleAuthenticated(user: SimulatedUser) {
    writeLocalUser(user);
    setCurrentUser(user);

    if (pendingAction === "collect") {
      collectLocally();
      setPendingAction(null);
    }

    setIsAuthOpen(false);
  }

  return (
    <>
      <button
        aria-pressed={isCollected}
        className={
          isCollected
            ? "min-h-12 w-full rounded-xl border border-neutral-950 bg-white px-4 text-sm font-medium text-neutral-950"
            : "min-h-12 w-full rounded-xl bg-neutral-950 px-4 text-sm font-medium text-white"
        }
        onClick={handleClick}
        type="button"
      >
        {isCollected ? "已收藏" : "收藏"}
      </button>
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
