# 测试报告

项目名称：智投社区：股票基金投资论坛系统

本文档记录模块四“AI辅助测试与调试”的测试过程。测试对象为当前 `docx` 分支整合后的 ABCD 四个模块代码，重点检查后端接口、前端构建、用户权限、论坛内容、社交互动和后台审核管理流程是否符合模块二设计文档要求。

## 一、测试目标

- 检查后端 FastAPI 项目能否正常编译和导入。
- 检查用户登录态、发帖作者、长文分析权限是否正确。
- 检查社交互动模块的评论、回复、点赞、收藏、关注、通知和群组接口是否可用。
- 检查前端 TypeScript 类型检查和 Vite 构建是否通过。
- 检查新增页面和路由是否能被前端构建正确识别。
- 记录测试过程中发现的环境问题和处理方式。

## 二、测试环境

| 项目 | 内容 |
| --- | --- |
| 操作系统 | Windows |
| 当前分支 | `docx` |
| 后端框架 | FastAPI + SQLAlchemy |
| 前端框架 | Vue 3 + Vite + TypeScript |
| 数据库 | SQLite 临时测试库 |
| 后端测试方式 | Python 编译检查、FastAPI TestClient 接口回归 |
| 前端测试方式 | `npm run build` |
| 测试日期 | 2026.6.16 |

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

接口回归结果：21 项通过，0 项失败。

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

## 五、发现的问题与处理

### 1. 系统默认 Python 版本依赖不匹配

测试时发现系统默认 `python` 为 Python 3.8.6，加载到的 SQLAlchemy 版本不支持项目中使用的 `DeclarativeBase`，直接运行接口测试会失败。

处理方式：改用已有 Python 3.12 临时测试环境执行后端回归，该环境中 SQLAlchemy 版本为 2.0.35，与 `backend/requirements.txt` 一致。

### 2. 论坛发帖作者固定

检查 `backend/app/modules/forum/router.py` 时发现 `POST /api/posts` 固定调用 `crud.create_post(..., user_id=1)`，不符合“登录用户发布帖子”的接口设计。

处理方式：将发帖接口改为依赖 `get_current_user`，使用当前登录用户 ID 创建帖子；同时补充编辑、删除权限边界。

### 3. 社交互动模块缺失

检查仓库时发现 `backend/app/modules/interaction` 和 `frontend/src/modules/interaction` 基本只有占位文件，评论、点赞、收藏、关注、通知和群组均未落地。

处理方式：新增社交互动后端模型、服务、路由、前端 API、类型、组件和页面，并与帖子详情、用户主页、个人中心和顶部导航联动。

## 六、测试结论

本次测试覆盖后端编译、A/B/C/D 关键接口、前端构建和模块文档一致性检查。测试结果显示，当前 `docx` 分支中用户与权限、论坛内容、社交互动、审核后台四个模块的主流程可以通过构建和接口回归检查，最终 API 回归为 21 项通过、0 项失败。

后续如果继续完善，可以补充浏览器自动化截图测试、正式后端测试用例文件、异常参数测试，以及更完整的群组资料区和认证审核页面。
