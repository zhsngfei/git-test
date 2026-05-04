# 未至项目重装 Codex 后续接说明

更新时间：2026-05-04

## 给新装 Codex 的第一句话

把下面这段复制给新装后的 Codex：

```text
请继续未至项目。项目目录是 D:\codex.files\git-test。
请先阅读：
1. docs/superpowers/resume-after-reinstall.md
2. docs/superpowers/project-state.md
3. docs/superpowers/specs/2026-04-29-weizhi-product-design.md
4. docs/superpowers/specs/2026-05-02-weizhi-technical-architecture.md
5. docs/superpowers/plans/2026-05-02-weizhi-slice-backlog.md

请用中文回复。继续遵守：按功能切片推进；适当使用 skills 和 subagent；创建文件后明确告诉我文件路径；不要参考旧 DESIGN.md、旧 prototype 或旧项目产物。
```

## 本机项目位置

项目目录：

```text
D:\codex.files\git-test
```

核心项目目录：

```text
D:\codex.files\git-test\weizhi-app
```

请在卸载或重装 Codex 前备份整个目录：

```text
D:\codex.files\git-test
```

建议备份到类似：

```text
D:\backups\git-test-weizhi-2026-05-04
```

## Git 状态

当前分支：

```text
main
```

远程仓库：

```text
origin https://github.com/zhsngfei/git-test.git
```

最近关键提交：

```text
a16707c chore: harden app launch readiness
ae27e41 feat: add controlled city recommendations
da51576 feat: add collections preparation book
cc40285 feat: add login-gated collections
b2a7c69 feat: add work and place detail pages
101faca feat: add city recommendations page
f857f8e chore: remove mood tag concept
```

注意：

- `.codex-tmp/` 是临时 UI 参考图压缩目录，不属于未至项目代码，不需要提交。
- 真正的项目记忆在 `docs/superpowers/` 和 `weizhi-app/` 中。

## 当前产品定位

未至是一款移动优先 Web App / PWA，用于旅行前文化准备。

第一版范围：

- 用户搜索或进入城市。
- 浏览城市关联书籍、电影和地点触点。
- 作品和地点可收藏。
- 收藏页按城市组织成出发前准备册。
- AI 只基于已核验资料排序、分组、解释，不编造事实。

第一版不做：

- 地图、路线、餐厅、酒店、机票、打卡。
- 想读/想看独立系统。
- 社区。
- 旧搜索细分类，例如安静、怀旧、主题气质等。

## 技术栈

- 前端：Next.js、TypeScript、Tailwind CSS v4。
- 后端：FastAPI、Pydantic、pytest。
- 数据库和登录：Supabase PostgreSQL/Auth。
- AI：统一标记为 `mimoaiapi`。
- 部署：前端 Vercel，后端独立部署，数据库 Supabase。

## 已完成进度

已完成：

- 干净项目目录 `weizhi-app/`。
- 前端 Next.js 初始化。
- 后端 FastAPI 初始化。
- 数据 schema、CSV/Excel 模板和导入校验。
- 城市 API。
- 首页内容浏览。
- 城市结果页 `/city/[slug]`。
- 作品详情页 `/works/[slug]`。
- 地点详情页 `/places/[slug]`。
- 登录与收藏第一切片。
- 收藏准备册 `/collections`。
- `mimoaiapi` 推荐第一切片。
- 上线质量第一切片：PWA metadata、manifest、图标、loading、error、404、CORS、health、deployment 文档。

## 最近验证结果

最近一次完整验证：

```text
后端：19 passed in 0.72s
前端：npm run lint 通过
前端：npx tsc --noEmit 通过
前端：npm run build 通过
旧搜索细分类残留检查：无输出
3000 / 8000 端口：未占用
python/node 项目进程：无残留
```

注意：

- 当前 Windows 环境普通权限运行 `npm run build` 可能遇到 `.next` 写入 EPERM，需要提升权限运行构建。
- 构建前如果页面需要后端数据，应临时启动 FastAPI 后端在 `127.0.0.1:8000`，构建后关闭。

## 常用验证命令

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

端口检查：

```powershell
netstat -ano | Select-String ':3000|:8000'
```

旧搜索细分类残留检查：

```powershell
$oldTerms = @("theme" + "_tags", "theme" + "Tags", "安" + "静", "怀" + "旧", "主题" + "气质", "电影" + "感", "文学" + "感", "城市" + "漫游")
Get-ChildItem -Recurse -File "weizhi-app\backend\app","weizhi-app\frontend\src","weizhi-app\content","docs\superpowers\specs","docs\superpowers\plans" |
  Select-String -Pattern $oldTerms -SimpleMatch
```

## 下一步建议

重装 Codex 后，建议不要立刻改 UI。下一步进入真实上线前的收口阶段：

1. 接入 Supabase Auth，替换当前临时本地登录和 `X-Weizhi-User-Id`。
2. 将内存/临时数据源替换为 Supabase PostgreSQL 查询。
3. 接入真实 `mimoaiapi`，保留“只基于已核验事实推荐”的约束。
4. 功能闭环稳定后，再进入 UI/UX 视觉专项微调。

## 重装后的交接流程

1. 安装新的 Codex 到 D 盘。
2. 打开项目目录 `D:\codex.files\git-test`。
3. 确认 git 状态：

```powershell
git status --short
git log --oneline -5
```

4. 把“给新装 Codex 的第一句话”复制给 Codex。
5. 让 Codex 先总结它读到的项目状态，不要直接写代码。
6. 确认总结无误后，再继续下一切片。

## 不要删除的内容

卸载 Codex 前不要删除：

- `D:\codex.files\git-test`
- `D:\codex.files\git-test\.git`
- `D:\codex.files\git-test\weizhi-app`
- `D:\codex.files\git-test\docs\superpowers`

如果 C 盘 Codex 缓存很大，可以在确认 D 盘新 Codex 能打开项目并读到这些文档后，再清理旧缓存。
