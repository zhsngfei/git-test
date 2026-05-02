# Weizhi App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建立未至第一版真实上线产品的干净项目骨架，并按功能切片推进到可浏览真实内容、可登录收藏、可接入 mimoaiapi 推荐的完整闭环。

**Architecture:** 新建 `weizhi-app/`，采用前后端分离但同仓管理。`frontend/` 使用 Next.js、Tailwind CSS v4、shadcn/ui；`backend/` 使用 FastAPI、Pydantic、Supabase PostgreSQL；内容通过 CSV/Excel 导入数据库；AI 通过独立 `mimoaiapi` Provider 封装；第一阶段推荐缓存使用数据库表。

**Tech Stack:** Next.js, TypeScript, Tailwind CSS v4, shadcn/ui, FastAPI, Python, Pydantic, Supabase PostgreSQL/Auth, mimoaiapi, pytest, Vitest/Playwright, CSV/Excel import.

---

## 0. 执行原则

本计划遵循以下原则：

- 新建干净目录 `D:\codex.files\git-test\weizhi-app`，不沿用旧 `prototype/`。
- 按功能切片交付，但先搭最小工程骨架。
- 每个切片尽量穿过前端、后端、数据、状态和测试。
- UI/UX 只遵循中文产品 spec 的“现代城市笔记感”，不参考外部图片视觉。
- AI 服务名称统一为 `mimoaiapi`。
- Redis 只预留，不作为第一阶段必需服务。
- 第一版运行时不读取 CSV/Excel，应用读取数据库。
- 每个任务完成后运行对应验证命令。

## 1. 文件结构

最终项目结构：

```text
D:\codex.files\git-test\weizhi-app\
  frontend\
    app\
    components\
      ui\
      layout\
      cards\
      states\
    features\
      home\
      city\
      works\
      places\
      collections\
      auth\
      recommendations\
    lib\
      api\
      auth\
      constants\
      formatting\
    tests\
  backend\
    app\
      api\
      core\
      db\
      features\
        cities\
        works\
        places\
        collections\
        recommendations\
        content_import\
      schemas\
      services\
        ai_provider\
        cache\
        auth\
    tests\
  content\
    csv\
    templates\
  docs\
```

## 2. 功能切片顺序

| 顺序 | 切片 | 用户可感知结果 |
|---:|---|---|
| 1 | 项目基础骨架 | 前后端能启动，有统一目录、环境变量和测试入口 |
| 2 | 数据模型与内容导入 | CSV/Excel 内容可以校验并导入数据库 |
| 3 | 内容浏览 | 首页搜索城市后能看到真实数据库内容 |
| 4 | 作品与地点详情 | 用户可以从作品进入地点触点 |
| 5 | 登录与收藏 | 用户登录后可收藏作品和地点 |
| 6 | 收藏准备册 | 收藏页按城市展示作品和地点 |
| 7 | mimoaiapi 推荐 | 系统基于真实数据生成主题分组和推荐解释 |
| 8 | 上线质量 | 移动端、加载、错误、空状态和部署检查完成 |

---

## Task 1: 创建干净项目骨架

**Files:**
- Create: `D:\codex.files\git-test\weizhi-app\README.md`
- Create: `D:\codex.files\git-test\weizhi-app\.gitignore`
- Create: `D:\codex.files\git-test\weizhi-app\docs\architecture.md`
- Create directories under `D:\codex.files\git-test\weizhi-app\frontend`, `backend`, and `content`

- [ ] **Step 1: 创建目录**

Run:

```powershell
New-Item -ItemType Directory -Force -Path 'D:\codex.files\git-test\weizhi-app\frontend'
New-Item -ItemType Directory -Force -Path 'D:\codex.files\git-test\weizhi-app\backend'
New-Item -ItemType Directory -Force -Path 'D:\codex.files\git-test\weizhi-app\content\csv'
New-Item -ItemType Directory -Force -Path 'D:\codex.files\git-test\weizhi-app\content\templates'
New-Item -ItemType Directory -Force -Path 'D:\codex.files\git-test\weizhi-app\docs'
```

Expected: all directories exist.

- [ ] **Step 2: 写入根 README**

Create `D:\codex.files\git-test\weizhi-app\README.md`:

