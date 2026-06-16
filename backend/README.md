# 后端项目说明

后端使用 Python FastAPI + SQLAlchemy + JWT。开发阶段默认使用项目内 SQLite，联调或部署时可以切换到 MySQL。

## 技术栈

- Python 3.10+
- FastAPI 0.115
- SQLAlchemy 2.0（同步模式）
- SQLite（默认开发）
- MySQL 8.0（可选）
- JWT 认证（python-jose）
- 密码加密（passlib + bcrypt）

## 快速启动

开发环境默认使用项目内 SQLite。首次启动后会自动创建 `backend/forum_system.db`，并写入用户、板块、帖子、评论、群组、通知和后台审核演示数据。

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

启动后访问 http://127.0.0.1:8000/docs 查看接口文档。

演示账号密码均为 `Admin123456`：

| 角色 | 邮箱 | 说明 |
| --- | --- | --- |
| 管理员 | `admin@stockforum.com` | 可访问后台审核、举报、敏感词和用户管理 |
| 普通用户 | `value@stockforum.com` | 可演示发帖、评论、关注、收藏和群组流程 |
| 专业用户 | `quant@stockforum.com` | 可演示专业认证、长文分析和量化主题内容 |

如需使用 MySQL，可复制 `.env.example` 为 `.env`，修改 `DATABASE_URL` 后再导入 `database/schema.sql` 和 `database/seed.sql`。

## 模块所有权

| 模块 | 负责人 | 目录 |
| --- | --- | --- |
| 用户与权限 | 成员A | `app/modules/auth` |
| 论坛内容 | 成员B | `app/modules/forum` |
| 社交互动 | 成员C | `app/modules/interaction` |
| 审核后台 | 成员D | `app/modules/admin` |

## 目录结构

```text
backend/
├── app/
│   ├── main.py          # FastAPI 入口
│   ├── config.py        # 配置（从 .env 读取）
│   ├── database.py      # 数据库连接
│   ├── common/          # 通用组件（响应、异常、依赖）
│   ├── security/        # JWT、密码工具
│   └── modules/         # 业务模块
├── requirements.txt
└── .env.example
```

## 模块内部结构约定

每个模块内部按以下结构组织：

```text
models.py      # SQLAlchemy 模型
schemas.py     # Pydantic 请求/响应模型
service.py     # 业务逻辑
router.py      # API 路由
```

公共代码放在 `common/`、`security/` 中。修改公共代码前需要在小组内说明影响范围。
