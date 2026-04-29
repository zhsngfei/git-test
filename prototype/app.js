const works = [
  {
    id: "norwegian-wood",
    title: "挪威的森林",
    type: "book",
    typeLabel: "书",
    city: "东京",
    image:
      "https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?auto=format&fit=crop&w=900&q=80",
    intro: "一部把青春、孤独和城市气味写得很轻很深的小说。",
    relation: "东京不是背景板，而是人物情绪移动的空间。",
    reason: "去东京前读它，会让校园、车站和普通街道都有一种迟缓的回声。",
    tags: ["文学", "青春", "孤独"],
    favorite: true,
    want: true,
    places: [
      {
        name: "早稻田大学",
        image:
          "https://images.unsplash.com/photo-1558865869-c93f6f8482af?auto=format&fit=crop&w=700&q=80",
        relation: "适合感受小说里学生生活、散步和青春片段的城市肌理。",
      },
      {
        name: "新宿",
        image:
          "https://images.unsplash.com/photo-1542051841857-5f90071e7989?auto=format&fit=crop&w=700&q=80",
        relation: "喧闹街区让作品里的孤独感更明显。",
      },
      {
        name: "井之头公园",
        image: "",
        relation: "暂时没有图，但它适合作为安静散步的想象触点。",
      },
    ],
  },
  {
    id: "lost-in-translation",
    title: "迷失东京",
    type: "film",
    typeLabel: "电影",
    city: "东京",
    image:
      "https://images.unsplash.com/photo-1536098561742-ca998e48cbcc?auto=format&fit=crop&w=900&q=80",
    intro: "异乡酒店、夜色和短暂相遇构成一场轻轻的城市漂浮。",
    relation: "东京在电影里呈现为既疏离又温柔的夜间迷宫。",
    reason: "去东京前看它，会更容易理解旅途中那种短暂失重的感觉。",
    tags: ["电影", "夜色", "异乡"],
    favorite: false,
    want: true,
    places: [
      {
        name: "新宿柏悦酒店",
        image:
          "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=700&q=80",
        relation: "高处夜景是电影最具代表性的孤独视角。",
      },
      {
        name: "涩谷",
        image:
          "https://images.unsplash.com/photo-1542931287-023b922fa89b?auto=format&fit=crop&w=700&q=80",
        relation: "霓虹、街口和人潮构成东京的视觉节奏。",
      },
    ],
  },
  {
    id: "tokyo-story",
    title: "东京物语",
    type: "film",
    typeLabel: "电影",
    city: "东京",
    image:
      "https://images.unsplash.com/photo-1505069190533-da1c9af13346?auto=format&fit=crop&w=900&q=80",
    intro: "关于家庭、距离和现代城市的一部安静经典。",
    relation: "东京代表生活变迁，也代表人与人之间慢慢拉开的距离。",
    reason: "它会让你在东京看见速度之外的东西：沉默、亲情和时间。",
    tags: ["经典", "家庭", "人文"],
    favorite: true,
    want: false,
    places: [
      {
        name: "上野",
        image:
          "https://images.unsplash.com/photo-1554797589-7241bb691973?auto=format&fit=crop&w=700&q=80",
        relation: "适合承接旧东京与日常生活感的城市区域。",
      },
    ],
  },
  {
    id: "before-the-coffee",
    title: "在咖啡冷掉之前",
    type: "book",
    typeLabel: "书",
    city: "东京",
    image:
      "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=900&q=80",
    intro: "一间咖啡馆里的时间旅行，温柔、克制，也有一点遗憾。",
    relation: "它把东京压缩成一间可以暂时回望人生的咖啡馆。",
    reason: "适合在出发前读，让普通咖啡馆也变成可以停顿的触点。",
    tags: ["治愈", "当代", "咖啡馆"],
    favorite: false,
    want: false,
    places: [
      {
        name: "神保町",
        image:
          "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=700&q=80",
        relation: "书店和咖啡馆密集，适合承接作品里的阅读气质。",
      },
      {
        name: "表参道咖啡街区",
        image: "",
        relation: "暂时没有图，但适合作为咖啡馆主题的现实延伸。",
      },
    ],
  },
  {
    id: "midnight-diner",
    title: "深夜食堂",
    type: "series",
    typeLabel: "剧集",
    city: "东京",
    image:
      "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80",
    intro: "小店、夜归人和一碗热食，构成东京另一种温柔。",
    relation: "它让东京从巨大都市变成一个个可以坐下来的深夜角落。",
    reason: "看完再去东京，你会更想留意那些不在攻略首页的小店。",
    tags: ["剧集", "深夜", "治愈"],
    favorite: true,
    want: true,
    places: [
      {
        name: "黄金街",
        image:
          "https://images.unsplash.com/photo-1554797589-7241bb691973?auto=format&fit=crop&w=700&q=80",
        relation: "密集小店和窄巷很接近剧集里的深夜氛围。",
      },
      {
        name: "新宿三丁目",
        image:
          "https://images.unsplash.com/photo-1542051841857-5f90071e7989?auto=format&fit=crop&w=700&q=80",
        relation: "适合感受东京夜间餐饮和归途人群。",
      },
    ],
  },
  {
    id: "weathering-with-you",
    title: "天气之子",
    type: "film",
    typeLabel: "电影",
    city: "东京",
    image:
      "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=900&q=80",
    intro: "雨、天空、少年少女和一座被天气包裹的东京。",
    relation: "电影把东京的天桥、楼顶和街道拍成青春寓言。",
    reason: "它会让你在东京抬头看天，而不是只看地图。",
    tags: ["电影", "青春", "动画"],
    favorite: false,
    want: false,
    places: [
      {
        name: "代代木会馆旧址周边",
        image: "",
        relation: "暂时没有图，但它是作品讨论中常被提到的城市触点。",
      },
      {
        name: "田端",
        image:
          "https://images.unsplash.com/photo-1526481280693-3bfa7568e0f3?auto=format&fit=crop&w=700&q=80",
        relation: "普通街区和轨道空间承接了动画里的日常感。",
      },
    ],
  },
];

