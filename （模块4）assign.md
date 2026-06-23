# 工作完成情况记录

## 模块四：AI辅助测试与调试

### 时间：2026.6.22

### 分工


| 成员 | 负责模块 | 测试与调试范围 |
|------|----------|----------------|
| 谢亨义（负责人） | 社交互动模块、整体验证与缺陷修复 | 评论、回复、点赞、收藏、关注、通知、群组、举报、测试环境、文档核对 |
| 牟俊臣 | 用户与权限模块 | 注册、登录、JWT、个人中心、认证申请、风险测评、用户公开主页、权限联动 |
| 徐英博 | 论坛内容模块 | 板块、标签、帖子、搜索、热榜、普通发帖、长文分析、帖子详情 |
| 周颂捷 | 审核与后台模块 | 后台概览、审核队列、举报处理、敏感词、用户处置、统计、管理员权限 |


---

## 一、总体模块要求完成情况核对

| 指导书要求 | 当前完成情况 | 证据 |
|------|------|------|
| 使用 AI 辅助生成测试用例 | 已完成 | `（模块4）ai.md` 记录测试提示词、AI 输出摘要、人工检查和迭代优化 |
| 单元测试或控制结构测试 | 已完成基础覆盖 | `scripts/backend_smoke_test.py` 使用 FastAPI TestClient 覆盖核心接口与分支 |
| 使用接口测试工具或 Swagger 测试后端接口 | 已完成 | 后端烟测覆盖健康检查、认证、发帖、评论、点赞、收藏、举报、群组、后台权限等接口 |
| 根据交互场景生成功能测试用例并测试 | 已完成 | `（模块4）test.md` 记录真实浏览器联调和截图路径 |
| 用 AI 辅助定位 bug | 已完成 | 记录并修复发帖作者固定、社交互动缺失、权限入口暴露、Python 3.9 类型兼容、bcrypt 依赖不一致等问题 |
| 输出测试报告 `test.md` | 已完成 | `（模块4）test.md` |
| 输出 AI 使用记录 `ai.md` | 已完成 | `（模块4）ai.md` |
| 输出工作完成情况 `assign.md` | 已完成 | 本文件 |

---

## 二、谢亨义（负责人）- 社交互动模块、整体验证与缺陷修复

| 分类 | 测试项或修复项 | 检查方式 | 结果 |
|------|----------------|----------|------|
| 指导书核对 | 模块四测试要求 | 结构化读取 `2026课程设计实验指导书V1.docx` | 完成 |
| 代码审计 | 后端路由、模型、服务 | `rg` 检查路由、模型、接口、测试脚本 | 完成 |
| 代码审计 | 前端路由、API、页面 | 检查 `frontend/src/shared/router/index.ts`、各模块 API 和页面 | 完成 |
| 环境修复 | 前端缺少依赖 | 执行 `npm ci` 安装 lockfile 对应依赖 | 完成 |
| 环境修复 | 后端依赖版本不一致 | 执行 `python -m pip install --upgrade --target backend\venv_lib -r backend\requirements.txt` | 完成 |
| 缺陷修复 | Python 3.9 无法导入 `str | None` ORM 注解 | 将 ORM 模型改为 `Optional[...]`、`List[...]` | 已修复 |
| 缺陷修复 | Python 3.9 无法解析 Pydantic/FastAPI 的 PEP604 注解 | 将 Schema 和路由参数改为 `Optional[...]`、`List[...]` | 已修复 |
| 缺陷修复 | bcrypt 5 与 passlib 1.7.4 不兼容 | 按 requirements 将 bcrypt 刷新为 4.0.1 | 已修复 |
| 评论 | 发布评论 | 后端烟测调用 `POST /api/posts/{post_id}/comments` | 通过 |
| 评论 | 回复评论 | 后端烟测调用 `POST /api/comments/{comment_id}/replies` | 通过 |
| 点赞 | 帖子点赞 | 后端烟测调用 `POST /api/posts/{post_id}/like` | 通过 |
| 收藏 | 帖子收藏 | 后端烟测调用 `POST /api/posts/{post_id}/favorite` | 通过 |
| 状态 | 互动状态查询 | 后端烟测调用 `GET /api/posts/{post_id}/interaction-status` | 通过 |
| 举报 | 帖子举报 | 后端烟测调用 `POST /api/posts/{post_id}/report` | 通过 |
| 群组 | 创建群组 | 后端烟测调用 `POST /api/groups` | 通过 |
| 群组 | 查看群组 | 后端烟测调用 `GET /api/groups/{group_id}` | 通过 |
| 前端 | 互动页面和组件构建 | `npm run build` | 通过 |

