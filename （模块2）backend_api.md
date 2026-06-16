# 后端接口设计文档

项目名称：智投社区：股票基金投资论坛系统

本文档依据 `（模块1）user_stories.md`、`（模块1）use_cases.md`、`（模块2）architect.md`、`（模块2）db.md` 和 `（模块2）ui_design.md`，设计智投社区后端 RESTful API。接口采用前后端分离原则，使用 JSON 作为数据交换格式，并提供 OpenAPI 3.0 YAML 规范，便于后续前端联调、接口测试和答辩展示。

## 一、接口设计目标

后端接口设计目标如下：

- 支持游客浏览首页、板块、帖子详情、搜索结果等公开内容。
- 支持注册用户完成注册、登录、发帖、评论、点赞、收藏、关注、加入群组等核心操作。
- 支持认证用户发布长文分析并展示认证身份。
- 支持平台管理员完成板块管理、内容审核、举报处理、敏感词管理和统计查看。
- 保持接口路径、数据库字段、前端页面和核心类设计之间的一致性。
- 采用 OpenAPI 3.0 描述主要接口，便于生成接口文档和模拟请求。

## 二、接口设计原则

### 1. RESTful 路径规范

| 规则 | 示例 |
| --- | --- |
| 使用名词复数表示资源 | `/api/posts`、`/api/sections` |
| 使用 HTTP 方法表达操作 | `GET` 查询、`POST` 新建、`PUT` 修改、`DELETE` 删除 |
| 子资源使用嵌套路径 | `/api/posts/{postId}/comments` |
| 管理端接口统一加 `/admin` 前缀 | `/api/admin/audits/posts` |
| 搜索和统计使用语义化路径 | `/api/search/posts`、`/api/admin/statistics/overview` |

### 2. 数据格式

所有请求和响应默认使用 JSON。

```text
Content-Type: application/json
Accept: application/json
```

文件上传接口使用 `multipart/form-data`，例如认证材料、帖子附件和图片上传。

### 3. 认证方式

系统采用 JWT Bearer Token。

```text
Authorization: Bearer <token>
```

游客可访问公开接口；注册用户、认证用户和平台管理员访问受限接口时必须携带 Token。

### 4. 权限级别

| 权限级别 | 说明 |
| --- | --- |
| Public | 游客可访问 |
| User | 登录用户可访问 |
| Certified | 认证用户可访问 |
| Admin | 平台管理员可访问 |

## 三、统一响应格式

### 1. 成功响应

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

