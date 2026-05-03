"use client";

import { useEffect, useState } from "react";
import { getCityRecommendation } from "./api";
import type { CityRecommendationResponse } from "./types";

type RecommendationStatusProps = {
  citySlug: string;
};

const STATUS_LABEL: Record<CityRecommendationResponse["status"], string> = {
  cached: "已缓存",
  generated: "已生成",
  fallback: "回退推荐",
};

export function RecommendationStatus({ citySlug }: RecommendationStatusProps) {
  const [recommendation, setRecommendation] = useState<CityRecommendationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const timeoutId = window.setTimeout(() => {
      setIsLoading(true);
      setError(null);
      getCityRecommendation({ citySlug })
        .then(setRecommendation)
        .catch(() => setError("推荐状态暂时不可用，已展示默认内容。"))
        .finally(() => setIsLoading(false));
    }, 0);

    return () => window.clearTimeout(timeoutId);
  }, [citySlug]);

  if (isLoading && !recommendation) {
    return (
      <section className="rounded-2xl border border-neutral-200 bg-white p-4 text-sm text-neutral-600">
        正在整理推荐状态...
      </section>
    );
  }

  if (error) {
    return (
      <section className="rounded-2xl border border-neutral-200 bg-white p-4 text-sm text-neutral-600">
        {error}
      </section>
    );
  }

  if (!recommendation) {
    return null;
  }

  return (
    <section className="space-y-3 rounded-2xl border border-neutral-200 bg-white p-4">
      <div className="flex items-center justify-between gap-4">
        <h2 className="text-base font-semibold">推荐状态</h2>
        <span className="rounded-full bg-neutral-100 px-3 py-1 text-xs text-neutral-600">
          {STATUS_LABEL[recommendation.status]}
        </span>
      </div>
      <p className="text-sm leading-6 text-neutral-600">{recommendation.message}</p>
      {recommendation.groups.length > 0 && (
        <div className="grid gap-2">
          {recommendation.groups.map((group) => (
            <div className="rounded-xl bg-neutral-50 p-3" key={group.title}>
              <h3 className="text-sm font-medium">{group.title}</h3>
              <p className="mt-1 text-xs leading-5 text-neutral-500">
                作品 {group.workSlugs.length} · 地点 {group.placeSlugs.length}
              </p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
