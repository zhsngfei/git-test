import Link from "next/link";
import type { CitySummary } from "./types";

type HomePageProps = {
  cities: CitySummary[];
};

export function HomePage({ cities }: HomePageProps) {
  return (
    <main className="min-h-dvh bg-[#f7f5f0] text-neutral-950">
      <section className="mx-auto flex w-full max-w-md flex-col gap-8 px-5 pb-12 pt-10">
        <header className="space-y-3">
          <p className="text-sm text-neutral-500">旅行前文化准备</p>
          <h1 className="text-4xl font-semibold tracking-normal">未至</h1>
          <p className="text-base leading-7 text-neutral-700">出发之前，先进入一座城市。</p>
        </header>

        <form className="rounded-2xl border border-neutral-200 bg-white p-3 shadow-sm">
          <label className="block text-sm font-medium text-neutral-700" htmlFor="city-search">
            你想先进入哪座城市？
          </label>
          <div className="mt-3 flex gap-2">
            <input
              className="min-h-12 flex-1 rounded-xl border border-neutral-200 px-4 text-base outline-none focus:border-neutral-900"
              id="city-search"
              placeholder="搜索京都、东京、台北"
            />
            <button
              className="min-h-12 rounded-xl bg-neutral-950 px-4 text-sm font-medium text-white"
              type="submit"
            >
              搜索
            </button>
          </div>
        </form>

        <section className="space-y-3">
          <h2 className="text-base font-semibold">精选城市</h2>
          <div className="grid gap-3">
            {cities.map((city) => (
              <Link
                className="rounded-2xl border border-neutral-200 bg-white p-4 transition hover:border-neutral-300"
                href={`/city/${city.slug}`}
                key={city.slug}
              >
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <h3 className="text-lg font-semibold">{city.nameZh}</h3>
                    <p className="mt-1 text-sm leading-6 text-neutral-600">{city.toneSummary}</p>
                  </div>
                  <span className="rounded-full bg-neutral-100 px-3 py-1 text-xs text-neutral-600">
                    {city.contentDepth === "core" ? "核心" : "扩展"}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}