### 2. 分页响应

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [],
    "page": 1,
    "size": 10,
    "total": 100
  }
}
```

### 3. 失败响应

```json
{
  "code": 40001,
  "message": "参数校验失败",
  "data": null
}
```

## 四、错误码设计

| 错误码 | 含义 | 常见场景 |
| --- | --- | --- |
| `0` | 成功 | 请求处理成功 |
| `40001` | 参数校验失败 | 标题为空、邮箱格式错误、密码强度不足 |
| `40002` | 资源不存在 | 帖子、板块、用户不存在 |
| `40003` | 状态不允许 | 用户被禁言、帖子已删除、板块已停用 |
| `40101` | 未登录 | 需要登录但未携带 Token |
| `40102` | Token 无效 | Token 过期或签名错误 |
| `40301` | 权限不足 | 普通用户访问后台接口 |
| `40901` | 资源冲突 | 手机号已注册、重复关注、重复加入群组 |
| `50001` | 系统内部错误 | 数据库异常或未知异常 |

## 五、接口总览

### 1. 用户与权限接口

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| `POST` | `/api/auth/register` | Public | 用户注册 |
| `POST` | `/api/auth/login` | Public | 用户登录 |
| `POST` | `/api/auth/logout` | User | 退出登录 |
| `GET` | `/api/users/me` | User | 获取当前登录用户 |
| `PUT` | `/api/users/me/profile` | User | 修改个人资料 |
| `POST` | `/api/users/me/certification` | User | 提交认证申请 |
| `GET` | `/api/users/{id}` | Public | 查看用户公开主页 |

### 2. 板块接口

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| `GET` | `/api/sections` | Public | 获取板块列表 |
| `GET` | `/api/sections/{id}` | Public | 获取板块详情 |
| `POST` | `/api/admin/sections` | Admin | 新增板块 |
| `PUT` | `/api/admin/sections/{id}` | Admin | 修改板块 |
| `DELETE` | `/api/admin/sections/{id}` | Admin | 删除或停用板块 |

### 3. 帖子接口

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| `GET` | `/api/posts` | Public | 分页查询帖子 |
| `POST` | `/api/posts` | User | 发布普通帖子 |
| `POST` | `/api/posts/analysis` | Certified | 发布长文分析 |
| `GET` | `/api/posts/{id}` | Public | 获取帖子详情 |
| `PUT` | `/api/posts/{id}` | User | 编辑自己的帖子 |
| `DELETE` | `/api/posts/{id}` | User | 删除自己的帖子 |
| `POST` | `/api/posts/{id}/like` | User | 点赞或取消点赞 |
| `POST` | `/api/posts/{id}/favorite` | User | 收藏或取消收藏 |
| `GET` | `/api/posts/{id}/interaction-status` | User | 获取当前用户对帖子的点赞、收藏、关注作者状态 |
| `POST` | `/api/posts/{id}/report` | User | 举报帖子 |

### 4. 评论接口

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| `GET` | `/api/posts/{postId}/comments` | Public | 获取帖子评论 |
| `POST` | `/api/posts/{postId}/comments` | User | 发布评论 |
| `POST` | `/api/comments/{id}/replies` | User | 回复评论 |
| `DELETE` | `/api/comments/{id}` | User | 删除自己的评论 |
| `POST` | `/api/comments/{id}/like` | User | 点赞或取消点赞评论 |
| `POST` | `/api/comments/{id}/report` | User | 举报评论 |

### 5. 社交互动接口

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| `POST` | `/api/users/{id}/follow` | User | 关注或取消关注 |
| `GET` | `/api/users/{id}/followers` | Public | 查看粉丝列表 |
| `GET` | `/api/users/{id}/following` | Public | 查看关注列表 |
| `GET` | `/api/me/favorites` | User | 查看我的收藏 |
| `GET` | `/api/me/notifications` | User | 查看通知 |
| `PUT` | `/api/me/notifications/{id}/read` | User | 标记通知已读 |

### 6. 群组接口

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| `GET` | `/api/groups` | Public | 获取群组列表 |
| `POST` | `/api/groups` | User | 创建群组 |
| `GET` | `/api/groups/{id}` | Public | 获取群组详情 |
| `POST` | `/api/groups/{id}/join` | User | 加入或申请加入群组 |
| `DELETE` | `/api/groups/{id}/members/me` | User | 退出群组 |

### 7. 搜索接口

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| `GET` | `/api/search/posts` | Public | 搜索帖子 |
| `GET` | `/api/search/suggestions` | Public | 搜索联想 |
| `GET` | `/api/hot-topics` | Public | 获取热门话题 |

### 8. 审核与后台接口

| 方法 | 路径 | 权限 | 说明 |
| --- | --- | --- | --- |
| `GET` | `/api/admin/audits/posts` | Admin | 获取待审核帖子 |
| `POST` | `/api/admin/audits/posts/{id}` | Admin | 审核帖子 |
| `GET` | `/api/admin/reports` | Admin | 获取举报列表 |
| `POST` | `/api/admin/reports/{id}/handle` | Admin | 处理举报 |
| `GET` | `/api/admin/users` | Admin | 用户管理列表 |
| `PUT` | `/api/admin/users/{id}/status` | Admin | 修改账号状态 |
| `GET` | `/api/admin/statistics/overview` | Admin | 获取运营统计 |

## 六、核心接口说明

### 1. 用户注册

```text
POST /api/auth/register
权限：Public
```

请求体：

```json
{
  "accountType": "phone",
  "phone": "13800000000",
  "email": null,
  "password": "Password123",
  "nickname": "价值投资者",
  "verifyCode": "123456"
}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "userId": 1
  }
}
```

### 2. 用户登录

```text
POST /api/auth/login
权限：Public
```

请求体：

```json
{
  "account": "13800000000",
  "password": "Password123"
}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "jwt-token",
    "user": {
      "id": 1,
      "nickname": "价值投资者",
      "authLevel": 0,
      "role": "USER",
      "status": 0
    }
  }
}
```

### 3. 发布帖子

```text
POST /api/posts
权限：User
```

请求体：

```json
{
  "sectionId": 1,
  "title": "今天A股新能源板块怎么看",
  "content": "从成交量和政策预期看，短期仍需控制仓位。",
  "postType": 1,
  "tags": ["A股", "新能源", "风险提示"]
}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "postId": 1001,
    "auditStatus": "PUBLISHED"
  }
}
```

### 4. 获取帖子详情

```text
GET /api/posts/{id}
权限：Public
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1001,
    "title": "今天A股新能源板块怎么看",
    "content": "从成交量和政策预期看，短期仍需控制仓位。",
    "postType": 1,
    "likeCount": 12,
    "commentCount": 4,
    "favoriteCount": 3,
    "elite": false,
    "section": {
      "id": 1,
      "name": "A股市场"
    },
    "author": {
      "id": 1,
      "nickname": "价值投资者",
      "authLevel": 0
    },
    "tags": ["A股", "新能源"]
  }
}
```

### 5. 发布评论

```text
POST /api/posts/{postId}/comments
权限：User
```

请求体：

```json
{
  "content": "这个观点可以参考成交量继续验证。"
}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "commentId": 501,
    "auditStatus": "PUBLISHED"
  }
}
```

### 6. 关注用户

```text
POST /api/users/{id}/follow
权限：User
```

请求体：

```json
{
  "followed": true,
  "starred": false
}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "followed": true
  }
}
```

### 7. 创建群组

```text
POST /api/groups
权限：User
```

请求体：

```json
{
  "name": "新能源长期投资讨论组",
  "description": "讨论新能源行业公司和基金配置。",
  "permission": 1
}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "groupId": 301
  }
}
```

### 8. 审核帖子

```text
POST /api/admin/audits/posts/{id}
权限：Admin
```

请求体：

```json
{
  "decision": "REJECT",
  "reason": "内容包含明确收益承诺，不符合社区规范。"
}
```

响应：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "auditStatus": "REJECTED"
  }
}
```

