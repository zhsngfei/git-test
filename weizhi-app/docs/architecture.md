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
