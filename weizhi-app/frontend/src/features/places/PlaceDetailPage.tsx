import Link from "next/link";
import { CollectionButton } from "@/features/collections/CollectionButton";
import type { PlaceDetailResponse, RelatedWork } from "./types";

type PlaceDetailPageProps = {
  detail: PlaceDetailResponse;
};

const CONTENT_TYPE_LABEL: Record<RelatedWork["contentType"], string> = {
  book: "书籍",
  film: "电影",
  series: "剧集",
};

export function PlaceDetailPage({ detail }: PlaceDetailPageProps) {
  const { city, meaning, place, relatedWorks } = detail;

  return (
    <main className="min-h-dvh bg-[#f7f5f0] pb-20 text-neutral-950">
      <section className="mx-auto flex w-full max-w-md flex-col gap-7 px-5 pb-8 pt-6">
        <Link className="text-sm text-neutral-500" href={`/city/${city.slug}`}>
          返回{city.nameZh}
        </Link>

        <header className="space-y-4">
          <div className="space-y-2">
            {place.area && <p className="text-sm text-neutral-500">{place.area}</p>}
            <h1 className="text-4xl font-semibold tracking-normal">{place.nameZh}</h1>
            {place.nameOriginal && <p className="text-base text-neutral-500">{place.nameOriginal}</p>}
          </div>
          {place.summary && <p className="text-base leading-7 text-neutral-700">{place.summary}</p>}
          <CollectionButton citySlug={city.slug} entityId={place.id} entityType="place" />
        </header>

        {meaning && (
          <section className="space-y-3 rounded-2xl border border-neutral-200 bg-white p-4">
            <h2 className="text-base font-semibold">地点意义</h2>
            <p className="text-sm leading-6 text-neutral-700">{meaning}</p>
          </section>
        )}

        <section className="space-y-3">
          <div className="flex items-end justify-between gap-4">
            <h2 className="text-base font-semibold">关联作品</h2>
            <span className="text-xs text-neutral-500">{relatedWorks.length} 个作品</span>
          </div>
          <div className="grid gap-3">
            {relatedWorks.map((work) => (
              <RelatedWorkCard key={work.id} work={work} />
            ))}
            {relatedWorks.length === 0 && (
              <p className="rounded-2xl border border-neutral-200 bg-white p-4 text-sm text-neutral-500">
                暂时没有关联作品。
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

function RelatedWorkCard({ work }: { work: RelatedWork }) {
  const content = (
    <article className="rounded-2xl border border-neutral-200 bg-white p-4 transition hover:border-neutral-300">
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
