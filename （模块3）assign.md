# 工作完成情况记录

## 模块三：AI辅助编码实现

### 时间：2026.6.22

### 分工


| 成员 | 负责模块 | 主要目录 |
|------|----------|----------|
| 谢亨义（负责人） | 社交互动模块、整体整合与补齐 | `backend/app/modules/interaction`、`frontend/src/modules/interaction` |
| 牟俊臣 | 用户与权限模块 | `backend/app/modules/auth`、`frontend/src/modules/auth` |
| 徐英博 | 论坛内容模块 | `backend/app/modules/forum`、`frontend/src/modules/forum` |
| 周颂捷 | 审核与后台模块 | `backend/app/modules/admin`、`frontend/src/modules/admin` |


---

## 一、课程指导书模块三要求核对

| 指导书要求 | 当前完成情况 | 证据 |
|------|------|------|
| 搭建前后端框架 | 已完成 | FastAPI 入口 `backend/app/main.py`；Vue 3 + Vite 入口 `frontend/src/main.ts` |
| 实现业务逻辑 | 已完成 | 用户认证、论坛发帖、附件、投票、搜索建议、热议话题、评论、点赞、收藏、关注、私信、通知、群组讨论、群组资源、举报、自动审核和后台管理均有后端接口和前端入口 |
| 数据库连接 | 已完成 | `backend/app/database.py` 支持 SQLite 默认开发和 MySQL 可选部署 |
| 输出可运行项目代码 | 已完成 | 后端编译、后端烟测、前端构建均通过 |
| 输出 SQL 脚本 | 已完成 | `database/schema.sql`、`database/seed.sql` |
| AI 使用记录 | 已完成 | `（模块3）ai.md` |
| 工作完成情况记录 | 已完成 | 本文件 |

---

## 二、谢亨义（负责人）- 社交互动模块、整合与补齐工作

