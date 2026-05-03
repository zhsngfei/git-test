export type CityContentType = "book" | "film";

export type CityContentTypeFilter = {
  value: "all" | CityContentType;
  label: string;
};

export type CityDetail = {
  slug: string;
  nameZh: string;
  countryRegion: string;
  intro?: string | null;
  toneSummary?: string | null;
};

export type CityPlace = {
  id: string;
  slug?: string | null;
  nameZh: string;
  nameOriginal?: string | null;
  area?: string | null;
  summary?: string | null;
  relatedWorkIds?: string[];
};

export type CityWork = {
  id: string;
  slug?: string | null;
  titleZh: string;
  titleOriginal?: string | null;
  creator?: string | null;
  year?: string | number | null;
  contentType: CityContentType;
  summary?: string | null;
  recommendationReason?: string | null;
  relatedPlaceIds?: string[];
};

export type CityRecommendations = {
  city: CityDetail;
  contentTypes: CityContentTypeFilter[];
  featuredWork: CityWork | null;
  works: CityWork[];
  places: CityPlace[];
};
