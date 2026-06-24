# 《软件工程理论与实践》课程设计

## 题目三：股票基金投资论坛

## 项目名称：智投社区

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg)
![Vue](https://img.shields.io/badge/Vue-3.x-brightgreen.svg)
![Vite](https://img.shields.io/badge/Vite-5.x-purple.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-Development-lightgrey.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![JWT](https://img.shields.io/badge/JWT-Auth-black.svg)
![bcrypt](https://img.shields.io/badge/bcrypt-Password%20Hashing-yellow.svg)


## 云端演示地址：
本项目已实现在云服务器部署

[http://8.148.72.200/](http://8.148.72.200/)

演示账号密码均为：

```text
Admin123456
```

| 角色 | 邮箱 | 可使用功能 |
| --- | --- | --- |
| 管理员 | `admin@stockforum.com` | 普通用户功能 + 后台管理、审核、举报处理、敏感词、统计 |
| 普通用户 | `value@stockforum.com` | 登录、个人中心、发帖、评论、点赞、收藏、关注、群组、通知、私信 |
| 专业用户 | `quant@stockforum.com` | 普通用户功能 + 专业认证、长文分析演示 |
| 游客 | 无需登录 | 首页、板块、帖子详情、搜索结果、热榜、公开群组浏览 |

## 项目成员：
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
| 前端框架 | Vue 3 + Vite + TypeScript |
| 数据库 | SQLite（默认开发）/ MySQL 8.0（可选部署） |
| 认证方式 | JWT Bearer Token |
| 密码加密 | bcrypt |

## 项目结构

本项目已完成前后端分离基础架构、数据库脚本、课程设计文档、测试截图和部署交付材料，主要目录结构如下：

```text
Course-Design-of-Software-Engineering-Theory-and-Practice/
├── README.md                         # 项目总说明
├── （模块1）user_stories.md          # 用户故事
├── （模块1）use_cases.md             # 交互场景
├── （模块1）ai.md                    # 模块一 AI 使用记录
├── （模块1）assign.md                # 模块一分工记录
├── （模块2）architect.md             # 架构与类设计
├── （模块2）backend_api.md           # 后端接口设计
├── （模块2）db.md                    # 数据库设计
├── （模块2）ui_design.md             # 前端 UI 设计
├── （模块2）ai.md                    # 模块二 AI 使用记录
├── （模块2）assign.md                # 模块二分工记录
├── （模块3）ai.md                    # 编码实现阶段 AI 使用记录
├── （模块3）assign.md                # 模块三分工记录
├── （模块4）test.md                  # 测试报告
├── （模块4）ai.md                    # 测试调试阶段 AI 使用记录
├── （模块4）assign.md                # 模块四分工记录
├── （模块5）install.md               # 本地部署说明
├── （模块5）user_guid.md             # 软件使用说明书
├── （模块5）ai.md                    # 部署交付阶段 AI 使用记录
├── （模块5）assign.md                # 模块五分工记录
├── backend/                          # FastAPI 后端项目
│   ├── README.md                     # 后端说明
│   ├── requirements.txt              # Python 依赖
│   ├── .env.example                  # 环境变量示例
│   └── app/
│       ├── main.py                   # FastAPI 应用入口
│       ├── config.py                 # 配置读取
│       ├── database.py               # 数据库连接与会话
│       ├── common/                   # 统一响应、异常、依赖等通用代码
│       ├── security/                 # JWT、密码加密等安全工具
│       └── modules/                  # 后端业务模块
│           ├── auth/                 # 用户、登录、权限、认证、风险测评
│           ├── forum/                # 板块、帖子、标签、搜索、热榜、投票、附件
│           ├── interaction/          # 评论、点赞、收藏、关注、通知、私信、群组
│           └── admin/                # 后台概览、审核、举报、敏感词、统计
├── frontend/                         # Vue 3 + Vite + TypeScript 前端项目
│   ├── README.md                     # 前端说明
│   ├── package.json                  # 前端依赖与脚本
│   ├── vite.config.ts                # Vite 配置与 API 代理
│   ├── index.html                    # 前端 HTML 入口
│   └── src/
│       ├── main.ts                   # Vue 应用入口
│       ├── App.vue                   # 全局布局与顶部导航
│       ├── shared/                   # 公共请求封装、路由、样式和后台布局
│       └── modules/                  # 前端业务模块
│           ├── auth/                 # 登录、注册、个人中心、认证、风险测评、用户主页
│           ├── forum/                # 首页、板块、发帖、帖子详情、搜索、热榜
│           ├── interaction/          # 评论组件、收藏、关注、通知、私信、群组
│           └── admin/                # 后台首页、审核、举报、敏感词、用户处罚、统计
├── database/                         # 数据库脚本
│   ├── README.md                     # 数据库说明
│   ├── schema.sql                    # 建表脚本
│   └── seed.sql                      # 演示数据
├── scripts/                          # 辅助脚本
│   ├── README.md                     # 脚本说明
│   └── backend_smoke_test.py         # 后端核心接口烟测脚本
└── figs/                             # 项目截图与 AI 迭代截图
    ├── e2e-20260617/                # 浏览器联调截图
    ├── （模块1）ai-image*.png        # 模块一 AI 记录截图
    └── （模块2）ai-*.png             # 模块二 AI 记录截图
```

## 模块分工

| 成员 | 分支 | 负责模块 | 主要目录 |
| --- | --- | --- | --- |
| 谢亨义（负责人） | `feature/social-interaction` | 社交互动模块、整体整合与交付统筹 | `backend/app/modules/interaction`、`frontend/src/modules/interaction` |
| 牟俊臣 | `feature/auth-user` | 用户与权限模块 | `backend/app/modules/auth`、`frontend/src/modules/auth` |
| 徐英博 | `feature/forum-content` | 论坛内容模块 | `backend/app/modules/forum`、`frontend/src/modules/forum` |
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

## 模块三：AI辅助编码实现

本模块完成了前后端项目代码、数据库脚本和核心业务流程实现。系统支持用户认证、论坛内容、社交互动、群组交流、后台审核等主要功能，并补齐附件、投票、搜索建议、热议话题、私信、群组资源和自动审核入队等扩展入口。

### 主要产出

- **后端实现**：FastAPI 路由、SQLAlchemy 模型、业务服务、统一响应和权限依赖
- **前端实现**：Vue 3 页面、路由、API 封装、类型定义和交互组件
- **数据库脚本**：SQLite 默认运行库和 MySQL 可选部署脚本
- **运行验证**：后端编译、后端烟测和前端构建均通过

### 文档链接

| 文档 | 说明 |
|------|------|
| [模块三 AI 使用记录](（模块3）ai.md) | 编码实现阶段与 AI 的交互过程记录 |
| [模块三分工记录](（模块3）assign.md) | 模块三团队成员完成情况和功能核对 |
| [数据库脚本](database/schema.sql) | 数据库建表脚本 |
| [种子数据](database/seed.sql) | 演示数据脚本 |

---

## 模块四：AI辅助测试与调试

本模块完成了后端接口烟测、前端构建检查、真实浏览器联调、问题定位和修复记录。测试覆盖用户权限、论坛内容、社交互动、群组、举报、后台管理和本地部署复现。

### 主要产出

- 使用 FastAPI TestClient 覆盖核心后端接口
- 使用 `npm run build` 检查前端 TypeScript 和 Vite 构建
- 使用真实浏览器联调首页、登录、帖子互动、群组、个人中心、通知、后台权限和移动端首页
- 记录并修复发帖作者固定、互动缺失、权限入口暴露、Python 版本兼容和依赖版本不一致等问题

### 文档链接

| 文档 | 说明 |
|------|------|
| [测试报告](（模块4）test.md) | 测试目标、测试环境、测试结果和问题处理 |
| [模块四 AI 使用记录](（模块4）ai.md) | 测试与调试阶段与 AI 的交互过程记录 |
| [模块四分工记录](（模块4）assign.md) | 模块四团队成员测试与修复完成情况 |
| [后端烟测脚本](scripts/backend_smoke_test.py) | 后端核心接口自动化检查脚本 |

---

## 模块五：本地部署与交付

本模块按本地单机部署方式完成交付。后端运行在 `127.0.0.1:8000`，前端运行在 `127.0.0.1:5173`，数据库默认使用 `backend/forum_system.db`。该方式适合课堂演示、验收复现和本机调试。

### 主要产出

- **部署说明**：说明环境要求、后端启动、前端启动、演示账号、验证命令和常见问题
- **用户手册**：说明普通用户、专业用户和管理员的主要操作流程
- **项目总结报告**：总结需求分析、系统设计、编码实现、测试调试和部署交付成果
- **模块五记录**：补齐 AI 使用记录和工作完成情况记录

### 文档链接

| 文档 | 说明 |
|------|------|
| [部署说明](（模块5）install.md) | 本地部署步骤、验证命令和常见问题 |
| [用户手册](（模块5）user_guid.md) | 系统访问、账号角色和功能操作说明 |
| [模块五 AI 使用记录](（模块5）ai.md) | 部署交付阶段与 AI 的交互过程记录 |
| [模块五分工记录](（模块5）assign.md) | 模块五团队成员完成情况 |

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
