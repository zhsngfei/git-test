export type CitySummary = {
  slug: string;
  nameZh: string;
  countryRegion: string;
  isSupported: boolean;
  contentDepth: "core" | "expansion" | "unsupported";
  toneSummary: string;
};
