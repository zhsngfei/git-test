"use client";

import Link from "next/link";

type ErrorPageProps = {
  reset: () => void;
};

export default function ErrorPage({ reset }: ErrorPageProps) {
  return (
    <main className="flex min-h-dvh items-center bg-[#f7f5f0] px-5 text-neutral-950">
      <section className="mx-auto w-full max-w-md space-y-6">
        <div className="space-y-3">
          <p className="text-sm text-neutral-500">页面暂时不可用</p>
          <h1 className="text-3xl font-semibold tracking-normal">内容没有顺利打开</h1>
          <p className="text-base leading-7 text-neutral-700">
            可以重新尝试载入，或返回首页继续浏览其他城市。
          </p>
        </div>
        <div className="flex flex-col gap-3 sm:flex-row">
          <button
            className="min-h-12 rounded-lg bg-neutral-950 px-5 text-sm font-medium text-white transition hover:bg-neutral-800"
            onClick={reset}
            type="button"
          >
            重新载入
          </button>
          <Link
            className="flex min-h-12 items-center justify-center rounded-lg border border-neutral-300 bg-white px-5 text-sm font-medium text-neutral-900 transition hover:border-neutral-400"
            href="/"
          >
            返回首页
          </Link>
        </div>
      </section>
    </main>
  );
}
