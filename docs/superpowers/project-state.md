# 未至项目状态

更新时间：2026-05-04

## 当前目标

未至第一版要做成可真实上线使用的移动优先 Web App / PWA。

产品核心：

- 旅行前文化准备应用。
- 用户搜索城市，浏览书籍、电影和地点触点。
- 应用基于真实资料库展示书籍、电影和地点触点。
- AI 只负责排序、分组和推荐解释，不编造事实。
- 用户登录后可以收藏作品和地点。

## 关键产品约束

- UI/UX 采用现代城市笔记感。
- 不做旧报纸、旧书、复古泛黄风。
- 不参考旧项目视觉。
- 不参考外部截图里的 UI 视觉，只参考过其技术栈建议。
- 前台不展示来源，但后台事实必须可追溯。
- 第一版正式支持书籍和电影，数据模型预留剧集。
- 第一版不做地图、路线、餐厅、酒店、机票、打卡、想读/想看、社区。
- 收藏统一为作品收藏和地点收藏，收藏页按城市组织为出发前准备册。
- 登录方式为邮箱 magic link 或邮箱验证码。

## 技术栈决策

- 前端：Next.js。
- UI：Tailwind CSS v4 + shadcn/ui。
- 后端：FastAPI。
- 数据库：Supabase PostgreSQL。
- 登录：Supabase Auth。
- AI：统一标记为 `mimoaiapi`。
- 缓存：第一阶段使用数据库缓存，Redis 预留。
- 内容导入：CSV/Excel -> FastAPI 导入逻辑 -> PostgreSQL。
- 部署：前端 Vercel，后端独立部署，数据库 Supabase。

## 已完成文档

- `docs/superpowers/specs/2026-04-29-weizhi-product-design.md`
  - 中文产品设计说明。
- `docs/superpowers/specs/2026-05-02-weizhi-technical-architecture.md`
  - 中文技术架构决策记录。
- `docs/superpowers/plans/2026-05-02-weizhi-app-implementation-plan.md`
  - 第一版功能切片实施计划。
- `docs/superpowers/plans/2026-05-02-weizhi-slice-backlog.md`
  - 后续功能切片清单。

## 已完成代码任务

### Task 1: 项目工作区

已创建：

- `weizhi-app/README.md`
- `weizhi-app/.gitignore`
- `weizhi-app/docs/architecture.md`

提交：

- `c7fb650 chore: create weizhi app workspace`

### Task 2: 前端初始化

已创建 Next.js 前端：

- `weizhi-app/frontend/`
- `weizhi-app/frontend/.env.example`
- `weizhi-app/frontend/src/lib/api/client.ts`
- `weizhi-app/frontend/src/components/*/.gitkeep`
- `weizhi-app/frontend/src/features/*/.gitkeep`
- `weizhi-app/frontend/src/lib/auth/.gitkeep`
- `weizhi-app/frontend/src/lib/constants/.gitkeep`

提交：

- `a2f4b50 chore: initialize weizhi frontend`
- `608b193 chore: track frontend structure placeholders`

### Task 3: 后端初始化

已创建 FastAPI 后端：

- `weizhi-app/backend/.env.example`
- `weizhi-app/backend/pyproject.toml`
- `weizhi-app/backend/app/core/config.py`
- `weizhi-app/backend/app/main.py`
- `weizhi-app/backend/tests/test_health.py`

提交：

- `af1636e chore: initialize weizhi backend`

### Task 4: 数据 schema 和核心类型

已创建：

- `weizhi-app/backend/app/db/schema.sql`
- `weizhi-app/backend/app/schemas/content.py`
- `weizhi-app/backend/tests/test_content_schema.py`

提交：

- `2ba010e feat: define content data schema`

### Task 5: CSV/Excel 内容模板和导入校验

已创建：

- `weizhi-app/content/templates/cities.csv`
- `weizhi-app/content/templates/works.csv`
- `weizhi-app/content/templates/places.csv`
- `weizhi-app/content/templates/work_city_relations.csv`
- `weizhi-app/content/templates/work_place_relations.csv`
- `weizhi-app/backend/app/features/content_import/validator.py`
- `weizhi-app/backend/tests/test_content_import_validator.py`

提交：

- `e95264e feat: add content import templates`

### Task 6: 城市 API 第一切片

已创建/修改：

- `weizhi-app/backend/app/features/cities/repository.py`
- `weizhi-app/backend/app/features/cities/router.py`
- `weizhi-app/backend/app/main.py`
- `weizhi-app/backend/tests/test_cities_api.py`

