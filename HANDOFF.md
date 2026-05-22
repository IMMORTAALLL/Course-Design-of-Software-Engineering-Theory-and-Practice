# 交接文档

更新时间：2026-05-22
项目路径：`D:\project\soft_practice\Course-Design-of-Software-Engineering-Theory-and-Practice`

## 1. 项目结论

- 课程选题：题目三，股票基金投资论坛。
- 项目名称：智投社区。
- 用户身份：成员 D。
- 成员 D 分支：`feature/admin-audit`。
- 成员 D 模块：后台管理、内容审核、举报处理、敏感词管理、用户处罚、精华标记、运营统计。
- 后端技术栈：`FastAPI + SQLAlchemy`。
- 前端技术栈：`Vue 3 + Vite + TypeScript`。
- 当前本地分支：`feature/admin-audit`。
- 当前本地 HEAD：`5a7a958 feat: 搭建后端FastAPI项目骨架，包含通用组件和安全层`。
- 远程仓库：`https://github.com/IMMORTAALLL/Course-Design-of-Software-Engineering-Theory-and-Practice.git`。

## 2. 必须遵守的 Git 规则

Git 规则文件在：

- `D:\project\soft_practice\GIT_RULES.md`

每次执行 Git 操作前都必须先读这个文件。已经确认过的硬性规则：

- 不直接在 `main` 上开发。
- 成员 D 使用 `feature/admin-audit`。
- 不使用 `git add .`。
- 不使用 `git reset --hard`。
- 不使用 `git push -f`。
- 提交前看 `git status` 和 `git diff`。
- 只添加自己负责的文件。
- 通过 Pull Request 合并到 `main`。

本次会话已经执行过：

- `git pull origin main`
- `git switch -c feature/admin-audit`

没有执行 commit，没有执行 push。

## 3. 分工信息

成员 D 负责的前端目录：

- `frontend/src/modules/admin`

成员 D 负责的后端目录：

- `backend/app/modules/admin`

成员 D 负责或需要同步的文档：

- `（模块2）db.md`
- `（模块2）backend_api.md`
- `（模块2）ai.md`
- `user_guid.md` 目前仓库根目录中还没有看到这个文件。

## 4. 已知 UI 风格要求

仓库已有设计文档：

- `D:\project\soft_practice\Course-Design-of-Software-Engineering-Theory-and-Practice\（模块2）ui_design.md`

该文档规定的方向：

- 风格：专业、清晰、可信。
- 不做过度娱乐化风格。
- 前台布局：顶部导航 + 主内容区 + 右侧信息栏。
- 后台布局：左侧菜单 + 顶部状态栏 + 主工作区。
- 主色：深蓝或科技蓝。
- 辅助色：绿色表示上涨或积极，红色表示下跌或风险。
- 中性色：白色、浅灰、深灰。
- 警示色：橙色或红色。

当前后台页面实现按这个方向做，没有换成别的视觉风格。

## 5. 后端已完成内容

新增后台模块文件：

- `backend/app/modules/admin/bootstrap.py`
- `backend/app/modules/admin/models.py`
- `backend/app/modules/admin/router.py`
- `backend/app/modules/admin/schemas.py`
- `backend/app/modules/admin/service.py`

已实现模型：

- `AuditQueueItem`
- `ReportItem`
- `SensitiveWord`
- `UserModerationRecord`

已实现接口：

- `GET /api/admin/overview`
- `GET /api/admin/audit-queue`
- `GET /api/admin/reports`
- `GET /api/admin/sensitive-words`
- `PATCH /api/admin/audit-queue/{item_id}`
- `PATCH /api/admin/reports/{item_id}`
- `PATCH /api/admin/sensitive-words/{word_id}`
- `GET /api/admin/user-moderation`
- `GET /api/admin/statistics`

已实现业务能力：

- 后台概览统计。
- 内容审核队列查询。
- 举报列表查询。
- 敏感词列表查询。
- 审核通过和驳回。
- 举报驳回、警告、封禁。
- 敏感词启用和停用。
- 用户处罚记录查询。
- 热门话题和活跃板块统计摘要。

已修改后端公共文件：

- `backend/app/main.py`
- `backend/app/config.py`
- `backend/app/database.py`
- `backend/app/common/deps.py`
- `backend/README.md`

准确变化：

- `main.py` 已挂载后台 admin 路由。
- `main.py` 启动时会建表并写入后台演示数据。
- `config.py` 默认 `DATABASE_URL` 改为 `sqlite:///./forum_system.db`。
- `database.py` 对 SQLite 增加 `check_same_thread=False`。
- `deps.py` 已清理末尾多余内容，导出 `get_db` 和 `get_current_user`。
- `backend/README.md` 已说明本地开发默认使用 SQLite。

## 6. 数据库脚本已完成内容

已修改：

- `database/schema.sql`
- `database/seed.sql`

新增或补充的表：

- `audit_queue_items`
- `report_items`
- `sensitive_words`
- `user_moderation_records`

补充的演示数据包括：

- 内容审核数据。
- 举报处理数据。
- 敏感词数据。
- 用户处罚记录数据。

当前本地运行会生成：

- `backend/forum_system.db`

这个文件是本地 SQLite 数据库，已经加入 `.gitignore`，不应该提交。

## 7. 前端已完成内容

新增前端工程文件：

