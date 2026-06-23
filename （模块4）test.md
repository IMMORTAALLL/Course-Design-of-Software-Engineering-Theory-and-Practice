# 测试报告

项目名称：智投社区：股票基金投资论坛系统

本文档记录模块四“AI辅助测试与调试”的测试过程。测试对象为当前 `main` 分支整合后的 ABCD 四个模块代码，重点检查后端接口、前端构建、用户权限、论坛内容、社交互动和后台审核管理流程是否符合模块二设计文档要求。

## 一、测试目标

- 检查后端 FastAPI 项目能否正常编译和导入。
- 检查用户登录态、发帖作者、长文分析权限是否正确。
- 检查社交互动模块的评论、回复、点赞、收藏、关注、通知、举报和群组接口是否可用。
- 检查板块、标签写接口是否受到管理员权限保护。
- 检查 SQLite 本地旧库在新增字段和新增表时是否能兼容启动。
- 检查前端 TypeScript 类型检查和 Vite 构建是否通过。
- 检查新增页面和路由是否能被前端构建正确识别。
- 使用真实浏览器联调登录、帖子互动、群组、个人中心、通知、后台权限和移动端首页。
- 记录测试过程中发现的环境问题和处理方式。

## 二、测试环境

| 项目 | 内容 |
| --- | --- |
| 操作系统 | Windows |
| 当前分支 | `main` |
| 后端框架 | FastAPI + SQLAlchemy |
| 前端框架 | Vue 3 + Vite + TypeScript |
| 数据库 | SQLite 临时测试库 |
| 后端测试方式 | Python 编译检查、FastAPI TestClient 接口回归 |
| 前端测试方式 | `npm run build`、Chrome + Playwright 真实浏览器联调 |
| 测试日期 | 2026.6.16 - 2026.6.22 |

## 三、后端测试

### 1. 编译检查

执行命令：

```bash
python -m compileall backend\app
```

测试结果：通过。后端 `app` 目录下的公共组件、认证模块、论坛模块、社交互动模块和后台模块均可完成 Python 编译。

### 2. API 回归测试

测试方式：使用 Python 3.12 临时虚拟环境、临时 SQLite 数据库和 FastAPI TestClient。测试数据库通过 `DATABASE_URL=sqlite:///临时文件` 指定，测试结束后删除，避免污染仓库中的运行数据。

| 测试项 | 接口或流程 | 实际结果 |
| --- | --- | --- |
| 健康检查 | `GET /api/health` | 通过 |
| 普通用户登录 | `POST /api/auth/login` | 通过 |
| 专业用户登录 | `POST /api/auth/login` | 通过 |
| 登录用户发帖 | `POST /api/posts` | 通过，作者为当前登录用户 |
| 普通用户发布长文 | `POST /api/posts/analysis` | 通过，返回权限不足 |
| 专业用户发布长文 | `POST /api/posts/analysis` | 通过，`post_type=2` |
| 发表评论 | `POST /api/posts/{post_id}/comments` | 通过 |
| 回复评论 | `POST /api/comments/{comment_id}/replies` | 通过 |
| 获取评论列表 | `GET /api/posts/{post_id}/comments` | 通过，包含楼中楼回复 |
| 点赞帖子 | `POST /api/posts/{post_id}/like` | 通过 |
| 收藏帖子 | `POST /api/posts/{post_id}/favorite` | 通过 |
| 我的收藏 | `GET /api/me/favorites` | 通过 |
| 关注用户 | `POST /api/users/{user_id}/follow` | 通过 |
| 关注列表 | `GET /api/users/{user_id}/following` | 通过 |
| 关注动态 | `GET /api/feed/following` | 通过 |
| 通知列表 | `GET /api/me/notifications` | 通过 |
| 标记通知已读 | `PUT /api/me/notifications/{id}/read` | 通过 |
| 创建群组 | `POST /api/groups` | 通过 |
| 加入群组 | `POST /api/groups/{id}/join` | 通过 |
| 群组列表 | `GET /api/groups` | 通过 |
| 未登录创建板块 | `POST /api/sections` | 通过，返回未登录 |
| 普通用户创建板块 | `POST /api/sections` | 通过，返回权限不足 |
| 管理员创建板块 | `POST /api/sections`、`POST /api/admin/sections` | 通过 |
| 管理员创建标签 | `POST /api/tags`、`POST /api/admin/tags` | 通过 |
| 查询帖子互动状态 | `GET /api/posts/{id}/interaction-status` | 通过，返回已点赞、已收藏、已关注作者 |
| 举报帖子 | `POST /api/posts/{id}/report` | 通过，写入 `report_items` |
| 举报评论 | `POST /api/comments/{id}/report` | 通过，写入 `report_items` |
| 审核群加入申请 | `POST /api/groups/{id}/join` | 通过，返回 `pending=true` 且未写入正式成员 |
| 审核群详情刷新 | `GET /api/groups/{id}` | 通过，保留申请中状态 |
| SQLite 旧库兼容 | 启动时补齐字段/表 | 通过，补齐 `posts.post_type`、`posts.is_elite`、`groups.description`、`notifications`、`group_join_requests` |