```markdown
# 未至

未至是一款移动优先的旅行前文化准备应用。

第一版技术结构：

- 前端：Next.js + Tailwind CSS v4 + shadcn/ui
- 后端：FastAPI
- 数据库和登录：Supabase PostgreSQL/Auth
- AI：mimoaiapi
- 内容导入：CSV/Excel -> FastAPI -> PostgreSQL

开发原则：

- 按功能切片交付
- 前后端同仓分目录管理
- UI 遵循现代城市笔记感
- AI 不生成数据库之外的事实
```

- [ ] **Step 3: 写入 `.gitignore`**

Create `D:\codex.files\git-test\weizhi-app\.gitignore`:

```gitignore
node_modules/
.next/
dist/
build/
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
.env
.env.*
!.env.example
coverage/
playwright-report/
test-results/
*.pyc
*.log
```

- [ ] **Step 4: 写入架构摘要**

Create `D:\codex.files\git-test\weizhi-app\docs\architecture.md`:

```markdown
# 未至架构摘要

## 分工

- Next.js：移动优先前端、页面路由、登录状态展示、调用 FastAPI。
- FastAPI：业务接口、CSV/Excel 导入、AI 推荐编排、缓存和数据校验。
- Supabase：PostgreSQL 数据库和邮箱登录。
- mimoaiapi：推荐排序、主题分组和推荐解释。

## 约束

- UI 不参考旧原型和外部截图视觉。
- AI 只能使用数据库中已核验事实。
- 第一阶段推荐缓存使用数据库表。
```

- [ ] **Step 5: 验证目录**

Run:

```powershell
Get-ChildItem -Recurse -Depth 2 'D:\codex.files\git-test\weizhi-app'
```

Expected: output contains `frontend`, `backend`, `content`, `docs`, `README.md`, `.gitignore`.

- [ ] **Step 6: Commit**

Run:

```powershell
git add weizhi-app
git commit -m "chore: create weizhi app workspace"
```

Expected: commit succeeds.

---

## Task 2: 初始化前端 Next.js 应用

**Files:**
- Create/Modify under `D:\codex.files\git-test\weizhi-app\frontend`
- Create: `D:\codex.files\git-test\weizhi-app\frontend\.env.example`
- Create: `D:\codex.files\git-test\weizhi-app\frontend\src\features\home`
- Create: `D:\codex.files\git-test\weizhi-app\frontend\src\features\city`
- Create: `D:\codex.files\git-test\weizhi-app\frontend\src\features\works`
- Create: `D:\codex.files\git-test\weizhi-app\frontend\src\features\places`
- Create: `D:\codex.files\git-test\weizhi-app\frontend\src\features\collections`
- Create: `D:\codex.files\git-test\weizhi-app\frontend\src\features\auth`

- [ ] **Step 1: 使用 Next.js 创建前端**

Run:

```powershell
Set-Location 'D:\codex.files\git-test\weizhi-app'
npx create-next-app@latest frontend --ts --eslint --app --src-dir --use-npm --import-alias "@/*"
```

Expected: `frontend/package.json` exists and app uses `src/app`.

- [ ] **Step 2: 安装 UI 依赖**

Run:

```powershell
Set-Location 'D:\codex.files\git-test\weizhi-app\frontend'
npm install lucide-react class-variance-authority clsx tailwind-merge
```

Expected: packages are added to `package.json`.

- [ ] **Step 3: 创建前端目录**

Run:

```powershell
New-Item -ItemType Directory -Force -Path 'src\components\ui'
New-Item -ItemType Directory -Force -Path 'src\components\layout'
New-Item -ItemType Directory -Force -Path 'src\components\cards'
New-Item -ItemType Directory -Force -Path 'src\components\states'
New-Item -ItemType Directory -Force -Path 'src\features\home'
New-Item -ItemType Directory -Force -Path 'src\features\city'
New-Item -ItemType Directory -Force -Path 'src\features\works'
New-Item -ItemType Directory -Force -Path 'src\features\places'
New-Item -ItemType Directory -Force -Path 'src\features\collections'
New-Item -ItemType Directory -Force -Path 'src\features\auth'
New-Item -ItemType Directory -Force -Path 'src\features\recommendations'
New-Item -ItemType Directory -Force -Path 'src\lib\api'
New-Item -ItemType Directory -Force -Path 'src\lib\auth'
New-Item -ItemType Directory -Force -Path 'src\lib\constants'
```

