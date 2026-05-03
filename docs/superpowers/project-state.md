# 未至项目状态

更新时间：2026-05-02

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

- 待提交

## 最近验证结果

最近一次总体验证：

- 后端测试：`11 passed in 0.76s`
- 前端 lint：通过
- 前端 build：通过
- Git 工作区：干净
- 3000 端口：未占用
- 8000 端口：未占用
- 没有残留的项目 `node/npm/python` 进程

注意：

- 前端 build 在当前 Windows 环境中可能因为 `.next` 文件写入权限失败，需要提升权限运行。
- 后端 pytest 使用 `-p no:cacheprovider`，避免 pytest cache 在 Windows 权限下产生 warning 或挂起。

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

建议进入 UI/UX 稿阶段，而不是继续直接写城市结果页代码。

应先产出：

- 首页 UX/UI 稿。
- 城市结果页 UX/UI 稿。
- 作品详情页 UX/UI 稿。
- 地点详情页 UX/UI 稿。
- 收藏准备册 UX/UI 稿。

形式建议：

- 先做本地 HTML 低/中保真视觉稿。
- 确认信息架构、布局节奏和现代城市笔记感。
- 再继续实现 Slice 2 城市结果页。

后续功能切片：

1. 城市结果页。
2. 作品详情与地点触点。
3. 登录与收藏。
4. 收藏准备册。
5. mimoaiapi 推荐。
6. 上线质量。
