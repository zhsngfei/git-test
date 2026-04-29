# 未至 DESIGN.md

## Product

### Name

未至

### Positioning

未至是一款旅行前的文化触点推荐应用。

用户输入目的地城市和阅读/观影偏好后，获得与该城市相关的书籍、电影或剧集推荐，以及作品中涉及的景点触点。它不是传统旅游攻略，也不是纯内容推荐工具，而是帮助用户在出发前先进入一座城市的故事和情绪。

### Core Experience

页面目标不是生成长篇介绍，而是通过作品卡片、封面/剧照、景点图片、收藏状态和简短理由，让用户快速建立对这座城市的感知，并形成“我出发前想补什么、到了之后想去看什么”的完整体验。

## Target Users

* 准备出行、愿意在旅行前做一点内容补课的用户
* 对书籍、电影、剧集、城市气质和故事感有兴趣的文艺旅行者
* 不满足于标准攻略，更在意氛围、记忆点和旅行意义的用户

## Product Tone

* 安静、克制、有文学感
* 像一本旅行前翻阅的视觉笔记，而不是旅游工具后台
* 图片比大段文字更重要
* 要有沉浸感、浏览感和收藏欲

## App Structure

This should feel like a complete app, not a single result page.

Main navigation can include:

* 探索
* 收藏
* 我的

## Core Flow

1. 用户进入应用，在探索页看到搜索入口、城市灵感和推荐内容
2. 用户输入城市，或从推荐城市/主题入口进入
3. 用户选择偏好后进入城市结果页
4. 用户浏览作品卡片，并展开对应景点触点
5. 用户收藏作品、标记想读/想看
6. 用户在收藏页回看内容，形成出发前准备闭环

## Pages

### 1\. 探索页

This page combines discovery and search. It is the app's first screen and primary entry point.

Need:

* 顶部品牌区，展示“未至”的名字和一句简短品牌语
* 首屏必须有明显的城市搜索框
* 搜索框下方展示偏好选择区
* 快速筛选标签，例如文学、电影、剧集、经典、当代、治愈、人文、青春、悬疑
* 搜索确认按钮
* 推荐城市入口，例如东京、京都、巴黎、台北、香港
* 最近搜索区，空状态时展示推荐城市
* 一个主视觉推荐区，可以是本周推荐城市或主题城市
* 按主题浏览的内容入口，例如“文学感城市”“适合电影爱好者”“适合一个人旅行前看的城市”
* 推荐作品横滑卡片区
* 最近热门景点触点区

This page should make users feel:

* 即使还没搜索，也已经开始被旅行灵感吸引
* 这不是工具，而是一个有审美的内容型 app

Layout guidance:

* 搜索能力要出现在首屏，不要藏在二级页面
* 内容推荐区要在搜索模块之后出现，让用户既能主动搜索，也能被动发现
* 页面不要做成单纯搜索页，也不要做成只有内容流的发现页
* 移动端底部导航只有探索、收藏、我的三个入口

### 2\. 城市结果页

This is the core page of the app.

Need:

* 城市标题
* 一句很短的城市气质描述
* 当前偏好标签
* 结果数量
* 结果排序或筛选区
* 6-10 个作品卡片
* 一个“继续探索这个城市”的内容区

Each work card must include:

* 作品名
* 类型：书 / 电影 / 剧集
* 封面 / 海报 / 代表性剧照
* 一句话简介
* 与城市的关系
* 推荐理由
* 情绪或风格标签
* 相关景点数量
* 收藏按钮
* 想读 / 想看按钮
* 点击进入详情

Card style:

* 图片要占据明显视觉权重
* 理由区不要太长，但要足够打动人
* 卡片之间有明显层级和呼吸感

### 3\. 作品详情页

This page should make each recommendation feel complete.

Need:

* 大图展示区
* 作品名称
* 类型信息
* 简介
* 与城市关系说明
* 推荐理由
* 适合什么时候看 / 读
* 情绪标签或风格标签
* 收藏、想读 / 想看按钮
* 相关景点列表
* 相似推荐区

Each work can expand up to 10 related places.

### 4\. 景点详情页

Need:

* 景点大图
* 景点名称
* 所属城市
* 简短景点介绍
* 它在作品中的意义
* 对应作品入口
* 地图入口

If no image is available:

* still show the place
* clearly display “暂时没有图”
* keep the page visually complete with a clean placeholder area

### 5\. 收藏页

Need:

* 已收藏作品
* 已标记想读 / 想看的作品
* 可按类型筛选：书 / 电影 / 剧集
* 空状态页面

This page should feel warm and personal, not like a plain list.

### 6\. 我的页

Need:

* 用户头像占位
* 用户名占位
* 收藏数量
* 想读 / 想看数量
* 最近浏览
* 设置入口

This page does not need to be complex, but it should make the app feel complete.

## Content Rules

* 推荐结果以作品为主，不按景点做主视图
* 文案保持短句，不写大段城市介绍
* 每个作品必须清楚表达两件事：

  * 它和这座城市有什么关系
  * 为什么值得在去之前看 / 读
* 书籍必须有封面
* 影视优先展示代表性剧照；如果没有合适剧照，可使用海报或封面
* 景点优先展示图片；如果没有图片，仍然要展示景点内容，并明确标注“暂时没有图”
* 同一作品最多展示 10 个景点

## Important Interactions

* 支持单城市搜索
* 支持通过探索页进入城市页
* 支持收藏作品
* 支持标记想读 / 想看
* 支持展开和收起景点列表
* 支持从作品跳到景点，再从景点回到作品
* 支持按类型筛选收藏内容
* 支持最近搜索和最近浏览
* 如果城市可用内容较少，允许少于 6 个作品，并提示“当前这座城市可用的文化触点还比较少”

## Visual Direction

* 不要做成普通旅游 app 的蓝色攻略风格
* 不要做成冷冰冰的内容后台
* 要像一本数字化的旅行前阅读手册
* 视觉重心放在封面、剧照、景点图上
* 页面需要明显的图片区、标题区、理由区和操作区层级
* 可以使用偏胶片、纸张、城市夜色、书页、电影感的视觉语言
* 首页和结果页要足够丰富，不能只是搜索框加列表

## Empty States

Need clear empty states for:

* 没有搜索记录
* 没有收藏内容
* 城市内容较少
* 景点暂时没有图

These empty states should still look refined and on-brand.

## Boundaries

* 本次需要输出的是完整 app 的 UI 设计
* 不需要设计机票、酒店、路线规划、餐厅推荐
* 不需要设计旅行后相册、游记社区、发帖互动等后续扩展功能
