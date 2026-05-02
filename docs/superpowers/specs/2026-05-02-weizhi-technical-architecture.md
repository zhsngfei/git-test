# 未至技术架构决策记录

## 背景

未至第一版目标是可真实上线使用的移动优先 Web App / PWA。

产品已确认的关键要求：

- 真实数据库内容。
- 邮箱 magic link 或邮箱验证码登录。
- 登录后收藏作品和地点。
- CSV/Excel 内容库导入数据库。
- AI 基于已核验内容做排序、分组和推荐解释。
- 前台不展示来源，但后台事实必须可追溯。
- UI/UX 采用现代城市笔记感，不参考旧项目或外部图片里的视觉样式。

本文记录第一版技术架构选择，用作后续实施计划依据。

## 技术栈决策

第一版采用：

```text
前端：Next.js
UI：Tailwind CSS v4 + shadcn/ui
后端：FastAPI
数据库：Supabase PostgreSQL
登录：Supabase Auth，邮箱 magic link / 邮箱验证码
AI：mimoaiapi
缓存：第一阶段使用数据库缓存，Redis 预留
内容导入：CSV/Excel -> FastAPI 导入逻辑 -> PostgreSQL
部署：前端 Vercel，后端独立部署，数据库 Supabase
```

## 架构分工

### Next.js

Next.js 负责：

- 移动优先前端应用。
- 页面路由。
- 首页、城市结果页、作品详情页、地点详情页、收藏页。
- PWA 基础能力。
- 调用 FastAPI 业务接口。
- 处理前端登录状态和收藏状态展示。

Next.js 不直接承担复杂 AI 推荐、CSV/Excel 导入和内容校验逻辑。

### Tailwind CSS v4 + shadcn/ui

Tailwind CSS v4 和 shadcn/ui 用于提升 UI 实现效率和组件一致性。

使用边界：

- 可以使用 shadcn/ui 的基础组件能力。
- 视觉设计仍然以未至产品 spec 为准。
- 不采用 shadcn 默认后台感。
- 不参考外部图片中的 UI 排版、色彩或视觉风格。
- 组件需要被重新设计成现代城市笔记感。

未至 UI/UX 继续遵循：

- 浅色现代。
- 干净留白。
- 城市照片、书封和电影剧照形成视觉层级。
- 不旧报纸。
- 不旧书。
- 不复古泛黄。
- 不做内容后台感。

### FastAPI

FastAPI 负责后端业务能力：

- 城市、作品、地点、关系数据查询。
- 城市搜索。
- 作品详情和地点详情接口。
- 收藏读写接口。
- CSV/Excel 导入。
- 内容字段校验。
- AI 推荐请求编排。
- AI 输出结构校验。
- 推荐结果缓存读写。
- 后续内部审核队列预留。

选择 FastAPI 的原因：

- Python 生态适合 CSV/Excel 处理。
- Python 生态适合 AI 调用、结构化输出校验和数据清洗。
- Pydantic 类型模型适合定义请求、响应和 AI 输出结构。
- 后端业务边界比全部放进 Next.js 更清晰。

### Supabase PostgreSQL

Supabase PostgreSQL 负责生产数据库。

用于存储：

- 城市。
- 作品。
- 地点。
- 作品与城市关系。
- 作品与地点关系。
- 图片元数据。
- 来源链接和来源备注。
- 审核状态。
- 用户收藏。
- AI 预生成和实时生成缓存。

Supabase 在第一版中定位为数据库和认证基础设施，不替代 FastAPI 业务后端。

### Supabase Auth

Supabase Auth 负责用户登录。

第一版登录方式：

- 邮箱 magic link。
- 或邮箱验证码。

第一版不做：

- 密码登录。
- 手机号登录。
- 第三方登录。

用户可以不登录浏览内容，但收藏作品或地点时必须登录。

### mimoaiapi

AI 服务统一标记为 `mimoaiapi`。

后端需要将 AI 能力封装为独立 Provider，避免业务逻辑直接绑定具体 AI 服务。

建议抽象边界：

```text
recommendation_service
  -> ai_provider
      -> mimoaiapi_client
```

AI Provider 负责：

- 接收已核验数据库事实。
- 调用 mimoaiapi。
- 返回结构化推荐结果。
- 校验输出结构。

AI Provider 不允许：

- 生成数据库之外的作品。
- 生成数据库之外的地点。
- 生成未经数据库验证的事实关系。

### 缓存

第一阶段使用数据库表缓存 AI 推荐结果。

原因：

- 降低第一版服务数量。
- 简化部署。
- 推荐缓存需要可追溯、可审核，数据库更直接。

Redis 预留但不强制第一阶段接入。

未来接入 Redis 的场景：

- AI 请求量上升。
- 需要更细的限流。
- 推荐结果短期高频读取。
- 需要后台任务状态缓存。

### 内容导入

内容维护方式：

```text
CSV/Excel -> FastAPI 导入逻辑 -> 字段校验 -> PostgreSQL
```

导入逻辑需要支持：

- 城市表。
- 作品表。
- 地点表。
- 作品-城市关系表。
- 作品-地点关系表。
- 图片字段。
- 来源字段。
- 审核状态字段。

应用运行时不直接读取 CSV/Excel。

## 文件组织原则

后续新建干净项目目录，不沿用旧 `prototype/`。

建议目录：

```text
weizhi-app/
  frontend/
    app/
    features/
    components/
    lib/
    tests/
  backend/
    app/
      api/
      features/
      services/
      models/
      schemas/
      importers/
      tests/
  content/
    csv/
    templates/
  docs/
```

前端按功能切片组织：

```text
features/
  home/
  city/
  works/
  places/
  collections/
  auth/
  recommendations/
```

后端按业务能力组织：

```text
features/
  cities/
  works/
  places/
  collections/
  recommendations/
  auth/
  content_import/
```

共享能力单独放：

```text
services/
  database
  ai_provider
  cache
  auth
  validation
```

## 开发方式

实施采用：

- 先搭最小基础骨架。
- 再按功能切片交付。
- 每个切片尽量穿过前端、后端、数据、状态和测试。
- 不按“先做所有后端，再做所有前端”的大瀑布方式。

推荐切片顺序：

1. 项目基础骨架。
2. 数据模型和 CSV/Excel 导入。
3. 内容浏览：首页、城市搜索、城市结果页。
4. 作品详情和地点触点。
5. 登录和收藏。
6. 收藏准备册。
7. mimoaiapi 推荐、缓存和兜底。
8. 上线质量、移动端体验和部署。

## 部署策略

前端：

- Vercel。

后端：

- FastAPI 独立部署。
- 可选 Render、Railway、Fly.io 或其他 Python 后端托管服务。
- 具体平台在实施计划前或部署阶段再定。

数据库和认证：

- Supabase。

## 明确不采用

第一版不采用：

- 纯静态前端。
- 旧 `prototype/` 继续改造。
- 单纯 Next.js API Routes 承担全部后端业务。
- AI 服务直接散落在页面或接口中。
- UI 参考外部图片视觉风格。

## 后续待实施计划展开

实施计划需要继续细化：

- 数据库表结构。
- CSV/Excel 字段模板。
- FastAPI 接口清单。
- 前端页面路由。
- 登录收藏流程。
- mimoaiapi Provider 接口。
- AI 输出结构。
- 推荐缓存表。
- 测试策略。
- 部署环境变量。
