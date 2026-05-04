"use client";

import type { Session, User } from "@supabase/supabase-js";
import { supabase } from "./supabaseClient";

export type AuthSession = {
  accessToken: string;
  user: User;
};

export async function getAuthSession(): Promise<AuthSession | null> {
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
