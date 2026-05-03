import type { CityRecommendationRequest, CityRecommendationResponse } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function getCityRecommendation(
  request: CityRecommendationRequest,
): Promise<CityRecommendationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/recommendations/city`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Recommendations API request failed: ${response.status}`);
  }

  return response.json() as Promise<CityRecommendationResponse>;
}