提交：

- `8678014 feat: expose supported cities api`

### Task 7: 首页浏览第一切片

已创建/修改：

- `weizhi-app/frontend/src/features/home/types.ts`
- `weizhi-app/frontend/src/features/home/api.ts`
- `weizhi-app/frontend/src/features/home/HomePage.tsx`
- `weizhi-app/frontend/src/app/page.tsx`
- `weizhi-app/frontend/src/app/layout.tsx`
- `weizhi-app/frontend/src/app/globals.css`

说明：

- 移除 Next.js 默认 Google Fonts，避免构建时访问 Google Fonts 失败。
- 首页现在从后端 `/api/cities` 获取城市数据。
- UI 只是最小功能切片，不是最终 UI/UX 稿。

提交：

- `efdd60d feat: add home content browsing slice`

### Task 8: 后续切片清单

已创建：

- `docs/superpowers/plans/2026-05-02-weizhi-slice-backlog.md`

提交：

- `28e7209 docs: add weizhi slice backlog`

### Task 9: 城市结果页第一切片

已创建/修改：

- `weizhi-app/backend/app/features/cities/repository.py`
- `weizhi-app/backend/app/features/cities/router.py`
- `weizhi-app/backend/tests/test_cities_api.py`
- `weizhi-app/frontend/src/features/city/types.ts`
- `weizhi-app/frontend/src/features/city/api.ts`
- `weizhi-app/frontend/src/features/city/CityPage.tsx`
- `weizhi-app/frontend/src/app/city/[slug]/page.tsx`
- `weizhi-app/frontend/src/features/home/HomePage.tsx`

说明：

- 后端新增 `GET /api/cities/{city_slug}/recommendations`。
- 前端新增 `/city/[slug]` 城市结果页。
- 首页精选城市卡片可进入对应城市结果页。
- 页面不包含搜索细分类入口。

提交：

- `101faca feat: add city recommendations page`

### Task 10: 作品详情与地点触点第一切片

已创建/修改：

- `weizhi-app/backend/app/features/works/repository.py`
- `weizhi-app/backend/app/features/works/router.py`
- `weizhi-app/backend/app/features/places/repository.py`
- `weizhi-app/backend/app/features/places/router.py`
- `weizhi-app/backend/app/main.py`
- `weizhi-app/backend/tests/test_works_api.py`
- `weizhi-app/backend/tests/test_places_api.py`
- `weizhi-app/frontend/src/features/works/types.ts`
- `weizhi-app/frontend/src/features/works/api.ts`
- `weizhi-app/frontend/src/features/works/WorkDetailPage.tsx`
- `weizhi-app/frontend/src/app/works/[slug]/page.tsx`
- `weizhi-app/frontend/src/features/places/types.ts`
- `weizhi-app/frontend/src/features/places/api.ts`
- `weizhi-app/frontend/src/features/places/PlaceDetailPage.tsx`
- `weizhi-app/frontend/src/app/places/[slug]/page.tsx`
- `weizhi-app/frontend/src/features/city/CityPage.tsx`

说明：

- 后端新增 `GET /api/works/{work_slug}`。
- 后端新增 `GET /api/places/{place_slug}`。
- 前端新增 `/works/[slug]` 作品详情页。
- 前端新增 `/places/[slug]` 地点详情页。
- 城市结果页作品卡片和地点卡片可以进入详情页。
- 收藏按钮为静态入口，真实登录收藏下一切片实现。

提交：

- `b2a7c69 feat: add work and place detail pages`

### Task 11: 登录与收藏第一切片

已创建/修改：

- `weizhi-app/backend/app/features/collections/schemas.py`
- `weizhi-app/backend/app/features/collections/repository.py`
- `weizhi-app/backend/app/features/collections/router.py`
- `weizhi-app/backend/app/main.py`
- `weizhi-app/backend/tests/test_collections_api.py`
- `weizhi-app/frontend/src/features/auth/AuthDialog.tsx`
- `weizhi-app/frontend/src/features/auth/localSession.ts`
- `weizhi-app/frontend/src/features/collections/types.ts`
- `weizhi-app/frontend/src/features/collections/api.ts`
- `weizhi-app/frontend/src/features/collections/CollectionButton.tsx`
- `weizhi-app/frontend/src/features/works/WorkDetailPage.tsx`
- `weizhi-app/frontend/src/features/places/PlaceDetailPage.tsx`

说明：