Expected: feature and component folders exist.

- [ ] **Step 4: 写入前端环境变量示例**

Create `D:\codex.files\git-test\weizhi-app\frontend\.env.example`:

```dotenv
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://example.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=replace-with-supabase-anon-key
```

- [ ] **Step 5: 写入 API 客户端基础文件**

Create `D:\codex.files\git-test\weizhi-app\frontend\src\lib\api\client.ts`:

```ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}
```

- [ ] **Step 6: 验证前端 lint**

Run:

```powershell
npm run lint
```

Expected: lint completes without errors.

- [ ] **Step 7: Commit**

Run:

```powershell
git add weizhi-app/frontend
git commit -m "chore: initialize weizhi frontend"
```

Expected: commit succeeds.

---

## Task 3: 初始化 FastAPI 后端

**Files:**
- Create: `D:\codex.files\git-test\weizhi-app\backend\pyproject.toml`
- Create: `D:\codex.files\git-test\weizhi-app\backend\.env.example`
- Create: `D:\codex.files\git-test\weizhi-app\backend\app\main.py`
- Create: `D:\codex.files\git-test\weizhi-app\backend\app\core\config.py`
- Create: `D:\codex.files\git-test\weizhi-app\backend\tests\test_health.py`

- [ ] **Step 1: 创建后端目录**

Run:

```powershell
Set-Location 'D:\codex.files\git-test\weizhi-app\backend'
New-Item -ItemType Directory -Force -Path 'app\api'
New-Item -ItemType Directory -Force -Path 'app\core'
New-Item -ItemType Directory -Force -Path 'app\db'
New-Item -ItemType Directory -Force -Path 'app\features\cities'
New-Item -ItemType Directory -Force -Path 'app\features\works'
New-Item -ItemType Directory -Force -Path 'app\features\places'
New-Item -ItemType Directory -Force -Path 'app\features\collections'
New-Item -ItemType Directory -Force -Path 'app\features\recommendations'
New-Item -ItemType Directory -Force -Path 'app\features\content_import'
New-Item -ItemType Directory -Force -Path 'app\schemas'
New-Item -ItemType Directory -Force -Path 'app\services\ai_provider'
New-Item -ItemType Directory -Force -Path 'app\services\cache'
New-Item -ItemType Directory -Force -Path 'tests'
```

- [ ] **Step 2: 写入 Python 项目配置**

Create `D:\codex.files\git-test\weizhi-app\backend\pyproject.toml`:

```toml
[project]
name = "weizhi-backend"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "fastapi>=0.115.0",
  "uvicorn[standard]>=0.30.0",
  "pydantic>=2.7.0",
  "pydantic-settings>=2.3.0",
  "pytest>=8.2.0",
  "httpx>=0.27.0",
  "python-multipart>=0.0.9",
  "pandas>=2.2.0",
  "openpyxl>=3.1.0",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

- [ ] **Step 3: 写入后端环境变量示例**

Create `D:\codex.files\git-test\weizhi-app\backend\.env.example`:

```dotenv
APP_ENV=local
SUPABASE_URL=https://example.supabase.co
SUPABASE_SERVICE_ROLE_KEY=replace-with-service-role-key
SUPABASE_JWT_SECRET=replace-with-jwt-secret
MIMOAI_API_BASE_URL=https://api.example.com
MIMOAI_API_KEY=replace-with-mimoai-key
```

- [ ] **Step 4: 写入配置模块**

Create `D:\codex.files\git-test\weizhi-app\backend\app\core\config.py`:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    supabase_url: str
    supabase_service_role_key: str
    supabase_jwt_secret: str
    mimoai_api_base_url: str
    mimoai_api_key: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()  # type: ignore[call-arg]
```

- [ ] **Step 5: 写入 FastAPI 入口**

Create `D:\codex.files\git-test\weizhi-app\backend\app\main.py`:

```python
from fastapi import FastAPI

app = FastAPI(title="Weizhi API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

- [ ] **Step 6: 写入健康检查测试**

Create `D:\codex.files\git-test\weizhi-app\backend\tests\test_health.py`:

```python
from fastapi.testclient import TestClient

from app.main import app


