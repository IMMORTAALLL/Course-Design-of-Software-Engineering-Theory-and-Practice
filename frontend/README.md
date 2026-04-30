# 前端项目说明

前端规划使用 Vue 3 + Vite + Element Plus + ECharts。当前目录先建立模块结构，后续由各成员在对应模块中补充页面、组件和接口调用。

## 模块所有权

| 模块 | 负责人 | 目录 |
| --- | --- | --- |
| 用户与权限 | 成员A | `src/modules/auth` |
| 论坛内容 | 成员B | `src/modules/forum` |
| 社交互动 | 成员C | `src/modules/interaction` |
| 审核后台 | 成员D | `src/modules/admin` |

## 目录约定

每个业务模块内部按以下结构组织：

```text
api/
components/
views/
stores/
types/
```

跨模块共享的请求封装、布局、路由、状态、工具函数和样式放在 `src/shared` 中。
