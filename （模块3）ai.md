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