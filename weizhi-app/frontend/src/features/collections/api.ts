import type {
  CollectionEntityType,
  CollectionItem,
  CollectionList,
  CollectionRequest,
  PreparationBook,
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

function userHeaders(userId: string) {
  return {
    "Content-Type": "application/json",
    "X-Weizhi-User-Id": userId,
  };
}

async function parseCollectionResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`Collections API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function getCollections(userId: string): Promise<CollectionList> {
  const response = await fetch(`${API_BASE_URL}/api/collections`, {
    headers: userHeaders(userId),
    cache: "no-store",
  });

  return parseCollectionResponse<CollectionList>(response);
}

export async function getPreparationBook(userId: string): Promise<PreparationBook> {
  const response = await fetch(`${API_BASE_URL}/api/collections/preparation`, {
    headers: userHeaders(userId),
    cache: "no-store",
  });

  return parseCollectionResponse<PreparationBook>(response);
}

export async function addCollection(
  userId: string,
  collection: CollectionRequest,
): Promise<CollectionItem> {
  const response = await fetch(`${API_BASE_URL}/api/collections`, {
    method: "POST",
    headers: userHeaders(userId),
    body: JSON.stringify(collection),
  });

  return parseCollectionResponse<CollectionItem>(response);
}

export async function removeCollection(
  userId: string,
  entityType: CollectionEntityType,
  entityId: string,
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/collections/${entityType}/${entityId}`, {
    method: "DELETE",
    headers: userHeaders(userId),
  });

  if (!response.ok) {
    throw new Error(`Collections API request failed: ${response.status}`);
  }
}
