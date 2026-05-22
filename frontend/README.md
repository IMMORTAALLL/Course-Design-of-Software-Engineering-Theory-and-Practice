# 前端项目说明

前端使用 `Vue 3 + Vite + TypeScript`。当前已经补齐最小运行骨架，并先落地成员 D 负责的后台管理首页，用于对接审核、举报、敏感词和统计接口。

## 运行方式

```bash
cd frontend
npm install
npm run dev
```

默认开发地址为 `http://127.0.0.1:5173`。

## 当前已完成

- Vite 入口与 TypeScript 配置
- 基础样式文件
- 成员 D 的后台首页、内容审核、举报处理、敏感词管理、用户处罚和运营统计页面
- 管理后台接口请求封装
- 审核队列、举报列表、敏感词列表和概览卡片展示

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
