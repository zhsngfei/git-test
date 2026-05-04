# 未至上线准备说明

更新时间：2026-05-04

## 当前部署目标

第一版按移动优先 Web App / PWA 准备上线：

- 前端：Next.js，部署到 Vercel。
- 后端：FastAPI，独立部署。
- 数据库和登录：Supabase PostgreSQL/Auth。
- AI 服务：环境变量统一保留为 `mimoaiapi`。

## 前端环境变量

文件参考：`weizhi-app/frontend/.env.example`

```dotenv
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://example.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=replace-with-supabase-anon-key
```

说明：

- `NEXT_PUBLIC_API_BASE_URL`：前端访问 FastAPI 的基础地址。
- `NEXT_PUBLIC_SUPABASE_URL`：Supabase 项目地址。
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`：Supabase 前端匿名 key。

## 后端环境变量

文件参考：`weizhi-app/backend/.env.example`

```dotenv
APP_ENV=local
FRONTEND_ORIGIN=http://localhost:3000
SUPABASE_URL=https://example.supabase.co
SUPABASE_SERVICE_ROLE_KEY=replace-with-service-role-key
SUPABASE_JWT_SECRET=replace-with-supabase-jwt-secret-at-least-32-characters
MIMOAI_API_BASE_URL=https://api.example.com
MIMOAI_API_KEY=replace-with-mimoai-key
```

说明：

- `APP_ENV`：当前运行环境，例如 `local`、`staging`、`production`。
- `FRONTEND_ORIGIN`：允许跨域访问后端的前端域名。
- `SUPABASE_SERVICE_ROLE_KEY`：只允许存在后端环境变量中，不进入前端。
- `SUPABASE_JWT_SECRET`：后续替换临时登录头时用于 JWT 校验。
- `MIMOAI_API_BASE_URL`、`MIMOAI_API_KEY`：后续接入真实 `mimoaiapi` 时使用。

## 本地验证命令

PWA 图标文件：

- `weizhi-app/frontend/public/icons/icon-192.png`
- `weizhi-app/frontend/public/icons/icon-512.png`
- `weizhi-app/frontend/public/icons/icon-maskable-512.png`

后端：

```powershell
cd D:\codex.files\git-test\weizhi-app\backend
.\.venv\Scripts\python.exe -m pytest -p no:cacheprovider
```

前端：

```powershell
cd D:\codex.files\git-test\weizhi-app\frontend
npm run lint
npx tsc --noEmit
npm run build
```

旧细分类残留检查：

```powershell
$oldTerms = @("theme" + "_tags", "theme" + "Tags", "安" + "静", "怀" + "旧", "主题" + "气质", "电影" + "感", "文学" + "感", "城市" + "漫游")
Get-ChildItem -Recurse -File "weizhi-app\backend\app","weizhi-app\frontend\src","weizhi-app\content","docs\superpowers\specs","docs\superpowers\plans" |
  Select-String -Pattern $oldTerms -SimpleMatch
```

## Smoke Test

上线前至少检查：

- `GET /health` 返回 `status=ok` 和当前 `appEnv`。
- 从前端域名发起的 CORS preflight 可以通过。
- 首页可以打开并显示城市内容。
- `/city/tokyo` 可以打开并显示推荐分组状态。
- `/works/lost-in-translation` 可以打开作品详情。
- `/places/shinjuku` 可以打开地点详情。
- 未登录收藏时出现登录入口。
- 登录后收藏页 `/collections` 可以读取准备册。

## Supabase Schema Migration

如果 Supabase 项目中还没有表，可以直接执行：

```text
weizhi-app/backend/app/db/schema.sql
```

如果 Supabase 项目中已经存在旧版 `collections` 表，不要只重复执行 `create table if not exists`。需要先迁移字段：

```sql
alter table collections
  alter column entity_id type text using entity_id::text;

alter table collections
  add column if not exists city_slug text;

update collections
set city_slug = cities.slug
from cities
where collections.city_id = cities.id
  and collections.city_slug is null;

alter table collections
  alter column city_slug set not null;

alter table collections
  drop column if exists city_id;
```

然后再执行 schema 中的 RLS policy 部分，确保 `collections` 只允许用户访问自己的收藏。

## 当前限制

- Supabase Auth 前端和后端 JWT 边界已接入；真实运行前需要在 Supabase 项目中启用邮箱 OTP / magic link，并填入真实环境变量。
- 收藏接口已改为 `Authorization: Bearer <Supabase access_token>`；旧 `X-Weizhi-User-Id` 不再作为认证方式。
- 非本地环境下收藏仓储会使用 Supabase REST 写入 `collections` 表；本地测试仍使用内存仓储。
- 推荐 provider 已保留 `mimoaiapi` 边界，但还没有调用真实外部服务。
- UI/UX 视觉细调已暂时搁置，后续会在功能闭环稳定后进入专项微调。
