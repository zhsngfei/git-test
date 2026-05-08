"use client";

import type { AuthSession } from "./session";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
const STORAGE_KEY = "weizhi.devAuthSession";

type DevSessionResponse = {
  accessToken: string;
  user: {
    id: string;
    email: string;
  };
};

export function getStoredDevSession(): AuthSession | null {
  if (typeof window === "undefined") {
    return null;
  }

  const rawSession = window.localStorage.getItem(STORAGE_KEY);
  if (!rawSession) {
    return null;
  }

  try {
    return JSON.parse(rawSession) as AuthSession;
  } catch {
    window.localStorage.removeItem(STORAGE_KEY);
    return null;
  }
}

export async function createDevSession(email: string): Promise<AuthSession> {
  const response = await fetch(`${API_BASE_URL}/api/dev/auth/session`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });

  if (!response.ok) {
    throw new Error(`Dev auth request failed: ${response.status}`);
  }

  const session = (await response.json()) as DevSessionResponse;
  const authSession: AuthSession = {
    accessToken: session.accessToken,
    user: session.user,
  };

  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(authSession));
  return authSession;
}