---

## 三、牟俊臣 - 用户与权限模块测试与调试

| 分类 | 测试项 | 检查方式 | 结果 |
|------|--------|----------|------|
| 注册 | 邮箱注册 | 后端烟测调用 `POST /api/auth/register` | 通过 |
| 登录 | 普通用户登录 | 后端烟测调用 `POST /api/auth/login` | 通过 |
| 登录 | 管理员登录 | 后端烟测调用 `POST /api/auth/login` | 通过 |
| 登录态 | 当前用户信息 | 后端烟测调用 `GET /api/users/me` | 通过 |
| Token | 请求拦截器 | 检查 `frontend/src/shared/api/request.ts` 自动附加 Bearer Token | 通过 |
| 权限 | 未登录路由保护 | 检查前端路由 `meta.requiresAuth` | 通过 |
| 权限 | 管理员路由保护 | 检查 `meta.requiresAdmin` 与 `loadCurrentUser()` 角色判断 | 通过 |
| 个人中心 | 用户资料展示和编辑 | 检查 `ProfileView.vue` 与 `PUT /api/users/me/profile` | 通过 |
| 认证 | 实名/专业认证表单 | 检查 `CertificationView.vue` 与认证接口 | 通过 |
| 风险测评 | 风险问卷提交 | 检查 `RiskAssessmentView.vue` 与风险测评接口 | 通过 |
| 用户主页 | 公开资料与关注入口 | 检查 `UserPublicView.vue` | 通过 |

---

## 四、徐英博 - 论坛内容模块测试与调试

| 分类 | 测试项 | 检查方式 | 结果 |
|------|--------|----------|------|
| 板块 | 板块列表 | 后端烟测调用 `GET /api/sections` | 通过 |
| 标签 | 标签列表 | 后端烟测调用 `GET /api/tags` | 通过 |
| 发帖 | 登录用户发帖 | 后端烟测调用 `POST /api/posts`，确认返回帖子 ID | 通过 |
| 发帖 | 作者修复 | 检查 `create_post` 使用当前登录用户 ID，不再固定 `user_id=1` | 通过 |
| 长文 | 专业认证长文接口 | 检查 `POST /api/posts/analysis` 权限逻辑 | 通过 |
| 帖子详情 | 详情查询 | 后端烟测调用 `GET /api/posts/{post_id}` | 通过 |
| 搜索 | 关键词搜索 | 检查 `GET /api/search/posts` | 通过 |
| 热榜 | 热门帖子 | 检查 `GET /api/posts/hot` 加权排序逻辑 | 通过 |
| 前端 | 首页/板块/热榜/搜索/发帖/详情 | `npm run build` 覆盖 TypeScript 和 Vite 构建 | 通过 |
| 权限 | 板块和标签写接口 | 后台写接口依赖 `require_admin` | 通过 |

---

## 五、周颂捷 - 审核与后台模块测试与调试

| 分类 | 测试项 | 检查方式 | 结果 |
|------|--------|----------|------|
| 后台概览 | 管理员访问概览 | 后端烟测调用 `GET /api/admin/overview` | 通过 |
| 后台权限 | 普通用户访问后台 | 后端烟测确认返回 `40301` | 通过 |
| 举报处理 | 举报列表 | 后端烟测调用 `GET /api/admin/reports` | 通过 |
| 审核队列 | 审核列表和处理 | 检查 `GET/PATCH /api/admin/audit-queue` | 通过 |
| 敏感词 | 敏感词列表和启停 | 检查 `GET/PATCH /api/admin/sensitive-words` | 通过 |
| 用户处置 | 处罚记录 | 检查 `GET /api/admin/user-moderation` | 通过 |
| 数据分析 | 后台统计 | 检查 `GET /api/admin/statistics` | 通过 |
| 前端 | 后台页面构建 | `npm run build` 覆盖后台全部页面 | 通过 |
| 前端权限 | 普通用户后台入口隐藏 | 检查 `App.vue` 的 `isAdminUser` 控制 | 通过 |
| 前端权限 | 非管理员路由拦截 | 检查 `router.beforeEach` 管理员判断 | 通过 |
