# 软件安装文档

项目名称：智投社区：股票基金投资论坛系统

本文档对应指导书模块五“上线部署与报告撰写”中软件安装文档 `install.md` 的提交要求，说明本系统在本地环境中的安装、启动、验证和常见问题处理方法。指导书要求本地部署，鼓励云上部署；本文以本地部署为主，同时列出当前云端演示访问方式。

## 一、系统概述

智投社区采用前后端分离架构：

| 层级 | 技术 |
| --- | --- |
| 前端 | Vue 3 + Vite + TypeScript |
| 后端 | Python FastAPI + SQLAlchemy |
| 数据库 | SQLite 默认演示库，可选 MySQL 8.0 |
| 认证 | JWT Bearer Token |
| 接口文档 | FastAPI Swagger UI |

本地部署完成后：

| 服务 | 默认地址 |
| --- | --- |
| 前端页面 | `http://127.0.0.1:5173` |
| 后端接口 | `http://127.0.0.1:8000/api` |
| 接口文档 | `http://127.0.0.1:8000/docs` |
| 健康检查 | `http://127.0.0.1:8000/api/health` |

## 二、环境要求

| 环境 | 要求 |
| --- | --- |
| 操作系统 | Windows 10/11、macOS 或 Linux |
| Python | 推荐 Python 3.10 及以上 |
| Node.js | 推荐 Node.js 18 及以上 |
| 包管理工具 | `pip`、`npm` |
| 浏览器 | Chrome、Edge 或其他现代浏览器 |
| 数据库 | 默认 SQLite，无需额外安装；MySQL 为可选部署 |

安装前可检查版本：

```powershell
python --version
node --version
npm --version
```

## 三、获取项目代码

使用 Git 克隆仓库：

```powershell
git clone https://github.com/IMMORTAALLL/Course-Design-of-Software-Engineering-Theory-and-Practice.git
cd Course-Design-of-Software-Engineering-Theory-and-Practice
```

如果已经有本地仓库，更新到最新版本：

```powershell
git pull --ff-only
```

## 四、后端安装与启动

进入后端目录：

```powershell
cd backend
```

安装依赖：

```powershell
python -m pip install -r requirements.txt
```

启动后端服务：

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

启动成功后，在浏览器访问：

```text
http://127.0.0.1:8000/api/health
```

正常返回示例：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "status": "ok"
  }
}
```

接口文档访问地址：

```text
http://127.0.0.1:8000/docs
```

首次启动时，系统会使用 SQLite 创建或复用 `backend/forum_system.db`，并写入用户、板块、帖子、评论、群组、通知、审核和举报等演示数据。

## 五、前端安装与启动

打开新的终端，从项目根目录进入前端目录：

```powershell
cd frontend
```

安装依赖：

```powershell
npm install
```

启动开发服务器：

```powershell
npm run dev
```

前端启动后访问：

```text
http://127.0.0.1:5173
```

Vite 开发环境会将 `/api` 请求代理到后端服务。若后端端口不是 `8000`，可设置环境变量 `VITE_API_PROXY_TARGET` 调整代理目标。

## 六、演示账号

演示账号密码均为：

```text
Admin123456
```

| 角色 | 邮箱 | 说明 |
| --- | --- | --- |
| 管理员 | `admin@stockforum.com` | 可进入后台管理、审核、举报、敏感词、统计等页面 |
| 普通用户 | `value@stockforum.com` | 可发帖、评论、点赞、收藏、关注、加入群组 |
| 专业用户 | `quant@stockforum.com` | 可演示专业认证和长文分析发布 |

## 七、安装验证

### 1. 后端编译检查

从项目根目录执行：

```powershell
python -m compileall backend\app
```

通过表现：终端正常列出后端目录，无语法错误和异常退出。

### 2. 前端构建检查

进入前端目录执行：

```powershell
cd frontend
npm run build
```

通过表现：终端输出 `built` 或构建完成信息，生成 `frontend/dist` 目录。

### 3. 接口健康检查

访问：

```text
http://127.0.0.1:8000/api/health
```

通过表现：返回 `code=0` 和 `status=ok`。

### 4. 页面访问检查

访问：

```text
http://127.0.0.1:5173
```

通过表现：浏览器显示“智投社区”首页，可看到板块、帖子、热榜、群组、登录注册等入口。

## 八、可选 MySQL 部署

默认情况下系统使用 SQLite，适合课程演示和本机复现。如果需要使用 MySQL：

1. 安装 MySQL 8.0。
2. 创建数据库，例如 `stock_forum`。
3. 复制配置文件：

```powershell
copy backend\.env.example backend\.env
```

4. 修改 `backend/.env` 中的数据库连接：

```env
DATABASE_URL=mysql+pymysql://用户名:密码@127.0.0.1:3306/stock_forum?charset=utf8mb4
```

5. 按需要导入：

```text
database/schema.sql
database/seed.sql
```

6. 重新启动后端服务。

## 九、云端演示地址

当前项目已部署到阿里云服务器，供课程展示截图和演示使用：

| 项目 | 地址 |
| --- | --- |
| 前端页面 | `http://8.148.72.200/` |
| API 健康检查 | `http://8.148.72.200/api/health` |
| Swagger 接口文档 | `http://8.148.72.200/docs` |

云端部署不替代指导书要求的本地部署，本地部署仍按本文档前述步骤完成。

## 十、常见问题

### 1. 后端提示依赖缺失

原因：未安装 `backend/requirements.txt` 中的 Python 依赖。

处理方式：

```powershell
cd backend
python -m pip install -r requirements.txt
```

### 2. 端口被占用

如果 `8000` 或 `5173` 被占用，可更换端口。

后端示例：

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8010
```

前端示例：

```powershell
npm run dev -- --port 5174
```

### 3. 前端请求后端失败

检查后端是否启动，并确认前端代理目标与后端端口一致。开发环境默认后端地址为 `http://127.0.0.1:8000`。

### 4. 登录失败

检查账号、密码是否正确。演示账号统一密码为 `Admin123456`。如果数据库被删除或重置，重新启动后端会写入演示数据。

### 5. 构建失败

先删除旧依赖并重新安装：

```powershell
cd frontend
npm install
npm run build
```

如果仍失败，检查 Node.js 版本是否满足要求。

## 十一、安装结论

按照本文档完成后端依赖安装、前端依赖安装、服务启动和验证后，系统可以在本地完成课程演示。系统支持游客浏览、用户登录注册、论坛发帖、评论互动、群组交流、通知私信和后台审核管理等功能。
