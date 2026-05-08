# 未至 Supabase 接入说明

更新时间：2026-05-08

## 目标

这一页用于真正接入 Supabase 项目时交接配置。当前代码已经完成 Supabase Auth 与收藏持久化的边界，但还没有连接你的真实 Supabase 项目。

本阶段不需要你的 Supabase 账号密码。需要的是项目级配置值，且 secret 只能放在本地或部署平台的环境变量里，不能提交到 Git。

## 需要你准备的值

前端需要：

```dotenv
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```

后端需要：

```dotenv
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_JWT_SECRET=
```

说明：

- `NEXT_PUBLIC_SUPABASE_URL` / `SUPABASE_URL` 是同一个 Supabase 项目 URL。
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` 是前端公开 key。Supabase 新项目也可能提供 publishable key；前端可以使用公开 key，但要保证数据表启用 RLS。
- `SUPABASE_SERVICE_ROLE_KEY` 只能放后端，不能进入浏览器、前端代码、聊天截图或 Git。
- `SUPABASE_JWT_SECRET` 用于后端验证 Supabase Auth 发出的用户 access token。

## 本地文件位置

前端本地环境文件：

```text
D:\codex.files\git-test\weizhi-app\frontend\.env.local
```

内容：

```dotenv
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=你的 Supabase Project URL
NEXT_PUBLIC_SUPABASE_ANON_KEY=你的 Supabase 前端公开 key
```

后端本地环境文件：

```text
D:\codex.files\git-test\weizhi-app\backend\.env
```

内容：

```dotenv
APP_ENV=staging
FRONTEND_ORIGIN=http://localhost:3000
SUPABASE_URL=你的 Supabase Project URL
SUPABASE_SERVICE_ROLE_KEY=你的 Supabase service_role key
SUPABASE_JWT_SECRET=你的 Supabase JWT secret
MIMOAI_API_BASE_URL=https://api.example.com
MIMOAI_API_KEY=replace-with-mimoai-key
```

为什么本地联调用 `APP_ENV=staging`：

- `APP_ENV=local` 时，后端收藏仓库使用内存存储，适合跑自动化测试。
- `APP_ENV=staging` 时，后端会拒绝占位密钥，并使用 Supabase REST 写入真实 `collections` 表。

## Supabase 项目设置

1. 创建或打开你的 Supabase 项目。
2. 在项目设置中找到 API / API Keys 页面，复制 Project URL、前端公开 key、service_role key。
3. 找到 JWT secret。它只给后端使用。
4. 在 Authentication 的邮件登录配置中启用 Email OTP / magic link。
5. 上线前，把生产前端域名加入 Auth Redirect URLs / Site URL。

安全原则：

- 前端只放公开 key。
- 后端只放 service role key 和 JWT secret。
- `.env`、`.env.local` 不提交到 Git。
- `collections` 表必须开启 RLS，即使当前后端通过 service role 写入，也要防止前端公开 key 被误用时越权读取。

## 数据库 schema

如果是全新的 Supabase 项目，执行：

```text
D:\codex.files\git-test\weizhi-app\backend\app\db\schema.sql
```

如果项目里已经有旧版 `collections` 表，先执行迁移：

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

然后执行 `schema.sql` 里与 `collections` RLS policy 相关的语句。

## 本地联调顺序

1. 填写 `frontend\.env.local`。
2. 填写 `backend\.env`。
3. 在 Supabase SQL Editor 执行 schema。
4. 启动后端：

```powershell
cd D:\codex.files\git-test\weizhi-app\backend
.\.venv\Scripts\uvicorn.exe app.main:app --reload --port 8000
```

5. 启动前端：

```powershell
cd D:\codex.files\git-test\weizhi-app\frontend
npm run dev
```

6. 手动验证：

- 打开首页。
- 进入作品或地点详情。
- 点击收藏。
- 用邮箱验证码登录。
- 收藏后进入 `/collections`。
- 在 Supabase `collections` 表中确认出现对应记录。

## 当前还没做的事

- 还没有拿到你的真实 Supabase 项目配置。
- 还没有在真实 Supabase 项目里执行 schema。
- 还没有跑真实邮箱 OTP 登录的端到端验证。
- 还没有把 Supabase 生产环境变量配置到 Vercel 和后端部署平台。
- Supabase 新 key 体系推荐 publishable / secret key；当前代码仍按 `anon` / `service_role` / `JWT secret` 边界实现，后续上线前需要再确认你的项目 key 类型并决定是否升级命名和后端调用方式。
