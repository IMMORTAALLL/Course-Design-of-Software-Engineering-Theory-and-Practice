from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.common.response import success
from app.common.deps import get_current_user
from app.modules.auth import service
from app.modules.auth.schemas import RegisterRequest, LoginRequest, VerifyCodeRequest

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register")
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    user_id = service.register(db, req)
    return success({"userId": user_id})


@router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    data = service.login(db, req)
    return success(data)


@router.post("/logout")
def logout(current_user=Depends(get_current_user)):
    return success(message="退出成功")


@router.post("/verify-code")
def send_verify_code(req: VerifyCodeRequest):
    code = service.send_verify_code(req.account_type, req.target)
    return success({"message": "验证码已发送（模拟）", "code": code})