- 后端新增 `GET /api/collections`。
- 后端新增 `POST /api/collections`。
- 后端新增 `DELETE /api/collections/{entity_type}/{entity_id}`。
- 后端暂用 `X-Weizhi-User-Id` 表示当前用户，后续替换为 Supabase JWT 校验。
- 前端作品和地点详情页收藏按钮会在未登录时打开登录弹窗。
- 登录弹窗本阶段记录邮箱，并用当前设备状态模拟登录与收藏。

提交：

- `cc40285 feat: add login-gated collections`

### Task 12: 收藏准备册第一切片

已创建/修改：

- `weizhi-app/backend/app/features/collections/schemas.py`
- `weizhi-app/backend/app/features/collections/repository.py`
- `weizhi-app/backend/app/features/collections/router.py`
- `weizhi-app/backend/tests/test_collections_api.py`
- `weizhi-app/frontend/src/features/collections/types.ts`
- `weizhi-app/frontend/src/features/collections/api.ts`
- `weizhi-app/frontend/src/features/collections/CollectionButton.tsx`
- `weizhi-app/frontend/src/features/collections/CollectionsPage.tsx`
- `weizhi-app/frontend/src/app/collections/page.tsx`
- `weizhi-app/frontend/src/features/city/CityPage.tsx`
- `weizhi-app/frontend/src/features/works/WorkDetailPage.tsx`
- `weizhi-app/frontend/src/features/places/PlaceDetailPage.tsx`

说明：

- 后端新增 `GET /api/collections/preparation`。
- 收藏准备册按城市聚合收藏作品和地点。
- 前端新增 `/collections` 页面。
- 收藏页未登录时显示登录入口，登录后读取当前用户收藏准备册。
- 城市页、作品页和地点页底部导航的“收藏”可以进入收藏准备册。

提交：

- `da51576 feat: add collections preparation book`

### Task 13: mimoaiapi 推荐第一切片

已创建/修改：

- `weizhi-app/backend/app/features/recommendations/schemas.py`
- `weizhi-app/backend/app/features/recommendations/provider.py`
- `weizhi-app/backend/app/features/recommendations/service.py`
- `weizhi-app/backend/app/features/recommendations/router.py`
- `weizhi-app/backend/app/main.py`
- `weizhi-app/backend/tests/test_recommendations_api.py`
- `weizhi-app/frontend/src/features/recommendations/types.ts`
- `weizhi-app/frontend/src/features/recommendations/api.ts`
- `weizhi-app/frontend/src/features/recommendations/RecommendationStatus.tsx`
- `weizhi-app/frontend/src/features/city/CityPage.tsx`

说明：

- 后端新增 `POST /api/recommendations/city`。
- 推荐响应包含 `cached/generated/fallback` 状态。
- 第一阶段 provider 使用已核验内容生成结构化推荐分组，保留 `mimoaiapi` 接入边界。
- 同请求会命中内存缓存。
- 未知城市或无内容时返回回退推荐，不编造作品或地点。
- 前端城市页展示推荐状态和推荐分组概览。

提交：

- `ae27e41 feat: add controlled city recommendations`

### Task 14: 上线质量第一切片

已创建/修改：

- `weizhi-app/frontend/src/app/layout.tsx`
- `weizhi-app/frontend/src/app/manifest.ts`
- `weizhi-app/frontend/src/app/loading.tsx`
- `weizhi-app/frontend/src/app/error.tsx`
- `weizhi-app/frontend/src/app/not-found.tsx`
- `weizhi-app/frontend/public/icons/icon-192.png`
- `weizhi-app/frontend/public/icons/icon-512.png`
- `weizhi-app/frontend/public/icons/icon-maskable-512.png`
- `weizhi-app/backend/.env.example`
- `weizhi-app/backend/app/core/config.py`
- `weizhi-app/backend/app/main.py`
- `weizhi-app/backend/tests/test_health.py`
- `weizhi-app/docs/deployment.md`

说明：

- 前端新增 PWA metadata、manifest、全局 loading、全局错误页和 404 页面。
- 前端新增 192/512/maskable PWA PNG 图标，避免只依赖 favicon。
- 后端新增 `FRONTEND_ORIGIN` 配置和 CORS 中间件。
- `GET /health` 现在返回 `status` 和 `appEnv`，用于上线 smoke test。
- 后端配置在本地允许占位值，非本地环境会拒绝占位 secret，避免生产环境误启动。
- 新增上线准备说明，集中记录环境变量、验证命令和 smoke test。

提交：

- 本切片提交：`chore: harden app launch readiness`

### Task 15: Supabase Auth 与收藏持久化边界第一切片

