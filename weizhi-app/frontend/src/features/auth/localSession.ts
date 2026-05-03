"use client";

import type { SimulatedUser } from "./AuthDialog";

const SESSION_STORAGE_KEY = "weizhi.localUser";

export function readLocalUser(): SimulatedUser | null {
  if (typeof window === "undefined") {
    return null;
  }

  const rawValue = window.localStorage.getItem(SESSION_STORAGE_KEY);
  if (!rawValue) {
    return null;
  }

  try {
    return JSON.parse(rawValue) as SimulatedUser;
  } catch {
    window.localStorage.removeItem(SESSION_STORAGE_KEY);
    return null;
  }
}

export function writeLocalUser(user: SimulatedUser) {
  window.localStorage.setItem(SESSION_STORAGE_KEY, JSON.stringify(user));
}
