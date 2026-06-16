# 前端项目说明

前端使用 `Vue 3 + Vite + TypeScript`，按课程设计分工拆分为用户与权限、论坛内容、社交互动、审核后台四个业务模块。

## 运行方式

先启动后端服务，默认地址为 `http://127.0.0.1:8000`。

```bash
cd frontend
npm install
npm run dev
```

默认开发地址为 `http://127.0.0.1:5173`。开发环境通过 Vite 将 `/api` 代理到 `http://127.0.0.1:8000`，可用 `VITE_API_PROXY_TARGET` 覆盖，例如：

```bash
$env:VITE_API_PROXY_TARGET="http://127.0.0.1:8001"
npm run dev
```

## 当前已完成

- Vite 入口、TypeScript 配置、基础样式与全局路由
- 成员 A：登录、注册、个人中心、认证申请、风险测评、用户公开主页
- 成员 B：首页、板块列表、板块详情、帖子详情、普通发帖、长文分析、搜索、热榜
- 成员 C：评论与回复、点赞、收藏、关注、通知中心、关注动态、群组列表与详情
- 成员 D：后台首页、内容审核、举报处理、敏感词管理、用户处置和运营统计
- 请求封装统一处理后端 `code/message/data` 响应格式，并在 Token 失效时清理登录态

## 模块分工

| 模块 | 负责人 | 目录 |
| --- | --- | --- |
| 用户与权限 | 成员A | `src/modules/auth` |
| 论坛内容 | 成员B | `src/modules/forum` |
| 社交互动 | 成员C | `src/modules/interaction` |
| 审核后台 | 成员D | `src/modules/admin` |

## 目录约定

```text
src/
├─ modules/
│  ├─ auth/
│  ├─ forum/
│  ├─ interaction/
│  └─ admin/
│     ├─ api/
│     ├─ components/
│     ├─ stores/
│     ├─ types/
│     └─ views/
└─ shared/
   ├─ api/
   ├─ components/
   ├─ layouts/
   ├─ router/
   ├─ stores/
   ├─ styles/
   └─ utils/
```

跨模块共享的请求封装、布局、状态管理和样式放在 `src/shared` 中。
