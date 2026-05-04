import type {
  CollectionEntityType,
  CollectionItem,
  CollectionList,
  CollectionRequest,
  PreparationBook,
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

function authHeaders(accessToken: string) {
  return {
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  };
}

async function parseCollectionResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`Collections API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function getCollections(accessToken: string): Promise<CollectionList> {
  const response = await fetch(`${API_BASE_URL}/api/collections`, {
    headers: authHeaders(accessToken),
    cache: "no-store",
  });

  return parseCollectionResponse<CollectionList>(response);
}

export async function getPreparationBook(accessToken: string): Promise<PreparationBook> {
  const response = await fetch(`${API_BASE_URL}/api/collections/preparation`, {
    headers: authHeaders(accessToken),
    cache: "no-store",
  });

  return parseCollectionResponse<PreparationBook>(response);
}

export async function addCollection(
  accessToken: string,
  collection: CollectionRequest,
): Promise<CollectionItem> {
  const response = await fetch(`${API_BASE_URL}/api/collections`, {
    method: "POST",
    headers: authHeaders(accessToken),
    body: JSON.stringify(collection),
  });

  return parseCollectionResponse<CollectionItem>(response);
}

export async function removeCollection(
  accessToken: string,
  entityType: CollectionEntityType,
  entityId: string,
): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/collections/${entityType}/${entityId}`, {
    method: "DELETE",
    headers: authHeaders(accessToken),
  });

  if (!response.ok) {
    throw new Error(`Collections API request failed: ${response.status}`);
  }
}
