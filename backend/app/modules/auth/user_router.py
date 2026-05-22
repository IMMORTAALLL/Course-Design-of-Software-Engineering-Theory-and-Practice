from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.common.response import success, paginated
from app.common.deps import get_current_user
from app.common.exceptions import ResourceNotFoundError
from app.modules.auth.models import User, UserProfile
from app.modules.auth.user_schemas import ProfileUpdateRequest, UserPublicProfile

router = APIRouter(prefix="/api/users", tags=["User"])


@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    profile = current_user.profile
    role_name = current_user.roles[0].name if current_user.roles else "USER"
    return success({
        "id": current_user.id,
        "phone": current_user.phone,
        "email": current_user.email,
        "nickname": profile.nickname if profile else None,
        "avatarUrl": profile.avatar_url if profile else None,
        "bio": profile.bio if profile else None,
        "authLevel": profile.auth_level if profile else 0,
        "riskPreference": profile.risk_preference if profile else None,
        "influenceScore": profile.influence_score if profile else 0,
        "role": role_name,
        "status": current_user.status,
    })


@router.put("/me/profile")
def update_profile(
    req: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = current_user.profile
    if not profile:
        profile = UserProfile(user_id=current_user.id, nickname="用户")
        db.add(profile)

    if req.nickname is not None:
        profile.nickname = req.nickname
    if req.avatar_url is not None:
        profile.avatar_url = req.avatar_url
    if req.bio is not None:
        profile.bio = req.bio
    if req.risk_preference is not None:
        profile.risk_preference = req.risk_preference

    db.commit()
    return success(message="修改成功")


@router.get("/search")
def search_users(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    query = db.query(User).join(UserProfile).filter(
        UserProfile.nickname.like(f"%{keyword}%")
    )
    total = query.count()
    users = query.offset((page - 1) * size).limit(size).all()

    items = []
    for u in users:
        p = u.profile
        items.append({
            "id": u.id,
            "nickname": p.nickname if p else None,
            "avatarUrl": p.avatar_url if p else None,
            "authLevel": p.auth_level if p else 0,
        })

    return paginated(items, page, size, total)


@router.get("/{user_id}")
def get_user_public_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ResourceNotFoundError("用户不存在")

    profile = user.profile
    return success({
        "id": user.id,
        "nickname": profile.nickname if profile else None,
        "avatarUrl": profile.avatar_url if profile else None,
        "bio": profile.bio if profile else None,
        "authLevel": profile.auth_level if profile else 0,
        "influenceScore": profile.influence_score if profile else 0,
    })