| 分类 | 细分功能 | 具体工作 | 状态 |
|------|----------|----------|------|
| 负责人工作 | 指导书要求核对 | 读取 `2026课程设计实验指导书V1.docx`，核对模块三编码实现交付要求 | 已完成 |
| 负责人工作 | README 分工核对 | 按 README 确认 A/B/C/D 模块归属和谢亨义负责人身份 | 已完成 |
| 负责人工作 | 代码现状审计 | 核查后端路由、模型、服务、前端路由、前端 API 和测试脚本 | 已完成 |
| 负责人工作 | 远端同步 | 拉取 `origin/main` 最新 17 个提交，并保留本地旧 assign 备份 | 已完成 |
| 负责人工作 | 本地备份 | 保存 `（模块3）assign.local-backup-20260622-164003.md` | 已完成 |
| 负责人工作 | Python 3.9 兼容 | 将后端关键 ORM、Schema、Router 注解改为 Python 3.9 可导入形式 | 已完成 |
| 负责人工作 | 依赖一致性 | 按 `backend/requirements.txt` 刷新忽略目录 `backend/venv_lib`，修复 bcrypt 版本不一致导致的烟测失败 | 已完成 |
| 评论 | 评论列表 | `GET /api/posts/{post_id}/comments` 返回评论和楼中楼回复 | 已完成 |
| 评论 | 发布评论 | `POST /api/posts/{post_id}/comments` 支持登录用户评论 | 已完成 |
| 评论 | 回复评论 | `POST /api/comments/{comment_id}/replies` 支持楼中楼回复 | 已完成 |
| 评论 | 删除评论 | `DELETE /api/comments/{comment_id}` 支持作者或管理员删除 | 已完成 |
| 互动 | 帖子点赞 | `POST /api/posts/{post_id}/like` 支持点赞/取消点赞 | 已完成 |
| 互动 | 评论点赞 | `POST /api/comments/{comment_id}/like` 支持评论点赞/取消点赞 | 已完成 |
| 互动 | 收藏帖子 | `POST /api/posts/{post_id}/favorite` 支持收藏/取消收藏 | 已完成 |
| 互动 | 我的收藏 | `GET /api/me/favorites` 分页返回收藏帖子 | 已完成 |
| 互动 | 互动状态 | `GET /api/posts/{post_id}/interaction-status` 返回已点赞、已收藏、已关注作者 | 已完成 |
| 互动 | 特别关注 | `PUT /api/users/{user_id}/follow/star` 支持将关注用户标记为特别关注 | 已完成 |
| 私信 | 私信列表 | `GET /api/me/messages` 返回当前用户站内私信 | 已完成 |
| 私信 | 发送私信 | `POST /api/users/{user_id}/messages` 支持向用户发送站内私信 | 已完成 |
| 举报 | 举报帖子 | `POST /api/posts/{post_id}/report` 写入后台举报处理队列 | 已完成 |
| 举报 | 举报评论 | `POST /api/comments/{comment_id}/report` 写入后台举报处理队列 | 已完成 |
| 关注 | 关注/取消关注 | `POST /api/users/{user_id}/follow` | 已完成 |
| 关注 | 粉丝列表 | `GET /api/users/{user_id}/followers` | 已完成 |
| 关注 | 关注列表 | `GET /api/users/{user_id}/following` | 已完成 |
| Feed | 关注动态 | `GET /api/feed/following` 展示关注用户的新帖 | 已完成 |
| 通知 | 通知列表 | `GET /api/me/notifications` | 已完成 |
| 通知 | 标记已读 | `PUT /api/me/notifications/{notification_id}/read` | 已完成 |
| 群组 | 群组列表 | `GET /api/groups` 支持公开展示群组 | 已完成 |
| 群组 | 创建群组 | `POST /api/groups` 支持公开、审核、私密权限类型 | 已完成 |
| 群组 | 群组详情 | `GET /api/groups/{group_id}` 返回成员数、加入状态和申请状态 | 已完成 |
| 群组 | 加入群组 | `POST /api/groups/{group_id}/join` 支持公开群直接加入、审核群写入申请 | 已完成 |
| 群组 | 退出群组 | `DELETE /api/groups/{group_id}/members/me` | 已完成 |
| 群组 | 群组讨论 | `GET/POST /api/groups/{group_id}/posts` 支持群组内讨论内容 | 已完成 |
| 群组 | 群组资源 | `GET/POST /api/groups/{group_id}/resources` 支持群组资料信息 | 已完成 |
| 通知 | @ 提及通知 | 评论发布流程自动识别 `@昵称` 并生成通知 | 已完成 |
| 前端组件 | 评论组件 | `CommentList.vue`、`CommentEditor.vue` | 已完成 |
| 前端组件 | 点赞收藏按钮 | `LikeButton.vue`、`FavoriteButton.vue` | 已完成 |
| 前端组件 | 关注按钮 | `FollowButton.vue` | 已完成 |
| 前端页面 | 收藏列表页 | `FavoritesView.vue` | 已完成 |
| 前端页面 | 关注动态页 | `FollowingFeedView.vue` | 已完成 |
| 前端页面 | 通知中心页 | `NotificationsView.vue` | 已完成 |
| 前端页面 | 私信页 | `MessagesView.vue` | 已完成 |
| 前端页面 | 群组列表页 | `GroupListView.vue` | 已完成 |
| 前端页面 | 群组详情页 | `GroupDetailView.vue` | 已完成 |
| 前端联动 | 帖子详情接入互动 | 评论、点赞、收藏、举报、关注作者接入帖子详情页 | 已完成 |
| 前端联动 | 用户主页接入关注 | 用户公开主页展示关注关系和关注按钮 | 已完成 |
| 前端联动 | 顶部导航接入互动入口 | 群组、关注、通知、个人中心等入口 | 已完成 |

---

## 三、牟俊臣 - 用户与权限模块

