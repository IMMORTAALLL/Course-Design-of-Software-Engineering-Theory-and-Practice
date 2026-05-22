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



### 三、用户与权限前端实现

#### 原始提示词

```text
根据当前项目方向和已有代码，完成牟俊臣负责的用户与权限模块。项目后端已经使用 FastAPI + SQLAlchemy 实现了注册、登录、用户资料、认证申请和风险测评接口，前端使用 Vue 3 + Vite + TypeScript。请补齐前端 auth 模块，包括接口封装、登录态保存、路由守卫、登录页、注册页、个人中心、认证申请页、风险测评页和用户公开主页，并和现有论坛页面风格保持一致。
```

#### AI输出摘要

AI 根据已有后端接口和前端项目结构，补充了用户与权限模块前端实现：

- `frontend/src/modules/auth/api/authApi.ts`：封装注册、登录、登出、验证码、当前用户、资料修改、认证申请、风险测评、用户公开主页等接口
- `frontend/src/modules/auth/types/auth.ts`：定义用户、登录、注册、认证、风险测评等 TypeScript 类型
- `frontend/src/modules/auth/stores/authStore.ts`：管理 JWT Token、当前用户、登录态持久化和退出登录
- `LoginView.vue`、`RegisterView.vue`：完成登录注册页面和表单校验
- `ProfileView.vue`：完成个人中心资料查看和修改
- `CertificationView.vue`：完成实名/专业认证申请
- `RiskAssessmentView.vue`：完成风险偏好问卷提交
- `UserPublicView.vue`：完成用户公开主页展示
- `frontend/src/shared/router/index.ts`：补充 auth 路由和登录态守卫
- `frontend/src/shared/api/request.ts`：请求自动携带 `Authorization: Bearer token`
- `frontend/src/App.vue`：顶部导航根据登录状态展示登录/注册或个人中心/退出

#### 人工检查

1. 初始检查发现 `frontend/node_modules` 未安装，`npm run build` 找不到 `vue-tsc`，先执行 `npm install` 后再构建。
2. `npm install` 引起了 `package-lock.json` 的本地扰动，但不是本次功能内容，因此恢复锁文件，避免提交无关修改。
3. 检查用户与权限前端接口路径，确保与后端已有 `/api/auth/*`、`/api/users/*` 路由保持一致。
4. 检查受保护路由 `/me`、`/me/certification`、`/me/risk-assessment`，未登录时会跳转到 `/login`。

#### 迭代优化

补充请求拦截器自动添加 JWT Token，统一处理 40101、40102 登录态失效。将登录状态封装到 `authStore` 中，刷新页面后可以从 `localStorage` 恢复登录态。最后运行 `npm run build`，前端 TypeScript 检查和 Vite 生产构建均通过。
