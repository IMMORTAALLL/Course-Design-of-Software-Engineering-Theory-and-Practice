# AI 使用记录

## 模块三：AI辅助编码实现

### 一、项目框架搭建

#### 原始提示词

```text
开始做模块三的代码构建。项目"智投社区"需要搭建后端基础框架。后端根据文档中的用Python FastAPI+SQLAlchemy+MySQL，前端用Vue3+Vite+TypeScript+Element Plus。先搭后端骨架，包括：FastAPI 入口、配置管理、数据库连接、统一响应格式、自定义异常体系、JWT认证、bcrypt密码加密。
```

#### AI输出摘要

AI生成了后端项目骨架原型，包括以下核心文件：

- `app/main.py`：FastAPI 应用入口，配置 CORS 中间件，注册全局异常处理器
- `app/config.py`：使用 pydantic-settings 从 .env 文件加载配置
- `app/database.py`：SQLAlchemy 引擎和会话管理
- `app/common/response.py`：统一响应格式 `{"code": 0, "message": "success", "data": {}}`
- `app/common/exceptions.py`：自定义异常类（40001参数错误、40101未登录、40102Token无效、40301权限不足、40901资源冲突、50001系统错误）
- `app/common/deps.py`：FastAPI 依赖注入（get_db、get_current_user）
- `app/security/jwt.py`：JWT 令牌创建和验证
- `app/security/password.py`：bcrypt 密码哈希和校验

#### 人工检查

1. 初始方案使用了异步 SQLAlchemy，但不是太需要异步复杂度，改为同步模式+pymysql更简单可靠
2. AI最初将依赖安装到本地的Anaconda base环境中，要让ai删除并且直接将环境下到项目目录中用pythonpath来使用
3. 统一响应的成功码用了200，要改为之前写的文档中的0

#### 迭代优化

将 SQLAlchemy 从异步改为同步模式，降低复杂度，修改依赖安装方式为 `pip install --target=./venv_lib`，成功响应码从 200 改为 0，与接口设计文档保持一致，添加`RequestValidationError` 处理器，确保 Pydantic 参数校验错误也返回统一格式



### 二、数据模型定义

#### 原始提示词

```text
根据（模块2）db.md中的数据库设计，创建 SQLAlchemy 模型，用户系统需要 User、UserProfile 两个模型，对应 users 和 user_profiles表。添加Role和UserRole模型支持角色权限体系同时更新database/schema.sql完整建表脚本。
```

#### AI输出摘要

AI 生成了 `app/modules/auth/models.py`，包含四个 SQLAlchemy 模型：

- `User`：用户基础表，包含 id、phone、email、password_hash、status、created_at、updated_at
- `UserProfile`：用户资料表（与 User 1:1），包含 nickname、avatar_url、bio、auth_level、risk_preference、influence_score
- `Role`：角色表，包含 name（USER/VERIFIED/MODERATOR/ADMIN）和 description
- `UserRole`：用户角色关联表（多对多）

同时更新了 `database/schema.sql`，包含全部5个模块的建表脚本，以及 `database/seed.sql` 初始化角色和板块数据。

#### 人工检查

AI使用了`str | None` 类型语法，但环境是Python3.9，不支持该语法

#### 迭代优化

将 `str | None` 改为 `Optional[str]`，兼容Python3.9



### 三、ABCD 模块整合与缺口检查

#### 原始提示词

```text
接管ABCD全部任务，按照对应任务分配完成之后进行提交，便于到时候提交四分工作任务与报告。先拉取最新仓库，分析整个项目现状，禁止虚构。
```

#### AI输出摘要

AI 先执行 `git fetch --all --prune`、`git pull --ff-only origin main`、`git status --short --branch`，确认当前 `main`、`docx` 与远端 `origin/main` 均位于同一提交，工作区干净。随后读取 README、模块二后端接口文档、模块二 UI 设计文档、后端 `main.py`、各模块路由、前端路由和页面文件，得到真实现状：

- 成员 A 用户与权限模块已有注册、登录、个人中心、认证申请、风险测评和用户公开主页。
- 成员 B 论坛内容模块已有板块、帖子、搜索、热榜和发帖页面，但普通发帖接口仍固定使用 `user_id=1`。
- 成员 C 社交互动模块目录只有占位文件，评论、点赞、收藏、关注、通知和群组功能缺失。
- 成员 D 后台审核模块已有后台概览、审核、举报、敏感词、用户处置和统计页面，并已经接入管理员权限。

#### 人工检查

不能只按聊天记录判断任务完成情况，必须以仓库代码和远端状态为准。检查时发现旧 `HANDOFF.md` 中的端口、分支和未提交状态已经过时，因此最终判断以当前 Git 命令和源码读取结果为准。

#### 迭代优化

将后续工作拆成三类：先修正 B 模块登录发帖和长文分析接口，再补齐 C 模块完整社交互动闭环，最后做 A/D 入口联动、文档更新和完整测试。


### 四、社交互动模块实现

#### 原始提示词