| 分类 | 细分功能 | 具体工作 | 状态 |
|------|----------|----------|------|
| 后端模型 | User 模型 | 用户基础信息、手机号、邮箱、密码哈希、账号状态 | 已完成 |
| 后端模型 | UserProfile 模型 | 昵称、头像、简介、认证等级、风险偏好、影响力值 | 已完成 |
| 后端模型 | Role 模型 | USER、VERIFIED、MODERATOR、ADMIN 角色定义 | 已完成 |
| 后端模型 | UserRole 模型 | 用户和角色多对多关联 | 已完成 |
| 注册认证 | 手机号注册 | `POST /api/auth/register` 支持手机号注册和验证码校验 | 已完成 |
| 注册认证 | 邮箱注册 | `POST /api/auth/register` 支持邮箱注册和验证码校验 | 已完成 |
| 注册认证 | 验证码发送 | `POST /api/auth/verify-code` 提供课程演示用模拟验证码 | 已完成 |
| 注册认证 | 用户登录 | `POST /api/auth/login` 校验账号密码并签发 JWT | 已完成 |
| 注册认证 | 退出登录 | `POST /api/auth/logout` 清理前端登录态 | 已完成 |
| 权限基础 | 当前用户依赖 | `get_current_user` 解析 Bearer Token 并读取用户 | 已完成 |
| 权限基础 | 管理员依赖 | `require_admin` 检查 ADMIN 角色 | 已完成 |
| 认证体系 | 实名认证 | `POST /api/users/me/certification` 支持 REAL_NAME 类型模拟通过 | 已完成 |
| 认证体系 | 专业认证 | `POST /api/users/me/certification` 支持 PROFESSIONAL 类型，提升认证等级 | 已完成 |
| 认证体系 | 风险测评 | `POST /api/users/me/risk-assessment` 根据问卷答案生成风险偏好 | 已完成 |
| 个人资料 | 查看个人中心 | `GET /api/users/me` 返回用户资料、认证、角色和状态 | 已完成 |
| 个人资料 | 编辑资料 | `PUT /api/users/me/profile` 支持昵称、头像、简介、风险偏好 | 已完成 |
| 个人资料 | 资料扩展 | `user_profiles` 支持投资经验、关注市场、隐私设置、积分和等级 | 已完成 |
| 用户主页 | 公开主页 | `GET /api/users/{user_id}` 返回他人公开资料 | 已完成 |
| 用户搜索 | 昵称搜索 | `GET /api/users/search` 支持分页模糊搜索 | 已完成 |
| 管理员 | 用户列表 | `GET /api/admin/users` 支持后台分页查看用户 | 已完成 |
| 管理员 | 用户状态修改 | `PUT /api/admin/users/{user_id}/status` 支持正常、禁言、封禁 | 已完成 |
| 前端 | 登录页 | 登录表单、错误提示、登录后跳转 | 已完成 |
| 前端 | 注册页 | 手机/邮箱注册切换、验证码输入、密码校验提示 | 已完成 |
| 前端 | Token 管理 | `authStore` 和请求拦截器保存并附加 JWT | 已完成 |
| 前端 | 路由守卫 | 未登录访问个人、发帖、后台等页面会跳转登录 | 已完成 |
| 前端 | 个人中心 | 资料展示、资料编辑、认证与互动入口 | 已完成 |
| 前端 | 认证申请页 | 实名/专业认证表单 | 已完成 |
| 前端 | 风险评估页 | 问卷提交与结果展示 | 已完成 |
| 前端 | 用户公开主页 | 资料、关注按钮、关注/粉丝信息入口 | 已完成 |

---

## 四、徐英博 - 论坛内容模块

