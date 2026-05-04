"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { AuthDialog } from "@/features/auth/AuthDialog";
import { getAuthSession, type AuthSession } from "@/features/auth/session";
import { supabase } from "@/features/auth/supabaseClient";
import { getPreparationBook } from "./api";
import type { PreparationBook, PreparationCityGroup, PreparationWork } from "./types";

type ActiveTab = "works" | "places";

const CONTENT_TYPE_LABEL: Record<PreparationWork["contentType"], string> = {
  book: "书籍",
  film: "电影",
  series: "剧集",
};

export function CollectionsPage() {
  const [authSession, setAuthSession] = useState<AuthSession | null>(null);
  const [book, setBook] = useState<PreparationBook | null>(null);
  const [activeTabByCity, setActiveTabByCity] = useState<Record<string, ActiveTab>>({});
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadPreparationBook = useCallback(async (accessToken: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const nextBook = await getPreparationBook(accessToken);
      setBook(nextBook);
    } catch {
      setError("暂时无法读取收藏准备册，请稍后再试。");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    let isMounted = true;

    void getAuthSession()
      .then((session) => {
        if (!isMounted) {
          return;
        }
        setAuthSession(session);
        if (session) {
          void loadPreparationBook(session.accessToken);
        }
      })
      .catch(() => {
        if (isMounted) {
          setError("暂时无法读取登录状态，请稍后再试。");
        }
      });

    const { data } = supabase.auth.onAuthStateChange((_event, session) => {
      if (!isMounted) {
        return;
      }
      const nextSession = session
        ? {
            accessToken: session.access_token,
            user: session.user,
          }
        : null;
      setAuthSession(nextSession);
      if (nextSession) {
        void loadPreparationBook(nextSession.accessToken);
      } else {
        setBook(null);
      }
    });

    return () => {
      isMounted = false;
      data.subscription.unsubscribe();
    };
  }, [loadPreparationBook]);

  async function handleAuthenticated() {
    const nextSession = await getAuthSession();
    setAuthSession(nextSession);
    setIsAuthOpen(false);
    if (nextSession) {
      await loadPreparationBook(nextSession.accessToken);
    }
  }

  function tabForCity(citySlug: string): ActiveTab {
    return activeTabByCity[citySlug] ?? "works";
  }

  function setTab(citySlug: string, tab: ActiveTab) {
    setActiveTabByCity((tabs) => ({ ...tabs, [citySlug]: tab }));
  }

  return (
    <main className="min-h-dvh bg-[#f7f5f0] pb-20 text-neutral-950">
      <section className="mx-auto flex w-full max-w-md flex-col gap-7 px-5 pb-8 pt-6">
        <header className="space-y-3">
          <p className="text-sm text-neutral-500">我的收藏</p>
          <h1 className="text-4xl font-semibold tracking-normal">出发前准备册</h1>
          <p className="text-base leading-7 text-neutral-700">按城市整理已经收藏的作品和地点。</p>
        </header>

        {!authSession && !isLoading && (
          <section className="rounded-2xl border border-neutral-200 bg-white p-4">
            <h2 className="text-base font-semibold">登录后查看收藏</h2>
            <p className="mt-2 text-sm leading-6 text-neutral-600">
              用邮箱继续后，可以查看你的出发前准备内容。
            </p>
            <button
              className="mt-4 min-h-12 w-full rounded-xl bg-neutral-950 px-4 text-sm font-medium text-white"
              onClick={() => setIsAuthOpen(true)}
              type="button"
            >
              登录查看
            </button>
          </section>
        )}

        {isLoading && <p className="rounded-2xl border border-neutral-200 bg-white p-4 text-sm">正在整理收藏...</p>}
        {error && <p className="rounded-2xl border border-neutral-200 bg-white p-4 text-sm text-neutral-600">{error}</p>}

        {authSession && book?.cities.length === 0 && (
          <section className="rounded-2xl border border-neutral-200 bg-white p-4">
            <h2 className="text-base font-semibold">还没有收藏</h2>
            <p className="mt-2 text-sm leading-6 text-neutral-600">先从城市页进入作品或地点，收藏后会出现在这里。</p>
            <Link className="mt-4 block min-h-12 rounded-xl bg-neutral-950 px-4 py-3 text-center text-sm font-medium text-white" href="/">
              去探索
            </Link>
          </section>
        )}

        {book?.cities.map((group) => {
          const activeTab = tabForCity(group.city.slug);
          return (
            <CityCollectionGroup
              activeTab={activeTab}
              group={group}
              key={group.city.slug}
              onTabChange={(tab) => setTab(group.city.slug, tab)}
            />
          );
        })}
      </section>

      <nav className="fixed inset-x-0 bottom-0 border-t border-neutral-200 bg-[#f7f5f0]/95 px-5 py-3 backdrop-blur">
        <div className="mx-auto grid max-w-md grid-cols-3 text-center text-sm text-neutral-600">
          <Link href="/">探索</Link>
          <span className="font-medium text-neutral-950">收藏</span>
          <span>我的</span>
        </div>
      </nav>

      <AuthDialog
        isOpen={isAuthOpen}
        onAuthenticated={handleAuthenticated}
        onClose={() => setIsAuthOpen(false)}
      />
    </main>
  );
}