const state = {
  view: "explore",
  filter: "all",
  favFilter: "all",
  recent: ["迷失东京", "挪威的森林", "深夜食堂"],
};

const workGrid = document.querySelector("#work-grid");
const favoritesGrid = document.querySelector("#favorites-grid");
const favoritesEmpty = document.querySelector("#favorites-empty");
const detailContent = document.querySelector("#detail-content");

function typeMatches(item, filter) {
  return filter === "all" || item.type === filter;
}

function renderWorkCard(work, compact = false) {
  const placesHtml = work.places
    .slice(0, 10)
    .map((place) => {
      const media = place.image
        ? `<img src="${place.image}" alt="${place.name}" />`
        : `<div class="missing-image">暂时<br />没有图</div>`;
      return `
        <div class="place-mini">
          ${media}
          <div>
            <strong>${place.name}</strong>
            <span>${place.relation}</span>
          </div>
        </div>
      `;
    })
    .join("");

  return `
    <article class="work-card" data-type="${work.type}">
      <div class="cover">
        <img src="${work.image}" alt="${work.title}" loading="lazy" />
        <span class="type-badge">${work.typeLabel}</span>
      </div>
      <div class="card-body">
        <div>
          <h3>${work.title}</h3>
          <p>${work.intro}</p>
        </div>
        <div class="reason-box">${work.reason}</div>
        <p>${work.relation}</p>
        <div class="tag-row">${work.tags.map((tag) => `<span>${tag}</span>`).join("")}</div>
        <div class="card-actions">
          <button class="icon-button ${work.favorite ? "active" : ""}" data-favorite="${work.id}" aria-label="收藏 ${work.title}">
            ${work.favorite ? "已收藏" : "收藏"}
          </button>
          <button class="secondary-button ${work.want ? "active" : ""}" data-want="${work.id}" aria-label="标记想读或想看 ${work.title}">
            ${work.want ? "已标记" : "想读 / 想看"}
          </button>
          <button class="secondary-button" data-detail="${work.id}">详情</button>
        </div>
        ${
          compact
            ? ""
            : `<div class="places-preview">
                <button class="place-toggle" data-toggle="${work.id}">${work.places.length} 个相关景点 · 展开</button>
                <div class="places-list" id="places-${work.id}">${placesHtml}</div>
              </div>`
        }
      </div>
    </article>
  `;
}

function renderExplore() {
  const filtered = works.filter((work) => typeMatches(work, state.filter));
  workGrid.innerHTML = filtered.map((work) => renderWorkCard(work)).join("");
}

function renderFavorites() {
  const favorites = works.filter(
    (work) => (work.favorite || work.want) && typeMatches(work, state.favFilter),
  );
  favoritesGrid.innerHTML = favorites.map((work) => renderWorkCard(work, true)).join("");
  favoritesEmpty.classList.toggle("hidden", favorites.length > 0);
}

function renderProfile() {
  document.querySelector("#stat-fav").textContent = works.filter((work) => work.favorite).length;
  document.querySelector("#stat-want").textContent = works.filter((work) => work.want).length;
  document.querySelector("#recent-list").innerHTML = state.recent
    .map(
      (item) => `
        <div class="recent-item">
          <strong>${item}</strong>
          <span>东京</span>
        </div>
      `,
    )
    .join("");
}

