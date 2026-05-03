import { apiGet } from "@/lib/api/client";
import type { WorkDetailResponse } from "./types";

export function getWorkDetail(slug: string): Promise<WorkDetailResponse> {
  return apiGet<WorkDetailResponse>(`/api/works/${slug}`);
}