## 七、OpenAPI 3.0 YAML

```yaml
openapi: 3.0.3
info:
  title: 智投社区后端接口
  description: 股票基金投资论坛系统 RESTful API
  version: 1.0.0
servers:
  - url: http://localhost:8080
    description: 本地开发环境

tags:
  - name: Auth
    description: 注册登录
  - name: User
    description: 用户资料与关注
  - name: Section
    description: 论坛板块
  - name: Post
    description: 帖子内容
  - name: Comment
    description: 评论回复
  - name: Group
    description: 投资群组
  - name: Search
    description: 搜索与热门话题
  - name: Admin
    description: 后台管理

paths:
  /api/auth/register:
    post:
      tags: [Auth]
      summary: 用户注册
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RegisterRequest'
      responses:
        '200':
          description: 注册成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserIdResponse'

  /api/auth/login:
    post:
      tags: [Auth]
      summary: 用户登录
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
      responses:
        '200':
          description: 登录成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoginResponse'

  /api/auth/logout:
    post:
      tags: [Auth]
      summary: 退出登录
      security:
        - bearerAuth: []
      responses:
        '200':
          description: 退出成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/users/me:
    get:
      tags: [User]
      summary: 获取当前登录用户
      security:
        - bearerAuth: []
      responses:
        '200':
          description: 当前用户信息
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'

  /api/users/me/profile:
    put:
      tags: [User]
      summary: 修改个人资料
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserProfileUpdateRequest'
      responses:
        '200':
          description: 修改成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/users/me/certification:
    post:
      tags: [User]
      summary: 提交认证申请
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CertificationRequest'
      responses:
        '200':
          description: 提交成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/users/{id}:
    get:
      tags: [User]
      summary: 获取用户公开主页
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 用户公开信息
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'

  /api/users/{id}/follow:
    post:
      tags: [User]
      summary: 关注或取消关注用户
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FollowRequest'
      responses:
        '200':
          description: 关注状态
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/FollowResponse'

  /api/users/{id}/followers:
    get:
      tags: [User]
      summary: 查看粉丝列表
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 粉丝列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/users/{id}/following:
    get:
      tags: [User]
      summary: 查看关注列表
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 关注列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/me/favorites:
    get:
      tags: [User]
      summary: 查看我的收藏
      security:
        - bearerAuth: []
      responses:
        '200':
          description: 收藏列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/me/notifications:
    get:
      tags: [User]
      summary: 查看通知
      security:
        - bearerAuth: []
      responses:
        '200':
          description: 通知列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/me/notifications/{id}/read:
    put:
      tags: [User]
      summary: 标记通知已读
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 标记成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/sections:
    get:
      tags: [Section]
      summary: 获取板块列表
      responses:
        '200':
          description: 板块列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SectionListResponse'

  /api/sections/{id}:
    get:
      tags: [Section]
      summary: 获取板块详情
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 板块详情
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SectionResponse'

  /api/posts:
    get:
      tags: [Post]
      summary: 分页查询帖子
      parameters:
        - name: sectionId
          in: query
          schema:
            type: integer
        - name: keyword
          in: query
          schema:
            type: string
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: 帖子分页列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostPageResponse'
    post:
      tags: [Post]
      summary: 发布普通帖子
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PostCreateRequest'
      responses:
        '200':
          description: 发布结果
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostCreateResponse'

  /api/posts/analysis:
    post:
      tags: [Post]
      summary: 发布长文分析
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PostCreateRequest'
      responses:
        '200':
          description: 发布结果
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostCreateResponse'

  /api/posts/{id}:
    get:
      tags: [Post]
      summary: 获取帖子详情
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 帖子详情
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostResponse'
    put:
      tags: [Post]
      summary: 编辑帖子
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PostUpdateRequest'
      responses:
        '200':
          description: 编辑成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'
    delete:
      tags: [Post]
      summary: 删除帖子
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 删除成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/posts/{id}/like:
    post:
      tags: [Post]
      summary: 点赞或取消点赞帖子
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 点赞状态
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ActionResponse'

  /api/posts/{id}/favorite:
    post:
      tags: [Post]
      summary: 收藏或取消收藏帖子
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 收藏状态
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ActionResponse'

  /api/posts/{id}/report:
    post:
      tags: [Post]
      summary: 举报帖子
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReportRequest'
      responses:
        '200':
          description: 举报成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/posts/{postId}/comments:
    get:
      tags: [Comment]
      summary: 获取帖子评论
      parameters:
        - name: postId
          in: path
          required: true
          schema:
            type: integer
            format: int64
      responses:
        '200':
          description: 评论列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CommentListResponse'
    post:
      tags: [Comment]
      summary: 发布评论
      security:
        - bearerAuth: []
      parameters:
        - name: postId
          in: path
          required: true
          schema:
            type: integer
            format: int64
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentCreateRequest'
      responses:
        '200':
          description: 评论发布结果
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CommentCreateResponse'

  /api/comments/{id}/replies:
    post:
      tags: [Comment]
      summary: 回复评论
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentCreateRequest'
      responses:
        '200':
          description: 回复发布结果
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CommentCreateResponse'

  /api/comments/{id}:
    delete:
      tags: [Comment]
      summary: 删除自己的评论
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 删除成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/comments/{id}/like:
    post:
      tags: [Comment]
      summary: 点赞或取消点赞评论
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 点赞状态
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ActionResponse'

  /api/comments/{id}/report:
    post:
      tags: [Comment]
      summary: 举报评论
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReportRequest'
      responses:
        '200':
          description: 举报成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/groups:
    get:
      tags: [Group]
      summary: 获取群组列表
      responses:
        '200':
          description: 群组列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GroupListResponse'
    post:
      tags: [Group]
      summary: 创建群组
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/GroupCreateRequest'
      responses:
        '200':
          description: 创建结果
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GroupCreateResponse'

  /api/groups/{id}:
    get:
      tags: [Group]
      summary: 获取群组详情
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 群组详情
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GroupResponse'

  /api/groups/{id}/join:
    post:
      tags: [Group]
      summary: 加入或申请加入群组
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 加入结果
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/JoinGroupResponse'

  /api/groups/{id}/members/me:
    delete:
      tags: [Group]
      summary: 退出群组
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 退出成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/search/posts:
    get:
      tags: [Search]
      summary: 搜索帖子
      parameters:
        - name: keyword
          in: query
          required: true
          schema:
            type: string
        - name: sort
          in: query
          schema:
            type: string
            enum: [time, hot, elite]
      responses:
        '200':
          description: 搜索结果
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostPageResponse'

  /api/search/suggestions:
    get:
      tags: [Search]
      summary: 搜索联想
      parameters:
        - name: keyword
          in: query
          required: true
          schema:
            type: string
      responses:
        '200':
          description: 联想词列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SuggestionResponse'

  /api/hot-topics:
    get:
      tags: [Search]
      summary: 获取热门话题
      responses:
        '200':
          description: 热门话题列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HotTopicResponse'

  /api/admin/sections:
    post:
      tags: [Admin]
      summary: 新增板块
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SectionCreateRequest'
      responses:
        '200':
          description: 创建成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/admin/sections/{id}:
    put:
      tags: [Admin]
      summary: 修改板块
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SectionCreateRequest'
      responses:
        '200':
          description: 修改成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'
    delete:
      tags: [Admin]
      summary: 删除或停用板块
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      responses:
        '200':
          description: 删除或停用成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/admin/audits/posts:
    get:
      tags: [Admin]
      summary: 获取待审核帖子
      security:
        - bearerAuth: []
      responses:
        '200':
          description: 待审核帖子
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PostPageResponse'

  /api/admin/audits/posts/{id}:
    post:
      tags: [Admin]
      summary: 审核帖子
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AuditRequest'
      responses:
        '200':
          description: 审核结果
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuditResponse'

  /api/admin/reports:
    get:
      tags: [Admin]
      summary: 获取举报列表
      security:
        - bearerAuth: []
      responses:
        '200':
          description: 举报列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/admin/reports/{id}/handle:
    post:
      tags: [Admin]
      summary: 处理举报
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ReportHandleRequest'
      responses:
        '200':
          description: 处理成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/admin/users:
    get:
      tags: [Admin]
      summary: 用户管理列表
      security:
        - bearerAuth: []
      responses:
        '200':
          description: 用户列表
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/admin/users/{id}/status:
    put:
      tags: [Admin]
      summary: 修改账号状态
      security:
        - bearerAuth: []
      parameters:
        - $ref: '#/components/parameters/Id'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserStatusUpdateRequest'
      responses:
        '200':
          description: 修改成功
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

  /api/admin/statistics/overview:
    get:
      tags: [Admin]
      summary: 获取运营统计
      security:
        - bearerAuth: []
      responses:
        '200':
          description: 统计概览
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BaseResponse'

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  parameters:
    Id:
      name: id
      in: path
      required: true
      schema:
        type: integer
        format: int64

  schemas:
    BaseResponse:
      type: object
      properties:
        code:
          type: integer
          example: 0
        message:
          type: string
          example: success
        data:
          nullable: true

    UserProfileUpdateRequest:
      type: object
      properties:
        nickname:
          type: string
        avatarUrl:
          type: string
        bio:
          type: string
        riskPreference:
          type: integer
          description: 1-保守, 2-稳健, 3-积极

    CertificationRequest:
      type: object
      required: [certificationType, realName]
      properties:
        certificationType:
          type: string
          enum: [REAL_NAME, PROFESSIONAL]
        realName:
          type: string
        materialUrls:
          type: array
          items:
            type: string

    ReportRequest:
      type: object
      required: [reason]
      properties:
        reason:
          type: string
        description:
          type: string

    ReportHandleRequest:
      type: object
      required: [decision]
      properties:
        decision:
          type: string
          enum: [DISMISS, DELETE_CONTENT, WARN_USER, MUTE_USER, BAN_USER]
        reason:
          type: string

    UserStatusUpdateRequest:
      type: object
      required: [status]
      properties:
        status:
          type: integer
          description: 0-正常, 1-禁言, 2-封禁
        reason:
          type: string

    RegisterRequest:
      type: object
      required: [accountType, password, nickname, verifyCode]
      properties:
        accountType:
          type: string
          enum: [phone, email]
        phone:
          type: string
        email:
          type: string
        password:
          type: string
        nickname:
          type: string
        verifyCode:
          type: string

    LoginRequest:
      type: object
      required: [account, password]
      properties:
        account:
          type: string
        password:
          type: string

    LoginResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: object
              properties:
                token:
                  type: string
                user:
                  $ref: '#/components/schemas/User'

    UserIdResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: object
              properties:
                userId:
                  type: integer
                  format: int64

    UserResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              $ref: '#/components/schemas/User'

    User:
      type: object
      properties:
        id:
          type: integer
          format: int64
        phone:
          type: string
        email:
          type: string
        nickname:
          type: string
        avatarUrl:
          type: string
        authLevel:
          type: integer
          description: 0-基础, 1-实名, 2-专业
        riskPreference:
          type: integer
        status:
          type: integer
          description: 0-正常, 1-禁言, 2-封禁

    Section:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        description:
          type: string
        sortOrder:
          type: integer
        active:
          type: boolean

    SectionCreateRequest:
      type: object
      required: [name]
      properties:
        name:
          type: string
        description:
          type: string
        sortOrder:
          type: integer
        active:
          type: boolean

    SectionResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              $ref: '#/components/schemas/Section'

    SectionListResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/components/schemas/Section'

    Post:
      type: object
      properties:
        id:
          type: integer
          format: int64
        sectionId:
          type: integer
        userId:
          type: integer
          format: int64
        title:
          type: string
        content:
          type: string
        postType:
          type: integer
        likeCount:
          type: integer
        commentCount:
          type: integer
        favoriteCount:
          type: integer
        elite:
          type: boolean
        auditStatus:
          type: string
          enum: [PENDING, PUBLISHED, REJECTED, DELETED]
        tags:
          type: array
          items:
            type: string

    PostCreateRequest:
      type: object
      required: [sectionId, title, content, postType]
      properties:
        sectionId:
          type: integer
        title:
          type: string
        content:
          type: string
        postType:
          type: integer
        tags:
          type: array
          items:
            type: string

    PostUpdateRequest:
      type: object
      properties:
        title:
          type: string
        content:
          type: string
        tags:
          type: array
          items:
            type: string

    PostResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              $ref: '#/components/schemas/Post'

    PostCreateResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: object
              properties:
                postId:
                  type: integer
                  format: int64
                auditStatus:
                  type: string

    PostPageResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: object
              properties:
                items:
                  type: array
                  items:
                    $ref: '#/components/schemas/Post'
                page:
                  type: integer
                size:
                  type: integer
                total:
                  type: integer

    Comment:
      type: object
      properties:
        id:
          type: integer
          format: int64
        postId:
          type: integer
          format: int64
        userId:
          type: integer
          format: int64
        parentId:
          type: integer
          format: int64
          nullable: true
        content:
          type: string
        likeCount:
          type: integer
        auditStatus:
          type: string

    CommentCreateRequest:
      type: object
      required: [content]
      properties:
        content:
          type: string

    CommentCreateResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: object
              properties:
                commentId:
                  type: integer
                  format: int64
                auditStatus:
                  type: string

    CommentListResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/components/schemas/Comment'

    Group:
      type: object
      properties:
        id:
          type: integer
          format: int64
        creatorId:
          type: integer
          format: int64
        name:
          type: string
        description:
          type: string
        permission:
          type: integer
          description: 1-公开, 2-需审核, 3-私密
        memberCount:
          type: integer

    GroupCreateRequest:
      type: object
      required: [name, permission]
      properties:
        name:
          type: string
        description:
          type: string
        permission:
          type: integer

    GroupCreateResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: object
              properties:
                groupId:
                  type: integer
                  format: int64

    GroupListResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: array
              items:
                $ref: '#/components/schemas/Group'

    GroupResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              $ref: '#/components/schemas/Group'

    JoinGroupResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: object
              properties:
                status:
                  type: string
                  enum: [JOINED, PENDING, REJECTED]

    SuggestionResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: array
              items:
                type: string

    HotTopicResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  topicName:
                    type: string
                  rankPos:
                    type: integer
                  hotScore:
                    type: integer

    FollowRequest:
      type: object
      required: [followed]
      properties:
        followed:
          type: boolean
        starred:
          type: boolean

    FollowResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: object
              properties:
                followed:
                  type: boolean

    ActionResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: object
              properties:
                active:
                  type: boolean
                count:
                  type: integer

    AuditRequest:
      type: object
      required: [decision]
      properties:
        decision:
          type: string
          enum: [APPROVE, REJECT, DELETE, REQUIRE_MODIFY]
        reason:
          type: string

    AuditResponse:
      allOf:
        - $ref: '#/components/schemas/BaseResponse'
        - type: object
          properties:
            data:
              type: object
              properties:
                auditStatus:
                  type: string
```

