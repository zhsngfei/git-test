export default function Loading() {
  return (
    <main className="flex min-h-dvh items-center bg-[#f7f5f0] px-5 text-neutral-950">
      <section className="mx-auto w-full max-w-md space-y-5">
        <div className="h-2 w-20 overflow-hidden rounded-full bg-neutral-200">
          <div className="h-full w-1/2 animate-pulse rounded-full bg-neutral-900" />
        </div>
        <div className="space-y-3">
          <p className="text-sm text-neutral-500">正在载入</p>
          <h1 className="text-3xl font-semibold tracking-normal">未至</h1>
          <p className="text-base leading-7 text-neutral-700">正在整理城市内容，请稍候。</p>
        </div>
      </section>
    </main>
  );
}
