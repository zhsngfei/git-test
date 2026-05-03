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
