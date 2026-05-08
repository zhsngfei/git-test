"use client";

import type { Session } from "@supabase/supabase-js";
import { getStoredDevSession } from "./devAuth";
import { isSupabaseConfigured, supabase } from "./supabaseClient";

export type AuthSession = {
  accessToken: string;
  user: {
    id: string;
    email?: string | null;
  };
};

export async function getAuthSession(): Promise<AuthSession | null> {
  if (!isSupabaseConfigured) {
    return getStoredDevSession();
  }

  const { data, error } = await supabase.auth.getSession();

  if (error) {
    throw error;
  }

  return toAuthSession(data.session);
}

export function toAuthSession(session: Session | null): AuthSession | null {
  if (!session) {
    return null;
  }

  return {
    accessToken: session.access_token,
    user: session.user,
  };
}