已创建/修改：

- `weizhi-app/frontend/package.json`
- `weizhi-app/frontend/package-lock.json`
- `weizhi-app/frontend/src/features/auth/AuthDialog.tsx`
- `weizhi-app/frontend/src/features/auth/supabaseClient.ts`
- `weizhi-app/frontend/src/features/auth/session.ts`
- `weizhi-app/frontend/src/features/auth/localSession.ts`
- `weizhi-app/frontend/src/features/collections/api.ts`
- `weizhi-app/frontend/src/features/collections/CollectionButton.tsx`
- `weizhi-app/frontend/src/features/collections/CollectionsPage.tsx`
- `weizhi-app/backend/pyproject.toml`
- `weizhi-app/backend/.env.example`
- `weizhi-app/backend/app/core/config.py`
- `weizhi-app/backend/app/db/schema.sql`
- `weizhi-app/backend/app/features/auth/dependencies.py`
- `weizhi-app/backend/app/features/collections/router.py`
- `weizhi-app/backend/app/features/collections/repository.py`
- `weizhi-app/backend/tests/test_collections_api.py`
- `weizhi-app/backend/tests/test_collections_repository.py`
- `weizhi-app/docs/deployment.md`

说明：

- 前端安装 `@supabase/supabase-js`，位置为 `weizhi-app/frontend/node_modules/@supabase`，安装后 `node_modules` 约增加 6.81 MB。
- 后端安装 `PyJWT`，位置为 `weizhi-app/backend/.venv/Lib/site-packages`，安装后 `.venv` 约增加 0.21 MB。
- 前端登录弹窗从模拟邮箱登录改为 Supabase 邮箱 OTP：发送验证码并验证验证码。
- 前端收藏 API 改为发送 `Authorization: Bearer <Supabase access_token>`。
- 前端收藏按钮和收藏页不再读取 `localSession` 或传递 `userId`。
- 后端收藏接口不再接受 `X-Weizhi-User-Id`，统一通过 Bearer JWT 提取用户身份。
- JWT 校验要求 `exp`、`iss`、`aud`、`sub`，并要求 `role=authenticated`。
- 非本地环境收藏仓储会通过 Supabase REST 写入/读取/删除 `collections` 表；本地测试仍使用内存仓储。
- 数据库 schema 将 `collections.entity_id` 调整为文本 id，将 `city_id` 调整为 `city_slug`，匹配当前内容 slug 和收藏 API。
- 数据库 schema 为 `collections` 启用 RLS，并添加用户只能读写自己收藏的 policies。
- 部署文档补充了旧版 `collections` 表的迁移说明。

提交：

- `3b59a00 feat: add supabase auth collections boundary`

### Task 16: Supabase 真实接入准备说明

已创建/修改：

- `weizhi-app/docs/supabase-setup.md`
- `weizhi-app/docs/deployment.md`
- `docs/superpowers/project-state.md`

说明：

- 新增 Supabase 接入说明，记录真实项目需要提供的前端公开 key、后端 service role key、JWT secret 和本地文件位置。
- 明确不需要用户提供 Supabase 账号密码；只需要项目配置值，且 secret 不能提交到 Git。
- 明确本地真实联调需要使用 `APP_ENV=staging`，因为 `APP_ENV=local` 会继续使用内存收藏仓储。
- 部署文档新增 Supabase setup 文档入口和 secret 安全提醒。
- 当前还没有执行真实 Supabase smoke test，因为真实项目配置尚未提供。

提交：

- `6af519e docs: add supabase setup guide`

### Task 17: 上线配置就绪状态接口

已创建/修改：

- `weizhi-app/backend/app/core/config.py`
- `weizhi-app/backend/app/main.py`
- `weizhi-app/backend/tests/test_health.py`
- `weizhi-app/docs/deployment.md`
- `docs/superpowers/project-state.md`

说明：

- 新增 `GET /health/readiness`，用于上线前检查 Supabase Auth、收藏仓储和 `mimoaiapi` 的配置状态。
- 响应只返回 `placeholder`、`configured`、`memory`、`supabase_rest` 这类安全状态，不返回 URL、key、JWT secret 或 service role key。
- 本地默认状态为 Supabase Auth `placeholder`、收藏仓储 `memory`、`mimoaiapi` `placeholder`。
- 该切片不需要真实 Supabase 配置；后续填入真实配置后，可用同一接口做 smoke test。

提交：

- `f57b010 feat: expose readiness configuration status`

### Task 18: 无密钥本地登录到收藏闭环

