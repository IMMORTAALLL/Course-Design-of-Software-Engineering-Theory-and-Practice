from sqlalchemy.orm import Session

from app.modules.auth.models import User, UserProfile, Role, UserRole
from app.modules.auth.schemas import RegisterRequest, LoginRequest
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token
from app.common.exceptions import (
    ParamValidationError, ConflictError, StateNotAllowedError
)

# 模拟验证码存储（课程演示用，接受任意6位数字）
_verify_codes: dict = {}


def send_verify_code(account_type: str, target: str) -> str:
    code = "123456"
    _verify_codes[target] = code
    return code


def _check_verify_code(target: str, code: str) -> bool:
    if len(code) == 6 and code.isdigit():
        return True
    return False


def register(db: Session, req: RegisterRequest) -> int:
    if not _check_verify_code(req.phone or req.email, req.verify_code):
        raise ParamValidationError("验证码错误")

    if req.account_type == "phone":
        if not req.phone:
            raise ParamValidationError("手机号不能为空")
        existing = db.query(User).filter(User.phone == req.phone).first()
        if existing:
            raise ConflictError("该手机号已注册")
    else:
        if not req.email:
            raise ParamValidationError("邮箱不能为空")
        existing = db.query(User).filter(User.email == req.email).first()
        if existing:
            raise ConflictError("该邮箱已注册")

    user = User(
        phone=req.phone,
        email=req.email,
        password_hash=hash_password(req.password),
    )
    db.add(user)
    db.flush()

    profile = UserProfile(user_id=user.id, nickname=req.nickname)
    db.add(profile)

    default_role = db.query(Role).filter(Role.name == "USER").first()
    if default_role:
        user_role = UserRole(user_id=user.id, role_id=default_role.id)
        db.add(user_role)

    db.commit()
    db.refresh(user)
    return user.id


def login(db: Session, req: LoginRequest) -> dict:
    user = db.query(User).filter(
        (User.phone == req.account) | (User.email == req.account)
    ).first()

    if not user:
        raise ParamValidationError("账号或密码错误")

    if not verify_password(req.password, user.password_hash):
        raise ParamValidationError("账号或密码错误")

    if user.status == 2:
        raise StateNotAllowedError("账号已被封禁")

    role_name = "USER"
    if user.roles:
        role_name = user.roles[0].name

    token = create_access_token({"sub": str(user.id)})

    profile = user.profile
    nickname = profile.nickname if profile else "用户"
    auth_level = profile.auth_level if profile else 0

    return {
        "token": token,
        "user": {
            "id": user.id,
            "nickname": nickname,
            "authLevel": auth_level,
            "role": role_name,
            "status": user.status,
        },
    }