接口回归结果：35 项通过，0 项失败。

## 四、前端测试

执行命令：

```bash
cd frontend
npm run build
```

构建过程包含：

- `vue-tsc --noEmit`
- `vite build`

测试结果：通过。说明当前前端新增的社交互动页面、路由、组件、API 类型定义和原有 A/B/D 模块页面之间不存在阻塞构建的 TypeScript 类型错误或 Vite 打包错误。

## 五、交付复现检查

### 1. README 启动命令复现

| 检查项 | 命令或方式 | 实际结果 |
| --- | --- | --- |
| 后端编译 | `py -3.13 -m compileall backend\app` | 通过 |
| 后端启动 | `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000` | 通过，`/api/health` 返回 `ok` |
| 后端烟测 | `scripts/backend_smoke_test.py` | 通过，21 项检查全部通过 |
| 前端构建 | `npm run build` | 通过 |
| 前端启动 | `npm run dev -- --host 127.0.0.1 --port 5173` | 通过，开发服务返回 200 |

2026.6.22 复查时本机默认 `python` 为 Python 3.9.13。已将后端关键 ORM、Schema 和 Router 类型注解改为 Python 3.9 兼容写法，并按 `backend/requirements.txt` 刷新项目内 `backend/venv_lib` 依赖后重新执行独立后端烟测，21 项检查全部通过。

### 2. 文档一致性检查

本次交付复现后同步检查 README、架构设计、UI 设计、后端说明、前端说明和测试报告。已将当前实现口径统一为 `FastAPI + SQLAlchemy + Vue 3 + Vite + TypeScript`，开发环境默认使用 SQLite，MySQL 作为可选部署数据库；同时明确 `HANDOFF.md` 为历史交接记录，避免其中旧路径、旧分支和旧端口影响最终验收。

## 六、真实浏览器全链路联调

### 1. 联调环境

| 项目 | 内容 |
| --- | --- |
| 后端服务 | `http://127.0.0.1:8000` |
| 前端服务 | `http://127.0.0.1:5174` |
| 说明 | 默认前端端口仍为 `5173`，本次测试时 `5173` 处于 TIME_WAIT 状态，因此 Vite 自动切换到 `5174` |
| 浏览器 | Chrome |
| 自动化方式 | Playwright 脚本驱动真实页面访问、登录、点击和截图 |
| 截图目录 | `figs/e2e-20260617/` |

### 2. 浏览器检查结果

| 序号 | 检查项 | 实际结果 |
| --- | --- | --- |
| 1 | 首页品牌可见 | 通过 |
| 2 | 首页演示数据区域可见 | 通过 |
| 3 | 首页演示帖子可见 | 通过 |
| 4 | 普通用户 `value@stockforum.com` 登录并写入 token | 通过 |
| 5 | 登录后顶部导航显示当前用户 | 通过 |
| 6 | 帖子详情页标题可见 | 通过 |
| 7 | 帖子详情页评论区可见 | 通过 |
| 8 | 点赞、收藏、评论等帖子互动按钮可见 | 通过 |
| 9 | 新增评论后页面能显示评论内容 | 通过 |
| 10 | 群组列表可见 | 通过 |
| 11 | 审核群状态可见 | 通过 |
| 12 | 个人中心页面可访问 | 通过 |
| 13 | 个人中心昵称可见 | 通过 |
| 14 | 通知中心页面可访问 | 通过 |
| 15 | 普通用户顶部导航不显示后台入口 | 通过 |
| 16 | 普通用户直接访问后台路由会被拦截并回到首页 | 通过 |
| 17 | 管理员 `admin@stockforum.com` 登录并写入 token | 通过 |
| 18 | 管理员顶部导航显示后台入口 | 通过 |
| 19 | 管理员可进入后台概览页 | 通过 |
| 20 | 移动端首页布局和主要内容可见 | 通过 |

浏览器联调脚本共执行 20 个断言，结果为 20 项通过、0 项失败。

### 3. 联调截图

首页演示数据：

![首页演示数据](figs/e2e-20260617/01-home.png)

帖子详情与评论互动：

![帖子详情与评论互动](figs/e2e-20260617/05-post-detail-comment.png)

群组列表与审核群：

![群组列表与审核群](figs/e2e-20260617/06-groups.png)

普通用户后台拦截：

![普通用户后台拦截](figs/e2e-20260617/09-admin-normal-user-guarded.png)

管理员后台概览：

![管理员后台概览](figs/e2e-20260617/10-admin-overview-guarded.png)

移动端首页：

![移动端首页](figs/e2e-20260617/13-mobile-home.png)

## 七、发现的问题与处理

### 1. 系统默认 Python 版本依赖不匹配

测试时发现系统默认 `python` 为 Python 3.8.6，加载到的 SQLAlchemy 版本不支持项目中使用的 `DeclarativeBase`，直接运行接口测试会失败。

