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