def test_health_returns_ok() -> None:
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [ ] **Step 7: 验证后端测试**

Run:

```powershell
Set-Location 'D:\codex.files\git-test\weizhi-app\backend'
python -m pip install -e .
python -m pytest
```

Expected: `test_health_returns_ok` passes.

- [ ] **Step 8: Commit**

Run:

```powershell
git add weizhi-app/backend
git commit -m "chore: initialize weizhi backend"
```

Expected: commit succeeds.

---

## Task 4: 定义数据库 schema 和核心类型

**Files:**
- Create: `D:\codex.files\git-test\weizhi-app\backend\app\db\schema.sql`
- Create: `D:\codex.files\git-test\weizhi-app\backend\app\schemas\content.py`
- Create: `D:\codex.files\git-test\weizhi-app\backend\tests\test_content_schema.py`

- [ ] **Step 1: 写入数据库 schema**

Create `D:\codex.files\git-test\weizhi-app\backend\app\db\schema.sql`:

```sql
create table if not exists cities (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  name_zh text not null,
  name_en text,
  country_region text not null,
  is_supported boolean not null default false,
  content_depth text not null check (content_depth in ('core', 'expansion', 'unsupported')),
  tone_summary text,
  hero_image_url text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists works (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  title text not null,
  original_title text,
  work_type text not null check (work_type in ('book', 'film', 'series')),
  creator text,
  year text,
  synopsis text not null,
  cover_image_url text,
  review_status text not null check (review_status in ('draft', 'reviewed', 'published')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists places (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  city_id uuid not null references cities(id) on delete cascade,
  name text not null,
  intro text not null,
  image_url text,
  address text,
  latitude numeric,
  longitude numeric,
  map_query text,
  review_status text not null check (review_status in ('draft', 'reviewed', 'published')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists work_city_relations (
  id uuid primary key default gen_random_uuid(),
  work_id uuid not null references works(id) on delete cascade,
  city_id uuid not null references cities(id) on delete cascade,
  relation_summary text not null,
  recommendation_note text not null,
  theme_tags text[] not null default '{}',
  source_url text,
  source_note text,
  review_status text not null check (review_status in ('draft', 'reviewed', 'published')),
  unique(work_id, city_id)
);

create table if not exists work_place_relations (
  id uuid primary key default gen_random_uuid(),
  work_id uuid not null references works(id) on delete cascade,
  place_id uuid not null references places(id) on delete cascade,
  meaning text not null,
  source_url text,
  source_note text,
  review_status text not null check (review_status in ('draft', 'reviewed', 'published')),
  unique(work_id, place_id)
);

create table if not exists collections (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,
  entity_type text not null check (entity_type in ('work', 'place')),
  entity_id uuid not null,
  city_id uuid not null references cities(id) on delete cascade,
  created_at timestamptz not null default now(),
  unique(user_id, entity_type, entity_id)
);

create table if not exists recommendation_caches (
  id uuid primary key default gen_random_uuid(),
  city_id uuid not null references cities(id) on delete cascade,
  content_type text not null default 'all',
  theme_tags text[] not null default '{}',
  cache_key text not null unique,
  result_json jsonb not null,
  generation_mode text not null check (generation_mode in ('pre_generated', 'realtime')),
  review_status text not null check (review_status in ('draft', 'reviewed', 'published')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
```

- [ ] **Step 2: 写入 Pydantic 内容类型**

Create `D:\codex.files\git-test\weizhi-app\backend\app\schemas\content.py`:

```python
from enum import StrEnum
from pydantic import BaseModel, Field


class WorkType(StrEnum):
    book = "book"
    film = "film"
    series = "series"


class ReviewStatus(StrEnum):
    draft = "draft"
    reviewed = "reviewed"
    published = "published"


class ContentDepth(StrEnum):
    core = "core"
    expansion = "expansion"
    unsupported = "unsupported"


class CityRecord(BaseModel):
    slug: str
    name_zh: str
    name_en: str | None = None
    country_region: str
    is_supported: bool
    content_depth: ContentDepth
    tone_summary: str | None = None
    hero_image_url: str | None = None


class WorkRecord(BaseModel):
    slug: str
    title: str
    original_title: str | None = None
    work_type: WorkType
    creator: str | None = None
    year: str | None = None
    synopsis: str = Field(min_length=1)
    cover_image_url: str | None = None
    review_status: ReviewStatus


class PlaceRecord(BaseModel):
    slug: str
    city_slug: str
    name: str
    intro: str = Field(min_length=1)
    image_url: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    map_query: str | None = None
    review_status: ReviewStatus
```

