"use client";

import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "https://example.supabase.co";
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ?? "replace-with-supabase-anon-key";

export const isSupabaseConfigured =
  supabaseUrl !== "https://example.supabase.co" &&
  supabaseAnonKey !== "replace-with-supabase-anon-key";

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
