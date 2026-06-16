from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.common.exceptions import AppException
from app.common.response import success
from app.database import Base, SessionLocal, engine
from app.modules.admin.bootstrap import seed_admin_demo_data
from app.modules.admin.router import router as admin_audit_router
from app.modules.auth.admin_router import router as auth_admin_router
from app.modules.auth.cert_router import router as cert_router
from app.modules.auth.router import router as auth_router
from app.modules.auth.user_router import router as user_router
from app.modules.forum import router as forum_router
from app.modules.interaction.router import router as interaction_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)


def ensure_sqlite_demo_schema() -> None:
    if engine.dialect.name != "sqlite":
        return
    with engine.begin() as conn:
        post_columns = {row[1] for row in conn.exec_driver_sql("PRAGMA table_info(posts)").fetchall()}
        if "post_type" not in post_columns:
            conn.exec_driver_sql("ALTER TABLE posts ADD COLUMN post_type INTEGER NOT NULL DEFAULT 1")
        if "is_elite" not in post_columns:
            conn.exec_driver_sql("ALTER TABLE posts ADD COLUMN is_elite INTEGER NOT NULL DEFAULT 0")

        group_columns = {row[1] for row in conn.exec_driver_sql("PRAGMA table_info(groups)").fetchall()}
        if "description" not in group_columns:
            conn.exec_driver_sql("ALTER TABLE groups ADD COLUMN description VARCHAR(255)")

        notification_exists = conn.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='notifications'"
        ).fetchone()
        if notification_exists is None:
            conn.exec_driver_sql(
                """
                CREATE TABLE notifications (
                    id INTEGER NOT NULL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    title VARCHAR(120) NOT NULL,
                    content VARCHAR(255) NOT NULL,
                    notification_type VARCHAR(32) NOT NULL,
                    target_type VARCHAR(32),
                    target_id INTEGER,
                    is_read BOOLEAN NOT NULL,
                    created_at DATETIME NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users (id)
                )
                """
            )

        join_request_exists = conn.exec_driver_sql(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='group_join_requests'"
        ).fetchone()
        if join_request_exists is None:
            conn.exec_driver_sql(
                """
                CREATE TABLE group_join_requests (
                    group_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    status VARCHAR(16) NOT NULL,
                    created_at DATETIME NOT NULL,
                    PRIMARY KEY (group_id, user_id),
                    FOREIGN KEY(group_id) REFERENCES groups (id),
                    FOREIGN KEY(user_id) REFERENCES users (id)
                )
                """
            )


Base.metadata.create_all(bind=engine)
ensure_sqlite_demo_schema()
with SessionLocal() as db:
    seed_admin_demo_data(db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    msg = errors[0].get("msg", "参数校验失败") if errors else "参数校验失败"
    return JSONResponse(
        status_code=200,
        content={"code": 40001, "message": msg, "data": None},
    )


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=200,
        content={"code": exc.code, "message": exc.message, "data": None},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content={"code": 50001, "message": "系统内部错误", "data": None},
    )


@app.get("/api/health")
def health_check():
    return success({"status": "ok"})


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(cert_router)
app.include_router(auth_admin_router)
app.include_router(forum_router)
app.include_router(interaction_router)
app.include_router(admin_audit_router)