## 八、接口与页面对应关系

| 前端页面 | 主要接口 |
| --- | --- |
| 登录页 | `POST /api/auth/login` |
| 注册页 | `POST /api/auth/register` |
| 首页 | `GET /api/posts`、`GET /api/hot-topics` |
| 板块列表页 | `GET /api/sections` |
| 板块详情页 | `GET /api/sections/{id}`、`GET /api/posts?sectionId=` |
| 帖子详情页 | `GET /api/posts/{id}`、`GET /api/posts/{postId}/comments` |
| 普通发帖页 | `POST /api/posts` |
| 长文分析发布页 | `POST /api/posts/analysis` |
| 搜索结果页 | `GET /api/search/posts`、`GET /api/search/suggestions` |
| 用户公开主页 | `GET /api/users/{id}`、`POST /api/users/{id}/follow` |
| 收藏列表页 | `GET /api/me/favorites` |
| 通知中心页 | `GET /api/me/notifications` |
| 群组列表页 | `GET /api/groups`、`POST /api/groups` |
| 内容审核页 | `GET /api/admin/audits/posts`、`POST /api/admin/audits/posts/{id}` |
| 举报处理页 | `GET /api/admin/reports`、`POST /api/admin/reports/{id}/handle` |

## 九、接口与数据库对应关系

