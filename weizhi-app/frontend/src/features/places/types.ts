export type PlaceWorkContentType = "book" | "film" | "series";

export type PlaceDetail = {
  id: string;
  slug: string;
  nameZh: string;
  nameOriginal?: string | null;
  area?: string | null;
  summary?: string | null;
};

export type PlaceCity = {
  slug: string;
  nameZh: string;
  countryRegion?: string | null;
};

export type RelatedWork = {
  id: string;
  slug?: string | null;
  titleZh: string;
  titleOriginal?: string | null;
  creator?: string | null;
  year?: string | number | null;
  contentType: PlaceWorkContentType;
  summary?: string | null;
  recommendationReason?: string | null;
};

export type PlaceDetailResponse = {
  place: PlaceDetail;
  city: PlaceCity;
  meaning?: string | null;
  relatedWorks: RelatedWork[];
};
