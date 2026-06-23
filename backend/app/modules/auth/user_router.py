import json
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.common.response import success, paginated
from app.common.deps import get_current_user
from app.common.exceptions import ResourceNotFoundError
from app.modules.auth.models import User, UserProfile
from app.modules.auth.user_schemas import ProfileUpdateRequest, UserPublicProfile

router = APIRouter(prefix="/api/users", tags=["User"])


def _loads_list(value: Optional[str]) -> List[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return [item.strip() for item in value.split(",") if item.strip()]
    return parsed if isinstance(parsed, list) else []


def _dumps_list(value: Optional[List[str]]) -> Optional[str]:
    if value is None:
        return None
    return json.dumps([item for item in value if item], ensure_ascii=False)


def _profile_payload(profile: Optional[UserProfile], public: bool = False) -> dict:
    if not profile:
        return {
            "nickname": None,
            "avatarUrl": None,
            "bio": None,
            "authLevel": 0,
            "riskPreference": None,
            "influenceScore": 0,
            "experienceTags": [],
            "interestMarkets": [],
            "privacyLevel": 0,
            "postCount": 0,
            "eliteCount": 0,
            "points": 0,
            "level": 1,
            "badgeTitle": None,
        }
    hidden = public and profile.privacy_level == 2
    return {
        "nickname": profile.nickname,
        "avatarUrl": profile.avatar_url,
        "bio": None if hidden else profile.bio,
        "authLevel": profile.auth_level,
        "riskPreference": None if public else profile.risk_preference,
        "influenceScore": profile.influence_score,
        "experienceTags": [] if hidden else _loads_list(profile.experience_tags),
        "interestMarkets": [] if hidden else _loads_list(profile.interest_markets),
        "privacyLevel": profile.privacy_level,
        "postCount": profile.post_count,
        "eliteCount": profile.elite_count,
        "points": profile.points,
        "level": profile.level,
        "badgeTitle": profile.badge_title,
    }


@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    profile = current_user.profile
    role_name = current_user.roles[0].name if current_user.roles else "USER"
    data = {
        "id": current_user.id,
        "phone": current_user.phone,
        "email": current_user.email,
        "role": role_name,
        "status": current_user.status,
    }
    data.update(_profile_payload(profile))
    return success(data)


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
    if req.experience_tags is not None:
        profile.experience_tags = _dumps_list(req.experience_tags)
    if req.interest_markets is not None:
        profile.interest_markets = _dumps_list(req.interest_markets)
    if req.privacy_level is not None:
        profile.privacy_level = req.privacy_level

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
            "level": p.level if p else 1,
            "badgeTitle": p.badge_title if p else None,
        })

    return paginated(items, page, size, total)


@router.get("/{user_id}")
def get_user_public_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ResourceNotFoundError("用户不存在")

    profile = user.profile
    data = {"id": user.id}
    data.update(_profile_payload(profile, public=True))
    return success(data)