function renderDetail(id) {
  const work = works.find((item) => item.id === id);
  if (!work) return;
  if (!state.recent.includes(work.title)) {
    state.recent.unshift(work.title);
    state.recent = state.recent.slice(0, 4);
  }
  detailContent.innerHTML = `
    <article class="detail-layout">
      <div class="detail-media">
        <img src="${work.image}" alt="${work.title}" />
      </div>
      <div class="detail-copy">
        <p class="eyebrow">${work.city} · ${work.typeLabel}</p>
        <h1 id="detail-title">${work.title}</h1>
        <p>${work.intro}</p>
        <div class="reason-box">${work.reason}</div>
        <p>${work.relation}</p>
        <div class="tag-row">${work.tags.map((tag) => `<span>${tag}</span>`).join("")}</div>
        <div class="card-actions">
          <button class="icon-button ${work.favorite ? "active" : ""}" data-favorite="${work.id}">
            ${work.favorite ? "已收藏" : "收藏"}
          </button>
          <button class="secondary-button ${work.want ? "active" : ""}" data-want="${work.id}">
            ${work.want ? "已标记" : "想读 / 想看"}
          </button>
        </div>
        <section class="detail-places">
          ${work.places
            .slice(0, 10)
            .map((place) => {
              const media = place.image
                ? `<img src="${place.image}" alt="${place.name}" />`
                : `<div class="missing-image">暂时<br />没有图</div>`;
              return `
                <article class="detail-place">
                  ${media}
                  <div>
                    <strong>${place.name}</strong>
                    <p>${place.relation}</p>
                  </div>
                  <a href="https://www.google.com/maps/search/${encodeURIComponent(place.name)}" target="_blank" rel="noreferrer">地图</a>
                </article>
              `;
            })
            .join("")}
        </section>
      </div>
    </article>
  `;
  setView("detail");
}

function setView(view) {
  state.view = view;
  document.querySelectorAll(".view").forEach((node) => node.classList.remove("active"));
  document.querySelector(`#${view}-view`).classList.add("active");
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.classList.toggle("active", item.dataset.view === view);
  });
  if (view === "favorites") renderFavorites();
  if (view === "profile") renderProfile();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function updateAll() {
  renderExplore();
  renderFavorites();
  renderProfile();
}

document.addEventListener("click", (event) => {
  const navButton = event.target.closest("[data-view]");
  if (navButton) {
    setView(navButton.dataset.view);
    return;
  }

  const favoriteButton = event.target.closest("[data-favorite]");
  if (favoriteButton) {
    const work = works.find((item) => item.id === favoriteButton.dataset.favorite);
    work.favorite = !work.favorite;
    updateAll();
    if (state.view === "detail") renderDetail(work.id);
    return;
  }

  const wantButton = event.target.closest("[data-want]");
  if (wantButton) {
    const work = works.find((item) => item.id === wantButton.dataset.want);
    work.want = !work.want;
    updateAll();
    if (state.view === "detail") renderDetail(work.id);
    return;
  }

  const toggle = event.target.closest("[data-toggle]");
  if (toggle) {
    const places = document.querySelector(`#places-${toggle.dataset.toggle}`);
    places.classList.toggle("open");
    toggle.textContent = toggle.textContent.includes("展开")
      ? toggle.textContent.replace("展开", "收起")
      : toggle.textContent.replace("收起", "展开");
    return;
  }

  const detailButton = event.target.closest("[data-detail]");
  if (detailButton) {
    renderDetail(detailButton.dataset.detail);
    return;
  }

  const filter = event.target.closest("[data-filter]");
  if (filter) {
    state.filter = filter.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach((item) => item.classList.remove("active"));
    filter.classList.add("active");
    renderExplore();
    return;
  }

  const favFilter = event.target.closest("[data-fav-filter]");
  if (favFilter) {
    state.favFilter = favFilter.dataset.favFilter;
    document.querySelectorAll("[data-fav-filter]").forEach((item) => item.classList.remove("active"));
    favFilter.classList.add("active");
    renderFavorites();
    return;
  }

  const cityTile = event.target.closest("[data-city]");
  if (cityTile) {
    document.querySelector("#city-input").value = cityTile.dataset.city;
    document.querySelector("#results").scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }

  if (event.target.closest("[data-back]")) {
    setView("explore");
  }
});

document.querySelector("#search-form").addEventListener("submit", (event) => {
  event.preventDefault();
  document.querySelector("#results").scrollIntoView({ behavior: "smooth", block: "start" });
});

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => chip.classList.toggle("selected"));
});

updateAll();
