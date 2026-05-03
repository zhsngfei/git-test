export type WorkContentType = "book" | "film" | "series";

export type WorkDetail = {
  id: string;
  slug: string;
  titleZh: string;
  titleOriginal?: string | null;
  creator?: string | null;
  year?: string | number | null;
  contentType: WorkContentType;
  summary?: string | null;
};

export type WorkCity = {
  slug: string;
  nameZh: string;
  countryRegion?: string | null;
};

export type RelatedPlace = {
  id: string;
  slug?: string | null;
  nameZh: string;
  nameOriginal?: string | null;
  area?: string | null;
  summary?: string | null;
};

export type WorkDetailResponse = {
  work: WorkDetail;
  city: WorkCity;
  recommendationReason?: string | null;
  cityConnection?: string | null;
  relatedPlaces: RelatedPlace[];
};
