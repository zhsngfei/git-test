export type CollectionEntityType = "work" | "place";

export type CollectionRequest = {
  entityType: CollectionEntityType;
  entityId: string;
  citySlug: string;
};

export type CollectionItem = CollectionRequest & {
  collectedAt?: string;
};

export type CollectionList = {
  items: CollectionItem[];
};

export type PreparationContentType = "book" | "film" | "series";

export type PreparationCity = {
  slug: string;
  nameZh: string;
  countryRegion?: string | null;
};

export type PreparationWork = {
  id: string;
  slug: string;
  titleZh: string;
  contentType: PreparationContentType;
  summary?: string | null;
};

export type PreparationPlace = {
  id: string;
  slug: string;
  nameZh: string;
  summary?: string | null;
};

export type PreparationCityGroup = {
  city: PreparationCity;
  works: PreparationWork[];
  places: PreparationPlace[];
};

export type PreparationBook = {
  cities: PreparationCityGroup[];
};
