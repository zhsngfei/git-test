import { apiGet } from "@/lib/api/client";
import type { CitySummary } from "./types";

export function getSupportedCities(): Promise<CitySummary[]> {
  return apiGet<CitySummary[]>("/api/cities");
}
