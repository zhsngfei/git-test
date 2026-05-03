import Link from "next/link";
import type { ReactNode } from "react";
import { CollectionButton } from "@/features/collections/CollectionButton";
import type { RelatedPlace, WorkDetailResponse } from "./types";

type WorkDetailPageProps = {
  detail: WorkDetailResponse;
};

const CONTENT_TYPE_LABEL: Record<WorkDetailResponse["work"]["contentType"], string> = {
  book: "书籍",
  film: "电影",
  series: "剧集",
};

export function WorkDetailPage({ detail }: WorkDetailPageProps) {
  const { city, cityConnection, recommendationReason, relatedPlaces, work } = detail;

  return (
    <main className="min-h-dvh bg-[#f7f5f0] pb-20 text-neutral-950">
      <section className="mx-auto flex w-full max-w-md flex-col gap-7 px-5 pb-8 pt-6">
        <Link className="text-sm text-neutral-500" href={`/city/${city.slug}`}>
          返回{city.nameZh}
        </Link>

        <header className="space-y-4">
          <div className="flex items-center gap-2 text-sm text-neutral-500">
            <span>{CONTENT_TYPE_LABEL[work.contentType]}</span>
            {work.year && (
              <>
                <span aria-hidden="true">/</span>
                <span>{work.year}</span>
              </>
            )}
          </div>
          <div className="space-y-2">
            <h1 className="text-4xl font-semibold tracking-normal">{work.titleZh}</h1>
            {work.titleOriginal && <p className="text-base text-neutral-500">{work.titleOriginal}</p>}
          </div>
          {work.creator && <p className="text-base text-neutral-700">{work.creator}</p>}
          {work.summary && <p className="text-base leading-7 text-neutral-700">{work.summary}</p>}
          <CollectionButton citySlug={city.slug} entityId={work.id} entityType="work" />
        </header>

        {recommendationReason && (
          <Section title="为什么推荐">
            <p className="text-sm leading-6 text-neutral-700">{recommendationReason}</p>
          </Section>
        )}

        {cityConnection && (
          <Section title={`和${city.nameZh}的关系`}>
            <p className="text-sm leading-6 text-neutral-700">{cityConnection}</p>
          </Section>
        )}

        <section className="space-y-3">
          <div className="flex items-end justify-between gap-4">
            <h2 className="text-base font-semibold">关联地点</h2>
            <span className="text-xs text-neutral-500">{relatedPlaces.length} 个地点</span>
          </div>
          <div className="grid gap-3">
            {relatedPlaces.map((place) => (
              <RelatedPlaceCard key={place.id} place={place} />
            ))}
            {relatedPlaces.length === 0 && (
              <p className="rounded-2xl border border-neutral-200 bg-white p-4 text-sm text-neutral-500">
                暂时没有关联地点。
              </p>
            )}
          </div>
        </section>
      </section>

      <nav className="fixed inset-x-0 bottom-0 border-t border-neutral-200 bg-[#f7f5f0]/95 px-5 py-3 backdrop-blur">
        <div className="mx-auto grid max-w-md grid-cols-3 text-center text-sm text-neutral-600">
          <Link className="font-medium text-neutral-950" href="/">
            探索
          </Link>
          <span>收藏</span>
          <span>我的</span>
        </div>
      </nav>
    </main>
  );
}

function Section({ children, title }: { children: ReactNode; title: string }) {
  return (
    <section className="space-y-3 rounded-2xl border border-neutral-200 bg-white p-4">
      <h2 className="text-base font-semibold">{title}</h2>
      {children}
    </section>
  );
}

function RelatedPlaceCard({ place }: { place: RelatedPlace }) {
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