已创建/修改：

- `weizhi-app/backend/app/features/auth/router.py`
- `weizhi-app/backend/app/main.py`
- `weizhi-app/backend/tests/test_collections_api.py`
- `weizhi-app/frontend/src/features/auth/devAuth.ts`
- `weizhi-app/frontend/src/features/auth/supabaseClient.ts`
- `weizhi-app/frontend/src/features/auth/session.ts`
- `weizhi-app/frontend/src/features/auth/AuthDialog.tsx`
- `weizhi-app/frontend/src/features/collections/CollectionButton.tsx`
- `weizhi-app/frontend/src/features/collections/CollectionsPage.tsx`
- `weizhi-app/docs/supabase-setup.md`
- `weizhi-app/docs/deployment.md`
- `docs/superpowers/project-state.md`

说明：

- 新增本地开发登录接口 `POST /api/dev/auth/session`，在 `APP_ENV=local` 时签发本地 JWT。
- 本地 dev auth token 使用和收藏接口一致的 Bearer JWT 校验链路，能验证登录态、收藏写入和准备册读取。
- 前端在 Supabase URL / key 仍为占位值时，不再误连 `example.supabase.co`，而是调用本地 dev auth endpoint。
- 本地 dev session 存在浏览器 localStorage，仅用于无密钥开发验证；真实上线仍必须配置 Supabase Auth。
- 该切片没有新增 Python 或 npm 依赖。

提交：

- 待提交

## 最近验证结果

Task 18 无密钥本地登录闭环验证：

- 后端局部测试：`tests/test_collections_api.py`，`9 passed in 0.73s`
- 后端完整测试：`28 passed in 0.93s`
- 前端 lint：通过。
- 前端 type check：`npx tsc --noEmit` 通过。
- 前端 build：`npm run build` 通过；第一次因 Windows `.next` 旧文件 unlink 权限失败，清理 `.next` 后提升权限重跑通过。

Task 17 配置就绪状态接口验证：

- 后端局部测试：`tests/test_health.py`，`4 passed in 0.53s`
- 后端完整测试：`26 passed in 0.84s`

Task 16 文档切片验证：

- 后端测试：`25 passed in 0.75s`
- 前端 lint：通过。

最近一次总体验证：

- 前端 type check：`npx tsc --noEmit` 通过。
- 前端 build：`npm run build` 通过；本机 Windows 环境使用提升权限运行。
- 旧细分类残留检查：应用源码、内容模板、产品规格和计划文档中无旧搜索细分类概念残留。
- 3000 端口：未占用。
- 8000 端口：未占用。
- 项目临时 `python/node` 进程：未残留。

注意：

- 前端 build 在当前 Windows 环境中可能因为 `.next` 文件写入权限失败，需要提升权限运行。
- 后端 pytest 使用 `-p no:cacheprovider`，避免 pytest cache 在 Windows 权限下产生 warning 或挂起。
- `npm install @supabase/supabase-js` 后 npm 报告 2 个 moderate vulnerabilities；`npm audit --audit-level=moderate` 本次运行超时，后续上线前需要单独完成依赖审计。

## 用户偏好和工作规则

- 后续默认用中文。
- 每次选择适当 skills。
- 创建文件后必须明确告诉用户文件名和位置。
- 适当时可以使用 subagent，但基础骨架阶段不滥用。
- 不随意清理或杀进程；启动预览前先检查端口。
- 如果需要停止旧 dev server，要先说明原因。
- 不继续参考旧 `DESIGN.md`、旧 `prototype/` 或旧产物。

## 端口和进程规则

启动预览前固定检查：

```powershell
netstat -ano | findstr ":3000"
netstat -ano | findstr ":8000"
```

规则：

- 3000 空闲时用于前端。
- 8000 空闲时用于 FastAPI。
- 如果端口被占用，先查 PID 和进程路径。
- 只有确认是旧项目 dev server 时，才征求用户同意后停止。
- 不确定来源时改用 3001、3002 或 8001。

## 下一步建议

完成上线质量第一切片后，建议进入真实上线前的“收口阶段”：

1. 获取并填写真实 Supabase 项目环境变量。
2. 在 Supabase 执行 schema，并验证邮箱 OTP 登录和收藏写入。
3. 将内容数据查询从当前仓储边界继续推进到 Supabase PostgreSQL。
4. 接入真实 `mimoaiapi`，保留“只基于已核验事实推荐”的约束。
5. 在功能闭环稳定后，再进入 UI/UX 视觉专项微调。
