# 脚本目录

本目录用于存放本地启动、数据库初始化、测试检查和部署等辅助脚本。

## 后端接口烟测

`backend_smoke_test.py` 会使用系统临时目录中的独立 SQLite 数据库，不会污染仓库里的本地演示数据库。检查范围包括健康检查、注册登录、发帖、评论回复、点赞收藏、举报、群组、管理员后台权限和 OpenAPI 生成。

运行前先准备后端依赖环境：

```bash
cd backend
pip install -r requirements.txt
```

从仓库根目录执行：

```bash
python scripts/backend_smoke_test.py
```

如果 Windows 默认 `python` 版本过旧，请改用已安装依赖的 Python 3.10+ 环境执行，例如：

```bash
py -3.13 scripts/backend_smoke_test.py
```

## 常用检查命令

```bash
python -m compileall backend/app
cd frontend && npm run build
git diff --check
```

后续可以继续补充：

- `dev-backend.ps1`
- `dev-frontend.ps1`
- `init-database.sql`
