from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.common.response import success, paginated
from app.common.deps import get_current_user
from app.common.exceptions import ForbiddenError, ResourceNotFoundError
from app.modules.auth.models import User, UserProfile
from app.modules.auth.admin_schemas import UserStatusUpdateRequest

router = APIRouter(prefix="/api/admin", tags=["Admin-User"])


def require_admin(current_user: User = Depends(get_current_user)):
    role_names = [r.name for r in current_user.roles]
    if "ADMIN" not in role_names:
        raise ForbiddenError("需要管理员权限")
    return current_user


@router.get("/users")
def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    query = db.query(User)
    total = query.count()
    users = query.order_by(User.id).offset((page - 1) * size).limit(size).all()

    items = []
    for u in users:
        p = u.profile
        items.append({
            "id": u.id,
            "phone": u.phone,
            "email": u.email,
            "nickname": p.nickname if p else None,
            "authLevel": p.auth_level if p else 0,
            "status": u.status,
            "createdAt": u.created_at.isoformat() if u.created_at else None,
        })

    return paginated(items, page, size, total)


@router.put("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    req: UserStatusUpdateRequest,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ResourceNotFoundError("用户不存在")

    if req.status not in (0, 1, 2):
        from app.common.exceptions import ParamValidationError
        raise ParamValidationError("状态值只能为0(正常)、1(禁言)、2(封禁)")

    user.status = req.status
    db.commit()

    return success({"userId": user_id, "status": req.status})