| 接口资源 | 主要表 |
| --- | --- |
| 用户注册登录 | `users`、`user_profiles` |
| 板块管理 | `sections` |
| 帖子发布与查询 | `posts`、`attachments`、`user_actions` |
| 评论与回复 | `comments`、`user_actions` |
| 关注关系 | `user_follows` |
| 群组 | `groups`、`group_members`、`group_join_requests` |
| 搜索与热榜 | `search_history`、`hot_topics` |
| 审核与举报 | `audit_logs`、`reports`、`report_items` |

## 十、最终采用方案

最终后端接口采用 RESTful API 风格，以 `/api` 作为统一前缀，后台接口统一使用 `/api/admin` 前缀。接口使用 JWT Bearer Token 完成身份认证，使用统一响应结构返回业务结果，使用错误码区分参数错误、未登录、权限不足、资源不存在和系统异常等情况。

课程设计阶段优先实现注册登录、板块浏览、发帖、帖子详情、评论、点赞、收藏、关注、群组加入和后台审核等核心闭环。OpenAPI 3.0 YAML 覆盖主要路径和 schema，可作为前端联调、接口测试和后续代码生成的基础。

## 十一、成员 D 后台模块实现补充

本节记录成员 D 已落地的后台管理接口。当前后端采用 `FastAPI + SQLAlchemy` 实现，接口统一挂载在 `/api/admin` 下，统一响应结构仍保持：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

