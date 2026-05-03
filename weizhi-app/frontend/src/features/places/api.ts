import { apiGet } from "@/lib/api/client";
import type { PlaceDetailResponse } from "./types";

export function getPlaceDetail(slug: string): Promise<PlaceDetailResponse> {
  return apiGet<PlaceDetailResponse>(`/api/places/${slug}`);
}
