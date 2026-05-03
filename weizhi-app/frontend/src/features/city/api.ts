import { apiGet } from "@/lib/api/client";
import type { CityRecommendations } from "./types";

export function getCityRecommendations(slug: string): Promise<CityRecommendations> {
  return apiGet<CityRecommendations>(`/api/cities/${slug}/recommendations`);
}