当前本地开发服务地址为：

```text
http://127.0.0.1:8001
```

### 1. 已实现接口清单

| 方法 | 路径 | 说明 | 前端页面 |
| --- | --- | --- | --- |
| `GET` | `/api/admin/overview` | 获取后台首页概览统计 | `/admin` |
| `GET` | `/api/admin/audit-queue` | 获取内容审核队列 | `/admin/audits` |
| `PATCH` | `/api/admin/audit-queue/{item_id}` | 更新审核队列条目状态 | `/admin/audits` |
| `GET` | `/api/admin/reports` | 获取举报处理列表 | `/admin/reports` |
| `PATCH` | `/api/admin/reports/{item_id}` | 更新举报处理状态 | `/admin/reports` |
| `GET` | `/api/admin/sensitive-words` | 获取敏感词列表 | `/admin/sensitive-words` |
| `PATCH` | `/api/admin/sensitive-words/{word_id}` | 启用或停用敏感词 | `/admin/sensitive-words` |
| `GET` | `/api/admin/user-moderation` | 获取用户处罚记录 | `/admin/users` |
| `GET` | `/api/admin/statistics` | 获取运营统计摘要 | `/admin/statistics` |

### 2. 后台概览接口

```text
GET /api/admin/overview
权限：Admin
```