```text
根据模块二接口文档和 UI 设计，完成成员 C 社交互动模块。需要覆盖评论、回复、点赞、收藏、关注、通知、群组，并与帖子详情、用户主页、个人中心联动。
```

#### AI输出摘要

AI 新增了 `backend/app/modules/interaction` 的模型、请求结构、服务和路由：

- `Comment`：帖子评论和楼中楼回复。
- `UserAction`：帖子/评论点赞、帖子收藏。
- `UserFollow`：用户关注关系。
- `Group`、`GroupMember`：投资主题群组和群成员。
- `Notification`：评论、点赞、关注、群组等通知。

后端接口覆盖：

- `GET/POST /api/posts/{post_id}/comments`
- `POST /api/comments/{comment_id}/replies`
- `POST /api/posts/{post_id}/like`
- `POST /api/posts/{post_id}/favorite`
- `GET /api/me/favorites`
- `POST /api/users/{user_id}/follow`
- `GET /api/users/{user_id}/followers`
- `GET /api/users/{user_id}/following`
- `GET /api/feed/following`
- `GET /api/me/notifications`
- `PUT /api/me/notifications/{id}/read`
- `GET/POST /api/groups`
- `GET /api/groups/{id}`
- `POST /api/groups/{id}/join`
- `DELETE /api/groups/{id}/members/me`

前端新增 `frontend/src/modules/interaction` 下的 API、类型、组件和页面，包括评论编辑器、评论列表、点赞按钮、收藏按钮、关注按钮、群组卡片、通知中心、收藏列表、关注动态、群组列表和群组详情。

#### 人工检查

实现时需要避免另起一套与设计文档不一致的数据结构，因此优先复用 `database/schema.sql` 中已经设计的 `comments`、`user_actions`、`user_follows`、`groups`、`group_members` 表。通知功能在数据库脚本中缺少对应表，补充了 `notifications` 表和演示数据。

#### 迭代优化

完成后使用 Python 3.12 临时 SQLite 数据库和 FastAPI TestClient 测试 21 个接口场景，包括登录发帖、长文权限、评论回复、点赞收藏、关注动态、通知已读和群组加入。测试结果为 21 项通过，0 项失败。


### 五、论坛内容与用户入口联动

#### 原始提示词

```text
完成项目要求中 A/B/C/D 的联动，检查是否符合开发文档要求。
```

#### AI输出摘要

AI 对已有模块做了必要联动：

- 将 `POST /api/posts` 从固定 `user_id=1` 改为使用当前登录用户。
- 新增 `POST /api/posts/analysis`，要求专业认证用户才能发布长文分析。
- 帖子列表和详情返回作者昵称、作者认证等级、帖子类型和精华标识。
- 发帖页增加普通帖子/长文分析选择。
- 帖子详情页接入作者主页、关注作者、点赞、收藏、评论和回复。
- 用户公开主页接入关注按钮、粉丝列表和关注列表。
- 个人中心增加通知中心、我的收藏、关注动态和投资群组入口。
- 顶部导航增加群组、关注动态和通知入口。

#### 人工检查

前端项目实际没有使用 Element Plus，而是已有原生 Vue + CSS 风格，因此新增页面和组件沿用现有 `.page`、`.panel`、`.stack`、`.primary-button` 等样式，不额外引入 UI 库。

#### 迭代优化

执行 `npm run build`，通过 `vue-tsc --noEmit` 和 `vite build`，确认新增页面、路由和类型定义不会阻塞前端构建。


### 六、权限与互动闭环加固

#### 原始提示词

```text
进行全面专业的检查和测试。禁止虚构，对照整个项目要求审核遗漏，发现问题后补齐。
```

#### AI输出摘要

AI 在补充审核中发现板块、标签写接口虽然已实现，但需要进一步与管理员权限要求对齐；帖子详情页已有点赞、收藏、关注按钮，但缺少登录用户的初始状态回显；设计文档中存在帖子和评论举报接口，前端入口和后端持久化需要补齐；需审核群组不应直接写入正式成员。

随后补充：

- 为 `POST /api/sections`、`POST /api/tags` 增加管理员权限保护。
- 增加 `/api/admin/sections`、`/api/admin/tags`，与模块二接口文档的后台路径保持一致。
- 增加 `GET /api/posts/{id}/interaction-status`，用于帖子详情页回显点赞、收藏和关注作者状态。
- 增加 `POST /api/posts/{id}/report`、`POST /api/comments/{id}/report`，写入后台 `report_items`。
- 增加 `group_join_requests`，使需审核群组的加入申请保持 `pending` 状态，不直接写入 `group_members`。
- 为本地 SQLite 旧库启动补齐新增字段和新增表，避免旧数据库因缺列报错。

#### 人工检查

这些补充只记录已经落地并测试过的功能。群组申请目前实现到“提交申请并保持待审核状态”，没有虚构管理员审批通过/驳回页面。

#### 迭代优化

最终执行 `git diff --check`、`python -m compileall backend\app`、`npm run build` 和 Python 3.12 临时 SQLite FastAPI TestClient 回归。接口回归结果为 35 项通过，0 项失败。
