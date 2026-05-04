import Link from "next/link";

export default function NotFound() {
  return (
    <main className="flex min-h-dvh items-center bg-[#f7f5f0] px-5 text-neutral-950">
      <section className="mx-auto w-full max-w-md space-y-6">
        <div className="space-y-3">
          <p className="text-sm text-neutral-500">404</p>
          <h1 className="text-3xl font-semibold tracking-normal">没有找到这个页面</h1>
          <p className="text-base leading-7 text-neutral-700">
            这个地址可能已经变更。回到首页后，可以从城市列表继续进入内容。
          </p>
        </div>
        <Link
          className="inline-flex min-h-12 items-center justify-center rounded-lg bg-neutral-950 px-5 text-sm font-medium text-white transition hover:bg-neutral-800"
          href="/"
        >
          返回首页
        </Link>
      </section>
    </main>
  );
}