响应数据字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `today_posts` | number | 今日发帖数量 |
| `pending_audits` | number | 待审核内容数量 |
| `pending_reports` | number | 待处理举报数量 |
| `active_sensitive_words` | number | 当前启用的敏感词数量 |

### 3. 内容审核接口

```text
GET /api/admin/audit-queue
PATCH /api/admin/audit-queue/{item_id}
权限：Admin
```

审核队列返回字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | number | 审核条目 ID |
| `content_type` | string | 内容类型 |
| `title` | string | 内容标题 |
| `author_name` | string | 作者昵称 |
| `reason` | string | 进入审核队列的原因 |
| `risk_level` | string | 风险等级 |
| `status` | string | 当前审核状态 |
| `created_at` | string | 创建时间 |

更新审核状态请求体：

```json
{
  "action": "approve"
}
```

当前前端使用的动作值包括：

- `approve`
- `reject`

### 4. 举报处理接口

```text
GET /api/admin/reports
PATCH /api/admin/reports/{item_id}
权限：Admin
```

举报列表返回字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | number | 举报 ID |
| `target_type` | string | 被举报对象类型 |
| `target_title` | string | 被举报对象标题 |
| `reporter_name` | string | 举报人昵称 |
| `reason` | string | 举报原因 |
| `status` | string | 举报处理状态 |
| `created_at` | string | 举报时间 |