- [ ] **Step 3: 写入 schema 测试**

Create `D:\codex.files\git-test\weizhi-app\backend\tests\test_content_schema.py`:

```python
import pytest
from pydantic import ValidationError

from app.schemas.content import CityRecord, ContentDepth, ReviewStatus, WorkRecord, WorkType


def test_city_record_accepts_supported_core_city() -> None:
    city = CityRecord(
        slug="kyoto",
        name_zh="京都",
        country_region="日本",
        is_supported=True,
        content_depth=ContentDepth.core,
    )

    assert city.slug == "kyoto"


def test_work_record_requires_synopsis() -> None:
    with pytest.raises(ValidationError):
        WorkRecord(
            slug="empty",
            title="空作品",
            work_type=WorkType.book,
            synopsis="",
            review_status=ReviewStatus.reviewed,
        )
```

- [ ] **Step 4: 运行后端测试**

Run:

```powershell
Set-Location 'D:\codex.files\git-test\weizhi-app\backend'
python -m pytest
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

Run:

```powershell
git add weizhi-app/backend/app/db/schema.sql weizhi-app/backend/app/schemas/content.py weizhi-app/backend/tests/test_content_schema.py
git commit -m "feat: define content data schema"
```

Expected: commit succeeds.

---

## Task 5: 建立 CSV/Excel 内容模板和导入校验

**Files:**
- Create: `D:\codex.files\git-test\weizhi-app\content\templates\cities.csv`
- Create: `D:\codex.files\git-test\weizhi-app\content\templates\works.csv`
- Create: `D:\codex.files\git-test\weizhi-app\content\templates\places.csv`
- Create: `D:\codex.files\git-test\weizhi-app\content\templates\work_city_relations.csv`
- Create: `D:\codex.files\git-test\weizhi-app\content\templates\work_place_relations.csv`
- Create: `D:\codex.files\git-test\weizhi-app\backend\app\features\content_import\validator.py`
- Create: `D:\codex.files\git-test\weizhi-app\backend\tests\test_content_import_validator.py`

- [ ] **Step 1: 写入城市 CSV 模板**

Create `D:\codex.files\git-test\weizhi-app\content\templates\cities.csv`:

```csv
slug,name_zh,name_en,country_region,is_supported,content_depth,tone_summary,hero_image_url
kyoto,京都,Kyoto,日本,true,core,安静、古典、适合旅行前慢慢进入的城市,
tokyo,东京,Tokyo,日本,true,core,孤独、夜晚、现代都市与日常缝隙,
```

- [ ] **Step 2: 写入作品 CSV 模板**

Create `D:\codex.files\git-test\weizhi-app\content\templates\works.csv`:

```csv
slug,title,original_title,work_type,creator,year,synopsis,cover_image_url,review_status
old-capital,古都,古都,book,川端康成,1962,一部通过京都街巷和传统生活气息进入城市记忆的小说,,reviewed
lost-in-translation,迷失东京,Lost in Translation,film,Sofia Coppola,2003,一部以东京夜晚和异乡感为核心气质的电影,,reviewed
```

- [ ] **Step 3: 写入地点 CSV 模板**

Create `D:\codex.files\git-test\weizhi-app\content\templates\places.csv`:

```csv
slug,city_slug,name,intro,image_url,address,latitude,longitude,map_query,review_status
gion,kyoto,祇园,京都代表性的传统街区之一，与城市的古典气质和夜色记忆紧密相关,,,,,京都 祇园,reviewed
kamo-river,kyoto,鸭川,贯穿京都日常生活的河流，也是许多城市漫游经验的起点,,,,,京都 鸭川,reviewed
```

- [ ] **Step 4: 写入关系 CSV 模板**

Create `D:\codex.files\git-test\weizhi-app\content\templates\work_city_relations.csv`:

```csv
work_slug,city_slug,relation_summary,recommendation_note,theme_tags,source_url,source_note,review_status
old-capital,kyoto,作品以京都传统生活和城市记忆为核心背景,适合在出发前用安静方式进入京都的季节感和旧日秩序,"安静|经典|文学感",,人工核验,reviewed
lost-in-translation,tokyo,电影通过东京酒店、街道和夜晚表现异乡人的孤独感,适合想从夜色和疏离感进入东京的用户,"孤独|电影感|城市漫游",,人工核验,reviewed
```

Create `D:\codex.files\git-test\weizhi-app\content\templates\work_place_relations.csv`:

```csv
work_slug,place_slug,meaning,source_url,source_note,review_status
old-capital,gion,祇园能帮助用户理解作品中京都传统街区和旧日生活秩序的气质,,人工核验,reviewed
old-capital,kamo-river,鸭川作为京都日常和漫游经验的触点，可以连接作品中的城市季节感,,人工核验,reviewed
```

- [ ] **Step 5: 写入导入校验器**

Create `D:\codex.files\git-test\weizhi-app\backend\app\features\content_import\validator.py`:

```python
import csv
from pathlib import Path