处理方式：早期测试改用已有 Python 3.12 临时测试环境执行后端回归；2026.6.22 复查时进一步将后端类型注解调整为 Python 3.9 兼容写法，并按 `backend/requirements.txt` 刷新项目内依赖目录，确认本机默认 Python 3.9.13 也可以完成后端烟测。

### 2. 论坛发帖作者固定

检查 `backend/app/modules/forum/router.py` 时发现 `POST /api/posts` 固定调用 `crud.create_post(..., user_id=1)`，不符合“登录用户发布帖子”的接口设计。

处理方式：将发帖接口改为依赖 `get_current_user`，使用当前登录用户 ID 创建帖子；同时补充编辑、删除权限边界。

### 3. 社交互动模块缺失

检查仓库时发现 `backend/app/modules/interaction` 和 `frontend/src/modules/interaction` 基本只有占位文件，评论、点赞、收藏、关注、通知和群组均未落地。

处理方式：新增社交互动后端模型、服务、路由、前端 API、类型、组件和页面，并与帖子详情、用户主页、个人中心和顶部导航联动。

### 4. 权限与状态闭环缺口

补充检查发现板块、标签写接口需要管理员权限保护，帖子详情页缺少已点赞/已收藏/已关注状态回显，举报接口虽在设计文档中存在但前后端闭环不足，需审核群组点击加入后不应直接成为成员。

处理方式：为板块和标签写接口增加管理员依赖，并补充 `/api/admin/sections`、`/api/admin/tags`；新增帖子互动状态接口；补齐帖子和评论举报接口及前端入口；新增 `group_join_requests` 保存审核群加入申请；为 SQLite 本地旧库补齐新增字段和表。

### 5. 普通用户后台前端入口暴露

真实浏览器联调时发现普通用户登录后可以看到后台导航入口，并能进入后台页面壳。该问题虽然后端接口仍有权限保护，但前端体验不符合后台管理权限设计。

处理方式：在前端路由中为后台页面增加 `meta.requiresAdmin`，路由守卫在进入后台前加载当前用户并判断 `role === "ADMIN"`；同时顶部导航仅在管理员登录时展示“后台”入口。修复后复测普通用户后台入口隐藏、直接访问后台路由被重定向，管理员仍可正常进入后台。

## 八、测试结论

本次测试覆盖后端编译、A/B/C/D 关键接口、前端构建、README 冷启动复现、真实浏览器全链路联调、权限边界、举报闭环、审核群申请状态、SQLite 旧库兼容和模块文档一致性检查。测试结果显示，当前 `main` 分支中用户与权限、论坛内容、社交互动、审核后台四个模块的主流程可以通过构建、接口回归、冷启动复现和浏览器联调检查，后端 API 回归为 35 项通过、0 项失败；独立后端烟测脚本为 21 项通过、0 项失败；真实浏览器联调为 20 项通过、0 项失败。2026.6.22 复查时再次执行 `python -m compileall backend\app`、`scripts/backend_smoke_test.py` 和 `npm run build`，结果均通过。

后续如果继续完善，可以补充正式测试用例文件、异常参数测试，以及更完整的群组资料区和认证审核页面。

## 九、2026.6.22 最新补齐功能复测

本次复测在现有 `main` 分支工作树上执行，覆盖新增的资料扩展、附件、投票、搜索建议、热议话题、特别关注、私信、群组讨论、群组资源和自动审核入队等功能。

### 1. 后端编译

```bash
python -m compileall backend\app
```

结果：通过。

### 2. 后端测试

```bash
$env:PYTHONPATH=(Resolve-Path 'backend\venv_lib').Path + ';' + (Resolve-Path 'backend').Path; python scripts\backend_smoke_test.py
```

结果：32 项 PASS，0 项 FAIL。新增覆盖项包括：

| 测试项 | 覆盖接口或流程 | 结果 |
| --- | --- | --- |
| 用户资料扩展 | `PUT /api/users/me/profile` | PASS |
| 帖子附件 | `POST /api/posts/{post_id}/attachments` | PASS |
| 投票选项与投票 | `POST /api/posts/{post_id}/poll-options`、`POST /api/poll-options/{option_id}/vote` | PASS |
| 搜索建议 | `GET /api/search/suggestions` | PASS |
| 热议话题 | `GET /api/hot-topics` | PASS |
| 特别关注 | `PUT /api/users/{user_id}/follow/star` | PASS |
| 私信 | `POST /api/users/{user_id}/messages` | PASS |
| 群组讨论 | `POST /api/groups/{group_id}/posts` | PASS |
| 群组资源 | `POST /api/groups/{group_id}/resources` | PASS |
| OpenAPI 生成 | `GET /openapi.json` | PASS |

### 3. 前端构建

```bash
cd frontend
npm run build
```

结果：通过。`vue-tsc --noEmit` 和 `vite build` 均通过，构建产物位于 `frontend/dist/`。

### 4. 结论

当前项目代码、SQL 脚本、模块三实现记录、模块四测试记录、模块五部署说明、用户手册和项目总结报告已经覆盖指导书中本题目要求的主要业务功能、测试验证和本地部署交付项。