function CityCollectionGroup({
  activeTab,
  group,
  onTabChange,
}: {
  activeTab: ActiveTab;
  group: PreparationCityGroup;
  onTabChange: (tab: ActiveTab) => void;
}) {
  return (
    <section className="space-y-4 rounded-2xl border border-neutral-200 bg-white p-4">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm text-neutral-500">{group.city.countryRegion}</p>
          <h2 className="mt-1 text-2xl font-semibold">{group.city.nameZh}</h2>
          <p className="mt-2 text-sm text-neutral-600">
            作品 {group.works.length} · 地点 {group.places.length}
          </p>
        </div>
        <Link className="rounded-full bg-neutral-100 px-3 py-1 text-xs text-neutral-600" href={`/city/${group.city.slug}`}>
          查看城市
        </Link>
      </div>

      <div className="grid grid-cols-2 rounded-xl border border-neutral-200 bg-neutral-50 p-1">
        <button
          className={`min-h-10 rounded-lg text-sm ${activeTab === "works" ? "bg-white font-medium shadow-sm" : "text-neutral-600"}`}
          onClick={() => onTabChange("works")}
          type="button"
        >
          作品
        </button>
        <button
          className={`min-h-10 rounded-lg text-sm ${activeTab === "places" ? "bg-white font-medium shadow-sm" : "text-neutral-600"}`}
          onClick={() => onTabChange("places")}
          type="button"
        >
          地点
        </button>
      </div>

      <div className="grid gap-3">
        {activeTab === "works" &&
          group.works.map((work) => (
            <Link className="rounded-xl border border-neutral-200 p-3 transition hover:border-neutral-300" href={`/works/${work.slug}`} key={work.id}>
              <p className="text-xs font-medium text-neutral-500">{CONTENT_TYPE_LABEL[work.contentType]}</p>
              <h3 className="mt-1 text-lg font-semibold">{work.titleZh}</h3>
              {work.summary && <p className="mt-2 text-sm leading-6 text-neutral-600">{work.summary}</p>}
            </Link>
          ))}
        {activeTab === "places" &&
          group.places.map((place) => (
            <Link className="rounded-xl border border-neutral-200 p-3 transition hover:border-neutral-300" href={`/places/${place.slug}`} key={place.id}>
              <h3 className="text-lg font-semibold">{place.nameZh}</h3>
              {place.summary && <p className="mt-2 text-sm leading-6 text-neutral-600">{place.summary}</p>}
            </Link>
          ))}
      </div>
    </section>
  );
}