REQUIRED_COLUMNS: dict[str, set[str]] = {
    "cities.csv": {"slug", "name_zh", "country_region", "is_supported", "content_depth"},
    "works.csv": {"slug", "title", "work_type", "synopsis", "review_status"},
    "places.csv": {"slug", "city_slug", "name", "intro", "review_status"},
    "work_city_relations.csv": {
        "work_slug",
        "city_slug",
        "relation_summary",
        "recommendation_note",
        "theme_tags",
        "review_status",
    },
    "work_place_relations.csv": {"work_slug", "place_slug", "meaning", "review_status"},
}


def validate_csv_columns(path: Path) -> list[str]:
    required = REQUIRED_COLUMNS[path.name]

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])

    missing = sorted(required - columns)
    return missing
```

- [ ] **Step 6: 写入导入校验测试**

Create `D:\codex.files\git-test\weizhi-app\backend\tests\test_content_import_validator.py`:

```python
from pathlib import Path

from app.features.content_import.validator import validate_csv_columns


def test_cities_template_has_required_columns() -> None:
    path = Path("../content/templates/cities.csv").resolve()

    missing = validate_csv_columns(path)

    assert missing == []
```

- [ ] **Step 7: 运行测试**

Run:

```powershell
Set-Location 'D:\codex.files\git-test\weizhi-app\backend'
python -m pytest
```

Expected: content import validator test passes.

- [ ] **Step 8: Commit**

Run:

```powershell
git add weizhi-app/content weizhi-app/backend/app/features/content_import weizhi-app/backend/tests/test_content_import_validator.py
git commit -m "feat: add content import templates"
```

Expected: commit succeeds.

---

## Task 6: 实现内容浏览 API 第一切片

**Files:**
- Create: `D:\codex.files\git-test\weizhi-app\backend\app\features\cities\router.py`
- Create: `D:\codex.files\git-test\weizhi-app\backend\app\features\cities\repository.py`
- Modify: `D:\codex.files\git-test\weizhi-app\backend\app\main.py`
- Create: `D:\codex.files\git-test\weizhi-app\backend\tests\test_cities_api.py`

- [ ] **Step 1: 写入城市 API 测试**

Create `D:\codex.files\git-test\weizhi-app\backend\tests\test_cities_api.py`:

```python
from fastapi.testclient import TestClient

from app.main import app


def test_list_supported_cities_returns_seed_shape() -> None:
    client = TestClient(app)
    response = client.get("/api/cities")

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    assert payload[0]["slug"] == "kyoto"
    assert payload[0]["nameZh"] == "京都"
```

- [ ] **Step 2: 写入临时 repository**

Create `D:\codex.files\git-test\weizhi-app\backend\app\features\cities\repository.py`:

```python
def list_supported_cities() -> list[dict[str, str | bool]]:
    return [
        {
            "slug": "kyoto",
            "nameZh": "京都",
            "countryRegion": "日本",
            "isSupported": True,
            "contentDepth": "core",
            "toneSummary": "安静、古典、适合旅行前慢慢进入的城市",
        },
        {
            "slug": "tokyo",
            "nameZh": "东京",
            "countryRegion": "日本",
            "isSupported": True,
            "contentDepth": "core",
            "toneSummary": "孤独、夜晚、现代都市与日常缝隙",
        },
    ]
