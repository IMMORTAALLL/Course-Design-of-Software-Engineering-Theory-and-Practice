from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.common.exceptions import AppException
from app.common.response import success
from app.modules.auth.admin_router import router as admin_router
from app.modules.auth.cert_router import router as cert_router
from app.modules.auth.router import router as auth_router
from app.modules.auth.user_router import router as user_router
from app.modules.forum import router as forum_router

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

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
app.include_router(admin_router)
app.include_router(forum_router)