- `frontend/index.html`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/tsconfig.json`
- `frontend/vite.config.ts`
- `frontend/src/App.vue`
- `frontend/src/main.ts`

新增共享层文件：

- `frontend/src/shared/api/http.ts`
- `frontend/src/shared/layouts/AdminLayout.vue`
- `frontend/src/shared/router/index.ts`
- `frontend/src/shared/styles/base.css`

新增后台模块文件：

- `frontend/src/modules/admin/api/admin.ts`
- `frontend/src/modules/admin/types/admin.ts`
- `frontend/src/modules/admin/views/AdminDashboard.vue`
- `frontend/src/modules/admin/views/AdminAuditView.vue`
- `frontend/src/modules/admin/views/AdminReportsView.vue`
- `frontend/src/modules/admin/views/AdminSensitiveWordsView.vue`
- `frontend/src/modules/admin/views/AdminModerationView.vue`
- `frontend/src/modules/admin/views/AdminStatisticsView.vue`

已实现路由：

- `/admin`
- `/admin/audits`
- `/admin/reports`
- `/admin/sensitive-words`
- `/admin/users`
- `/admin/statistics`

已实现页面能力：

- 后台统一布局：左侧菜单 + 顶部信息 + 主内容区。
- 后台首页概览卡片。
- 内容审核页。
- 举报处理页。
- 敏感词管理页。
- 用户处罚页。
- 运营统计页。
- 审核、举报、敏感词状态按钮已接后端接口。

前端 API 地址当前为：

- 默认值：`http://127.0.0.1:8001`
- 可用环境变量覆盖：`VITE_API_BASE_URL`
- 配置位置：`frontend/src/shared/api/http.ts`

## 8. 当前验证结果

已经验证过后端接口在 `8001` 可访问：

- `http://127.0.0.1:8001/api/health`
- `http://127.0.0.1:8001/api/admin/overview`
- `http://127.0.0.1:8001/api/admin/audit-queue`
- `http://127.0.0.1:8001/api/admin/reports`
- `http://127.0.0.1:8001/api/admin/sensitive-words`
- `http://127.0.0.1:8001/api/admin/user-moderation`
- `http://127.0.0.1:8001/api/admin/statistics`

已经验证过前端开发页在 `5173` 可访问：

- `http://127.0.0.1:5173`

已经执行前端构建：

```bash
npm.cmd run build
```

结果：

- `vue-tsc --noEmit` 通过。
- `vite build` 通过。

此前已经执行过后端 Python 语法检查，涉及后台模块和公共入口文件，通过。

## 9. 当前 Git 状态

当前分支：

- `feature/admin-audit`

当前没有提交 commit。

当前已修改文件：

- `.gitignore`
- `（模块2）backend_api.md`
- `（模块2）db.md`
- `（模块2）ai.md`
- `backend/README.md`
- `backend/app/common/deps.py`
- `backend/app/config.py`
- `backend/app/database.py`
- `backend/app/main.py`
- `database/schema.sql`
- `database/seed.sql`
- `frontend/README.md`

当前新增未跟踪文件：

- `HANDOFF.md`
- `backend/app/modules/admin/bootstrap.py`
- `backend/app/modules/admin/models.py`
- `backend/app/modules/admin/router.py`
- `backend/app/modules/admin/schemas.py`
- `backend/app/modules/admin/service.py`
- `frontend/index.html`
- `frontend/package-lock.json`
- `frontend/package.json`
- `frontend/src/App.vue`
- `frontend/src/main.ts`
- `frontend/src/modules/admin/api/admin.ts`
- `frontend/src/modules/admin/types/admin.ts`
- `frontend/src/modules/admin/views/AdminAuditView.vue`
- `frontend/src/modules/admin/views/AdminDashboard.vue`
- `frontend/src/modules/admin/views/AdminModerationView.vue`
- `frontend/src/modules/admin/views/AdminReportsView.vue`
- `frontend/src/modules/admin/views/AdminSensitiveWordsView.vue`
- `frontend/src/modules/admin/views/AdminStatisticsView.vue`
- `frontend/src/shared/api/http.ts`
- `frontend/src/shared/layouts/AdminLayout.vue`
- `frontend/src/shared/router/index.ts`
- `frontend/src/shared/styles/base.css`
- `frontend/tsconfig.json`
- `frontend/vite.config.ts`

`backend/forum_system.db` 已被 `.gitignore` 忽略，不在当前 Git 状态列表中。

`frontend/dist/` 已在 `.gitignore` 中，执行构建后不在当前 Git 状态列表中。

## 10. 明确未完成项

以下内容还没有完成：

- 没有提交 commit。
- 没有 push 到远程 `feature/admin-audit`。
- 没有创建 Pull Request。
- 没有实现独立的用户禁言接口。
- 没有实现独立的用户封号接口。
- 没有实现板块管理页。
- 没有实现认证审核页。
- 没有做浏览器截图级页面验证。
- 没有把 SQLite 作为团队正式数据库方案写入团队决策文档。

## 11. 下一步建议

下一步按这个顺序做：

1. 检查 `git diff`。
2. 确认 `backend/forum_system.db` 不在待提交列表。
3. 按文件逐个 `git add`，不要使用 `git add .`。
4. commit 信息建议：`feat: 实现后台审核管理模块`。
5. push：`git push -u origin feature/admin-audit`。
6. 在 GitHub 创建 Pull Request，目标分支选择 `main`。

## 12. 新对话必须先做的事

新对话开始后先读：

- `D:\project\soft_practice\GIT_RULES.md`
- `D:\project\soft_practice\Course-Design-of-Software-Engineering-Theory-and-Practice\HANDOFF.md`
- `D:\project\soft_practice\Course-Design-of-Software-Engineering-Theory-and-Practice\（模块2）ui_design.md`

然后执行：

```bash
git status --short --branch
```

确认仍在 `feature/admin-audit`，确认 `backend/forum_system.db` 没出现在待提交列表中。
