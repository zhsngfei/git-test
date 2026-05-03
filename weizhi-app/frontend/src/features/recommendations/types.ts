export type RecommendationStatus = "cached" | "generated" | "fallback";

export type CityRecommendationRequest = {
  citySlug: string;
  contentType?: "all" | "book" | "film";
};

export type RecommendationGroup = {
  title: string;
  workSlugs: string[];
  placeSlugs: string[];
};

export type CityRecommendationResponse = {
  citySlug: string;
  status: RecommendationStatus;
  message: string;
  groups: RecommendationGroup[];
};