```

- [ ] **Step 3: 写入城市 router**

Create `D:\codex.files\git-test\weizhi-app\backend\app\features\cities\router.py`:

```python
from fastapi import APIRouter

from app.features.cities.repository import list_supported_cities

router = APIRouter(prefix="/api/cities", tags=["cities"])


@router.get("")
def get_supported_cities() -> list[dict[str, str | bool]]:
    return list_supported_cities()
```

- [ ] **Step 4: 注册 router**

Modify `D:\codex.files\git-test\weizhi-app\backend\app\main.py`:

```python
from fastapi import FastAPI

from app.features.cities.router import router as cities_router

app = FastAPI(title="Weizhi API")
app.include_router(cities_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
```

- [ ] **Step 5: 运行测试**

Run:

```powershell
Set-Location 'D:\codex.files\git-test\weizhi-app\backend'
python -m pytest
```

Expected: cities API test passes.

- [ ] **Step 6: Commit**

Run:

```powershell
git add weizhi-app/backend/app/features/cities weizhi-app/backend/app/main.py weizhi-app/backend/tests/test_cities_api.py
git commit -m "feat: expose supported cities api"
```

Expected: commit succeeds.

---

## Task 7: 实现前端首页浏览第一切片

**Files:**
- Modify: `D:\codex.files\git-test\weizhi-app\frontend\src\app\page.tsx`
- Create: `D:\codex.files\git-test\weizhi-app\frontend\src\features\home\types.ts`
- Create: `D:\codex.files\git-test\weizhi-app\frontend\src\features\home\api.ts`
- Create: `D:\codex.files\git-test\weizhi-app\frontend\src\features\home\HomePage.tsx`

- [ ] **Step 1: 写入首页类型**

Create `D:\codex.files\git-test\weizhi-app\frontend\src\features\home\types.ts`:

```ts
export type CitySummary = {
  slug: string;
  nameZh: string;
  countryRegion: string;
  isSupported: boolean;
  contentDepth: "core" | "expansion" | "unsupported";
  toneSummary: string;
};
```

- [ ] **Step 2: 写入首页 API**

Create `D:\codex.files\git-test\weizhi-app\frontend\src\features\home\api.ts`:

```ts
import { apiGet } from "@/lib/api/client";
import type { CitySummary } from "./types";

export function getSupportedCities(): Promise<CitySummary[]> {
  return apiGet<CitySummary[]>("/api/cities");
}
```

- [ ] **Step 3: 写入首页组件**

Create `D:\codex.files\git-test\weizhi-app\frontend\src\features\home\HomePage.tsx`:

```tsx
import type { CitySummary } from "./types";

const themeTags = ["安静", "怀旧", "人文", "电影感", "城市漫游"];

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
          <p className="text-base leading-7 text-neutral-700">
            出发之前，先进入一座城市。
          </p>
        </header>

        <form className="rounded-2xl border border-neutral-200 bg-white p-3 shadow-sm">
          <label className="block text-sm font-medium text-neutral-700" htmlFor="city-search">
            你想先进入哪座城市？
          </label>
          <div className="mt-3 flex gap-2">
            <input
              id="city-search"
              className="min-h-12 flex-1 rounded-xl border border-neutral-200 px-4 text-base outline-none focus:border-neutral-900"
              placeholder="搜索京都、东京、台北"
            />
            <button className="min-h-12 rounded-xl bg-neutral-950 px-4 text-sm font-medium text-white" type="submit">
              搜索
            </button>
          </div>
        </form>

        <section className="space-y-3">
          <h2 className="text-base font-semibold">主题气质</h2>
          <div className="flex flex-wrap gap-2">
            {themeTags.map((tag) => (
              <button
                className="min-h-11 rounded-full border border-neutral-200 bg-white px-4 text-sm text-neutral-700"
                key={tag}
                type="button"
              >
                {tag}
              </button>
            ))}
          </div>
        </section>

        <section className="space-y-3">
          <h2 className="text-base font-semibold">精选城市</h2>
          <div className="grid gap-3">
            {cities.map((city) => (
              <article className="rounded-2xl border border-neutral-200 bg-white p-4" key={city.slug}>
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <h3 className="text-lg font-semibold">{city.nameZh}</h3>
                    <p className="mt-1 text-sm leading-6 text-neutral-600">{city.toneSummary}</p>
                  </div>
                  <span className="rounded-full bg-neutral-100 px-3 py-1 text-xs text-neutral-600">
                    {city.contentDepth === "core" ? "核心" : "扩展"}
                  </span>
                </div>
              </article>
            ))}
          </div>
        </section>
      </section>
    </main>
  );
}
```

- [ ] **Step 4: 接入首页路由**

Modify `D:\codex.files\git-test\weizhi-app\frontend\src\app\page.tsx`:

```tsx
import { getSupportedCities } from "@/features/home/api";
import { HomePage } from "@/features/home/HomePage";

