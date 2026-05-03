"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import type { CityContentTypeFilter, CityRecommendations, CityWork } from "./types";

type CityPageProps = {
  recommendations: CityRecommendations;
};

const DEFAULT_FILTERS: CityContentTypeFilter[] = [
  { value: "all", label: "全部" },
  { value: "book", label: "书籍" },
  { value: "film", label: "电影" },
];

const CONTENT_TYPE_LABEL: Record<CityWork["contentType"], string> = {
  book: "书籍",
  film: "电影",
};

export function CityPage({ recommendations }: CityPageProps) {
  const { city, featuredWork, places, works } = recommendations;
  const filters = recommendations.contentTypes.length > 0 ? recommendations.contentTypes : DEFAULT_FILTERS;
  const [activeType, setActiveType] = useState<CityContentTypeFilter["value"]>("all");

  const filteredWorks = useMemo(() => {
    if (activeType === "all") {
      return works;
    }

    return works.filter((work) => work.contentType === activeType);
  }, [activeType, works]);

  return (
    <main className="min-h-dvh bg-[#f7f5f0] pb-20 text-neutral-950">
      <section className="mx-auto flex w-full max-w-md flex-col gap-7 px-5 pb-8 pt-6">
        <Link className="text-sm text-neutral-500" href="/">
          返回首页
        </Link>

        <header className="space-y-3">
          <p className="text-sm text-neutral-500">{city.countryRegion}</p>
          <h1 className="text-4xl font-semibold tracking-normal">{city.nameZh}</h1>
          {(city.intro ?? city.toneSummary) && (
            <p className="text-base leading-7 text-neutral-700">{city.intro ?? city.toneSummary}</p>
          )}
        </header>

        <section className="space-y-3">
          <div className="flex rounded-2xl border border-neutral-200 bg-white p-1">
            {filters.map((filter) => {
              const isActive = filter.value === activeType;

              return (
                <button
                  className={`min-h-11 flex-1 rounded-xl px-3 text-sm font-medium transition ${
                    isActive ? "bg-neutral-950 text-white" : "text-neutral-600"
                  }`}
                  key={filter.value}
                  onClick={() => setActiveType(filter.value)}
                  type="button"
                >
                  {filter.label}
                </button>
              );
            })}
          </div>
        </section>

        {featuredWork && (
          <section className="space-y-3">
            <h2 className="text-base font-semibold">推荐作品</h2>
            <WorkCard work={featuredWork} variant="featured" />
          </section>
        )}

        <section className="space-y-3">
          <div className="flex items-end justify-between gap-4">
            <h2 className="text-base font-semibold">更多作品</h2>
            <span className="text-xs text-neutral-500">{filteredWorks.length} 个推荐</span>
          </div>
          <div className="grid gap-3">
            {filteredWorks.map((work) => (
              <WorkCard key={work.id} work={work} />
            ))}
            {filteredWorks.length === 0 && (
              <p className="rounded-2xl border border-neutral-200 bg-white p-4 text-sm text-neutral-500">
                当前类型还没有推荐作品。
              </p>
            )}
          </div>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-semibold">关联地点</h2>
          <div className="grid gap-3">
            {places.map((place) => (
              <PlaceCard key={place.id} place={place} />
            ))}
          </div>
        </section>
      </section>

      <nav className="fixed inset-x-0 bottom-0 border-t border-neutral-200 bg-[#f7f5f0]/95 px-5 py-3 backdrop-blur">
        <div className="mx-auto grid max-w-md grid-cols-3 text-center text-sm text-neutral-600">
          <Link className="font-medium text-neutral-950" href="/">
            探索
          </Link>
          <Link href="/collections">收藏</Link>
          <span>我的</span>
        </div>
      </nav>
    </main>
  );
}

function PlaceCard({ place }: { place: CityRecommendations["places"][number] }) {
  const content = (
    <article className="rounded-2xl border border-neutral-200 bg-white p-4 transition hover:border-neutral-300">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-semibold">{place.nameZh}</h3>
          {place.nameOriginal && <p className="mt-1 text-sm text-neutral-500">{place.nameOriginal}</p>}
        </div>
        {place.area && (
          <span className="shrink-0 rounded-full bg-neutral-100 px-3 py-1 text-xs text-neutral-600">
            {place.area}
          </span>
        )}
      </div>
      {place.summary && <p className="mt-3 text-sm leading-6 text-neutral-600">{place.summary}</p>}
    </article>
  );

  if (!place.slug) {
    return content;
  }

  return <Link href={`/places/${place.slug}`}>{content}</Link>;
}

function WorkCard({ work, variant = "default" }: { work: CityWork; variant?: "default" | "featured" }) {
  const content = (
    <article
      className={`rounded-2xl border border-neutral-200 bg-white p-4 ${
        variant === "featured" ? "shadow-sm" : ""
      }`}
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-medium text-neutral-500">{CONTENT_TYPE_LABEL[work.contentType]}</p>
          <h3 className="mt-1 text-lg font-semibold">{work.titleZh}</h3>
          {work.titleOriginal && <p className="mt-1 text-sm text-neutral-500">{work.titleOriginal}</p>}
        </div>
        {work.year && (
          <span className="shrink-0 rounded-full bg-neutral-100 px-3 py-1 text-xs text-neutral-600">
            {work.year}
          </span>
        )}
      </div>
      {work.creator && <p className="mt-3 text-sm text-neutral-600">{work.creator}</p>}
      {(work.recommendationReason ?? work.summary) && (
        <p className="mt-3 text-sm leading-6 text-neutral-600">
          {work.recommendationReason ?? work.summary}
        </p>
      )}
    </article>
  );

  if (!work.slug) {
    return content;
  }

  return <Link href={`/works/${work.slug}`}>{content}</Link>;
}