| 分类 | 细分功能 | 具体工作 | 状态 |
|------|----------|----------|------|
| 后端模型 | Section 模型 | 板块名称、简介、排序、启用状态 | 已完成 |
| 后端模型 | Post 模型 | 帖子标题、正文、作者、类型、状态、浏览/点赞/评论数、精华标识 | 已完成 |
| 后端模型 | Tag 模型 | 股票、基金、主题标签 | 已完成 |
| 后端模型 | PostTag 模型 | 帖子与标签多对多关联 | 已完成 |
| 板块 | 市场讨论区 | A股、港股、美股等默认板块种子数据 | 已完成 |
| 板块 | 主题专区 | 基金、量化、价值投资、新股新债、宏观策略、问答求助等板块 | 已完成 |
| 板块 | 板块查询 | `GET /api/sections`、`GET /api/sections/{id}` | 已完成 |
| 板块 | 板块创建 | `POST /api/sections` 和 `POST /api/admin/sections`，管理员权限保护 | 已完成 |
| 标签 | 标签查询 | `GET /api/tags` 支持按类型筛选 | 已完成 |
| 标签 | 标签创建 | `POST /api/tags` 和 `POST /api/admin/tags`，管理员权限保护 | 已完成 |
| 发帖 | 普通帖子 | `POST /api/posts` 使用当前登录用户作为作者 | 已完成 |
| 发帖 | 长文分析 | `POST /api/posts/analysis` 要求专业认证用户，`post_type=2` | 已完成 |
| 发帖 | 编辑帖子 | `PUT /api/posts/{post_id}` 仅作者或管理员可编辑 | 已完成 |
| 发帖 | 删除帖子 | `DELETE /api/posts/{post_id}` 仅作者或管理员可删除，逻辑删除为 DELETED | 已完成 |
| 查询 | 帖子列表 | `GET /api/posts` 支持分页、板块筛选、关键词搜索 | 已完成 |
| 查询 | 帖子详情 | `GET /api/posts/{post_id}` 返回作者、认证等级、标签和完整正文 | 已完成 |
| 搜索 | 全文搜索 | `GET /api/search/posts` 按标题和正文模糊搜索 | 已完成 |
| 搜索 | 搜索建议 | `GET /api/search/suggestions` 返回搜索建议 | 已完成 |
| 热榜 | 热门帖子 | `GET /api/posts/hot` 按浏览、点赞、评论加权排序 | 已完成 |
| 热榜 | 热议话题 | `GET /api/hot-topics` 返回每日和每周热议话题 | 已完成 |
| 附件 | 帖子附件 | `GET/POST /api/posts/{post_id}/attachments` 支持帖子附件信息 | 已完成 |
| 投票 | 投票帖 | `POST /api/posts/{post_id}/poll-options`、`POST /api/poll-options/{option_id}/vote` 支持投票选项和投票 | 已完成 |
| 前端 | 首页 | 展示核心板块、最新帖子和热门讨论 | 已完成 |
| 前端 | 板块列表页 | 展示全部板块卡片 | 已完成 |
| 前端 | 板块详情页 | 展示指定板块帖子列表 | 已完成 |
| 前端 | 帖子详情页 | 展示帖子正文、标签、作者和互动区域 | 已完成 |
| 前端 | 发帖页 | 支持普通帖子和长文分析入口 | 已完成 |
| 前端 | 搜索结果页 | 展示关键词搜索结果 | 已完成 |
| 前端 | 热榜页 | 展示热门讨论排行 | 已完成 |

---

## 五、周颂捷 - 审核与后台模块

