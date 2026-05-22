from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.common.response import success
from app.common.deps import get_current_user
from app.modules.auth.models import User, UserProfile
from app.modules.auth.cert_schemas import (
    CertificationRequest, RiskAssessmentRequest
)

router = APIRouter(prefix="/api/users/me", tags=["Certification"])


@router.post("/certification")
def submit_certification(
    req: CertificationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profile = current_user.profile
    if not profile:
        profile = UserProfile(user_id=current_user.id, nickname="用户")
        db.add(profile)

    if req.certification_type == "REAL_NAME":
        profile.auth_level = max(profile.auth_level, 1)
    elif req.certification_type == "PROFESSIONAL":
        profile.auth_level = 2

    db.commit()
    return success({
        "authLevel": profile.auth_level,
        "message": "认证已通过（模拟）",
    })


@router.get("/certification")
def get_certification_status(current_user: User = Depends(get_current_user)):
    profile = current_user.profile
    auth_level = profile.auth_level if profile else 0

    status_map = {0: "未认证", 1: "实名认证", 2: "专业认证"}
    return success({
        "authLevel": auth_level,
        "status": status_map.get(auth_level, "未认证"),
    })


@router.post("/risk-assessment")
def submit_risk_assessment(
    req: RiskAssessmentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    total = sum(req.answers)
    count = len(req.answers) if req.answers else 1
    avg = total / count

    if avg <= 1.5:
        risk_preference = 1
        label = "保守型"
    elif avg <= 2.5:
        risk_preference = 2
        label = "稳健型"
    else:
        risk_preference = 3
        label = "进取型"

    profile = current_user.profile
    if not profile:
        profile = UserProfile(user_id=current_user.id, nickname="用户")
        db.add(profile)

    profile.risk_preference = risk_preference
    db.commit()

    return success({
        "riskPreference": risk_preference,
        "label": label,
    })