export default async function Page() {
  const cities = await getSupportedCities();

  return <HomePage cities={cities} />;
}
```

- [ ] **Step 5: 运行前端检查**

Run:

```powershell
Set-Location 'D:\codex.files\git-test\weizhi-app\frontend'
npm run lint
npm run build
```

Expected: lint and build pass when backend URL is reachable or mocked in the build environment.

- [ ] **Step 6: Commit**

Run:

```powershell
git add weizhi-app/frontend/src
git commit -m "feat: add home content browsing slice"
```

Expected: commit succeeds.

---

## Task 8: 后续切片计划拆分

**Files:**
- Create: `D:\codex.files\git-test\docs\superpowers\plans\2026-05-02-weizhi-slice-backlog.md`

- [ ] **Step 1: 创建后续切片清单**

Create `D:\codex.files\git-test\docs\superpowers\plans\2026-05-02-weizhi-slice-backlog.md`:

```markdown
# 未至后续功能切片清单

## Slice 2: 城市结果页

- 后端：`GET /api/cities/{city_slug}/recommendations`
- 前端：`/city/[slug]`
- 验收：用户从首页进入京都结果页，看到主题气质分组和作品卡片。

## Slice 3: 作品详情与地点触点

- 后端：`GET /api/works/{work_slug}`、`GET /api/places/{place_slug}`
- 前端：`/works/[slug]`、`/places/[slug]`
- 验收：用户能从作品进入地点，并返回相关作品。

## Slice 4: 登录与收藏

- 后端：收藏读写接口和 Supabase JWT 校验。
- 前端：登录弹窗、收藏按钮状态。
- 验收：未登录点击收藏弹出登录，登录后自动完成收藏。

## Slice 5: 收藏准备册

- 后端：按城市聚合用户收藏。
- 前端：`/collections`
- 验收：用户按城市查看收藏作品和地点。

## Slice 6: mimoaiapi 推荐

- 后端：AI Provider、推荐结构校验、数据库缓存。
- 前端：推荐生成中、失败回退、缓存命中状态。
- 验收：常见组合读取缓存，非常规组合生成后缓存。

## Slice 7: 上线质量

- 移动端适配。
- 加载、错误、空状态。
- PWA metadata。
- 部署环境变量。
- smoke test。
```

- [ ] **Step 2: Commit**

Run:

```powershell
git add docs/superpowers/plans/2026-05-02-weizhi-slice-backlog.md
git commit -m "docs: add weizhi slice backlog"
```

Expected: commit succeeds.

---

## Self-Review

Spec coverage:

- 产品定位：由产品 spec 覆盖，实施从首页和城市浏览切片开始。
- 技术架构：由技术架构记录覆盖，本计划使用 Next.js、FastAPI、Supabase、mimoaiapi。
- 文件组织：本计划明确 `frontend/`、`backend/`、`content/`。
- 功能切片：本计划先落地基础骨架、数据 schema、CSV 模板、城市 API、首页浏览。
- AI：本计划只定义 provider 边界和后续切片，不在第一批任务直接调用 mimoaiapi。
- UI：本计划首页示例遵守现代城市笔记感，不参考外部图片视觉。

Type consistency:

- 前端 `CitySummary` 字段使用 camelCase。
- 后端第一批临时 API 返回 camelCase，匹配前端类型。
- 数据库 schema 使用 snake_case，后续 repository 层负责转换。

Verification:

- 每个任务都有对应命令。
- 第一批切片完成后，用户可以看到首页从后端 API 读取城市数据。