| 分类 | 细分功能 | 具体工作 | 状态 |
|------|----------|----------|------|
| 后端模型 | AuditQueueItem | 内容审核队列条目 | 已完成 |
| 后端模型 | ReportItem | 用户举报处理条目 | 已完成 |
| 后端模型 | SensitiveWord | 敏感词规则、风险等级、处理动作 | 已完成 |
| 后端模型 | UserModerationRecord | 用户处罚记录 | 已完成 |
| 启动数据 | 后台演示数据 | `seed_admin_demo_data` 写入用户、帖子、评论、群组、审核、举报、敏感词等演示数据 | 已完成 |
| 后台概览 | 统计卡片 | `GET /api/admin/overview` | 已完成 |
| 内容审核 | 审核队列列表 | `GET /api/admin/audit-queue` | 已完成 |
| 内容审核 | 审核处理 | `PATCH /api/admin/audit-queue/{item_id}` 支持通过、驳回等状态 | 已完成 |
| 举报处理 | 举报列表 | `GET /api/admin/reports` | 已完成 |
| 举报处理 | 举报处置 | `PATCH /api/admin/reports/{item_id}` 支持驳回、警告、封禁等动作 | 已完成 |
| 敏感词 | 敏感词列表 | `GET /api/admin/sensitive-words` | 已完成 |
| 敏感词 | 启停规则 | `PATCH /api/admin/sensitive-words/{word_id}` | 已完成 |
| 自动审核 | 发帖入队 | 发帖时检测敏感词和重复标题，命中后写入 `audit_queue_items` | 已完成 |
| 用户管理 | 用户处罚记录 | `GET /api/admin/user-moderation` | 已完成 |
| 数据分析 | 后台统计 | `GET /api/admin/statistics` 返回热门话题和活跃板块摘要 | 已完成 |
| 板块维护 | 板块更新删除 | `PUT/DELETE /api/admin/sections/{id}` 支持后台维护板块 | 已完成 |
| 标签维护 | 标签更新删除 | `PUT/DELETE /api/admin/tags/{id}` 支持后台维护标签 | 已完成 |
| 权限保护 | 管理员接口保护 | 后台接口统一依赖 `require_admin` | 已完成 |
| 前端布局 | 后台布局 | `AdminLayout.vue` 左侧菜单和主工作区 | 已完成 |
| 前端页面 | 后台概览页 | `AdminDashboard.vue` | 已完成 |
| 前端页面 | 审核管理页 | `AdminAuditView.vue` | 已完成 |
| 前端页面 | 举报处理页 | `AdminReportsView.vue` | 已完成 |
| 前端页面 | 敏感词管理页 | `AdminSensitiveWordsView.vue` | 已完成 |
| 前端页面 | 用户处置页 | `AdminModerationView.vue` | 已完成 |
| 前端页面 | 统计页 | `AdminStatisticsView.vue` | 已完成 |
| 前端权限 | 后台路由守卫 | `meta.requiresAdmin` 限制非管理员进入后台页面 | 已完成 |
| 前端权限 | 后台入口控制 | 普通用户隐藏后台导航，管理员显示后台入口 | 已完成 |

---

## 六、模块三最终检查结果

| 检查项 | 命令或方式 | 结果 |
|------|------|------|
| 后端编译检查 | `python -m compileall backend\app` | 通过 |
| 后端烟测 | `$env:PYTHONPATH=(Resolve-Path 'backend\venv_lib').Path + ';' + (Resolve-Path 'backend').Path; python scripts\backend_smoke_test.py` | 32 项通过，0 项失败 |
| 前端构建 | `cd frontend && npm run build` | 通过 |
| 依赖安装 | `npm ci`、`python -m pip install --upgrade --target backend\venv_lib -r backend\requirements.txt` | 通过，依赖目录均被 `.gitignore` 忽略 |

模块三编码实现已完成。用户资料扩展、附件、投票、搜索建议、热议话题、特别关注、私信、@ 提及通知、群组讨论、群组资源、板块标签维护和内容自动审核入队等工作均已并入对应成员模块表中，作为已完成工作统一呈现。

最新复测命令：

```bash
python -m compileall backend\app
$env:PYTHONPATH=(Resolve-Path 'backend\venv_lib').Path + ';' + (Resolve-Path 'backend').Path; python scripts\backend_smoke_test.py
cd frontend && npm run build
```

最新复测结果：后端编译通过，后端冒烟测试 32 项全部通过，前端 `vue-tsc --noEmit` 与 `vite build` 通过。
