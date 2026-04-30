# 后端项目说明

后端规划使用 Spring Boot 3 + MyBatis-Plus + MySQL + JWT。当前目录先建立标准模块结构，后续由各成员在对应模块中补充代码。

## 模块所有权

| 模块 | 负责人 | 目录 |
| --- | --- | --- |
| 用户与权限 | 成员A | `src/main/java/com/stockforum/modules/auth` |
| 论坛内容 | 成员B | `src/main/java/com/stockforum/modules/forum` |
| 社交互动 | 成员C | `src/main/java/com/stockforum/modules/interaction` |
| 审核后台 | 成员D | `src/main/java/com/stockforum/modules/admin` |

## 包结构约定

每个模块内部按以下结构组织：

```text
controller/
service/
mapper/
entity/
dto/
vo/
```

公共代码放在 `common`、`config`、`security` 中。修改公共代码前需要在小组内说明影响范围。
