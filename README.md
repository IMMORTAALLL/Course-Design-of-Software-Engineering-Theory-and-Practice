# 《软件工程理论与实践》课程设计

## 题目三：股票基金投资论坛

## 项目名称：智投社区

||姓名|班级|学号|GitHub账号|
|--|--|--|--|--|
|负责人|谢亨义|软件2401班|U202411368|IMMORTAALLL|
|小组成员|周颂捷|软件2401班|U202415511|shenglaiyaoyan|
|小组成员|徐英博|软件2401班|U202413068|xyb-Corder|
|小组成员|牟俊臣|软件2401班|U202316388|mmmmermer|

## 项目简介

智投社区是一个面向股票基金投资者的综合性论坛平台，支持多市场讨论（A股、港股、美股、基金等）、投资观点分享、社交互动、群组交流以及后台内容审核管理。系统采用前后端分离架构，后端使用 Python FastAPI，前端使用 Vue 3。

## 技术栈

| 层级 | 技术选型 |
|------|----------|
| 后端框架 | Python FastAPI + SQLAlchemy |
| 前端框架 | Vue 3 + Vite + TypeScript + Element Plus |
| 数据库 | MySQL 8.0 |
| 认证方式 | JWT Bearer Token |
| 密码加密 | bcrypt |

## 模块分工

| 成员 | 分支 | 负责模块 | 主要目录 |
| --- | --- | --- | --- |
| 牟俊臣 | `feature/auth-user` | 用户与权限模块 | `backend/app/modules/auth`、`frontend/src/modules/auth` |
| 徐英博 | `feature/forum-content` | 论坛内容模块 | `backend/app/modules/forum`、`frontend/src/modules/forum` |
| 谢亨义 | `feature/social-interaction` | 社交互动模块 | `backend/app/modules/interaction`、`frontend/src/modules/interaction` |
| 周颂捷 | `feature/admin-audit` | 审核与后台模块 | `backend/app/modules/admin`、`frontend/src/modules/admin` |

---

## 模块一：项目启动与AI辅助需求分析

本模块完成了项目选题确认、团队分组、仓库搭建，并通过AI辅助完成了用户故事和交互场景的编写。

### 主要产出

- 明确了系统五大功能模块：用户系统、内容系统、社交与关系系统、信息整合系统、管理运营系统
- 为每个功能模块编写了用户故事（按"作为…我想…以便…"格式）
- 为每个用户故事生成了详细的交互场景描述

### 文档链接

| 文档 | 说明 |
|------|------|
| [用户故事](（模块1）user_stories.md) | 各功能模块的用户故事集合 |
| [交互场景](（模块1）use_cases.md) | 基于用户故事的详细交互场景 |
| [AI使用记录](（模块1）ai.md) | 模块一中与AI的交互过程记录 |
| [分工记录](（模块1）assign.md) | 模块一团队成员完成情况 |

---

## 模块二：AI辅助设计

本模块完成了系统的架构设计、数据库设计、后端接口设计和前端UI设计，为编码实现阶段提供了完整的技术蓝图。

### 主要产出

- **架构设计**：确定前后端分离架构，后端分层（Controller → Service → Mapper），模块化业务拆分
- **数据库设计**：完成全部核心表结构设计（用户、帖子、评论、关注、群组、审核等），提供完整建表SQL脚本
- **接口设计**：设计了覆盖全部业务的 RESTful API（共40+接口），提供 OpenAPI 3.0 YAML 规范
- **UI设计**：完成各页面的布局设计和交互流程

### 文档链接

| 文档 | 说明 |
|------|------|
| [架构和类设计](（模块2）architect.md) | 系统总体架构、分层设计、模块划分、核心类图 |
| [数据库设计](（模块2）db.md) | ER图、数据字典、完整建表脚本 |
| [后端接口文档](（模块2）backend_api.md) | RESTful API设计、统一响应格式、错误码、OpenAPI YAML |
| [前端UI设计](（模块2）ui_design.md) | 页面布局、组件设计、交互流程 |
| [AI使用记录](（模块2）ai.md) | 模块二中与AI的交互过程记录 |
| [分工记录](（模块2）assign.md) | 模块二团队成员完成情况 |

---

## 快速启动

开发环境默认使用本地 SQLite。首次启动后端时会自动创建 `backend/forum_system.db`，并写入板块、标签、帖子、评论、群组、通知和后台审核等演示数据。

### 后端

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
| 普通用户 | `value@stockforum.com` | 可发帖、评论、关注、收藏和加入群组 |
| 专业用户 | `quant@stockforum.com` | 可演示专业认证和长文分析内容 |

如需连接 MySQL，可复制 `backend/.env.example` 为 `backend/.env`，修改 `DATABASE_URL` 后再导入 `database/schema.sql` 和 `database/seed.sql`。

### 前端

```bash
cd frontend
npm install
npm run dev
```

启动后访问 http://127.0.0.1:5173 。Vite 会将 `/api` 代理到 `http://127.0.0.1:8000`，如后端端口不同，可通过 `VITE_API_PROXY_TARGET` 覆盖。