处理举报请求体：

```json
{
  "action": "warning_issued"
}
```

当前前端使用的动作值包括：

- `dismissed`
- `warning_issued`
- `banned`

### 5. 敏感词管理接口

```text
GET /api/admin/sensitive-words
PATCH /api/admin/sensitive-words/{word_id}
权限：Admin
```

敏感词返回字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | number | 敏感词 ID |
| `keyword` | string | 敏感词内容 |
| `category` | string | 分类 |
| `risk_level` | string | 风险等级 |
| `action` | string | 命中后的处理方式 |
| `enabled` | boolean | 是否启用 |
| `note` | string/null | 备注 |
| `created_at` | string | 创建时间 |

启用或停用请求体：

```json
{
  "enabled": false
}
```

### 6. 用户处罚与统计接口

```text
GET /api/admin/user-moderation
GET /api/admin/statistics
权限：Admin
```

用户处罚记录返回字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | number | 处罚记录 ID |
| `user_name` | string | 用户昵称 |
| `action` | string | 处罚动作 |
| `reason` | string | 处罚原因 |
| `status` | string | 当前状态 |
| `created_at` | string | 处罚时间 |

运营统计接口返回：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `hot_topics` | string[] | 热门话题列表 |
| `active_sections` | object[] | 活跃板块统计 |

### 7. 当前实现说明

当前实现已经满足后台管理首页、内容审核、举报处理、敏感词管理、用户处罚记录和运营统计的基础联调。独立的用户禁言、封号写接口还没有拆出；目前举报处理里的 `banned` 动作只更新举报处理结果，不会同步修改用户账号状态。
