from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.deps import get_db, require_admin
from app.common.response import success
from app.modules.admin import service
from app.modules.admin.schemas import (
    AdminStatistics,
    AuditDecisionIn,
    AuditQueueItemOut,
    ReportDecisionIn,
    ReportItemOut,
    SensitiveWordOut,
    SensitiveWordToggleIn,
    UserModerationRecordOut,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/overview")
def admin_overview(admin=Depends(require_admin), db: Session = Depends(get_db)):
    return success(service.get_admin_overview(db))


@router.get("/audit-queue")
def audit_queue(admin=Depends(require_admin), db: Session = Depends(get_db)):
    items = service.list_audit_queue(db)
    return success([AuditQueueItemOut.model_validate(item).model_dump() for item in items])


@router.get("/reports")
def report_list(admin=Depends(require_admin), db: Session = Depends(get_db)):
    items = service.list_reports(db)
    return success([ReportItemOut.model_validate(item).model_dump() for item in items])


@router.get("/sensitive-words")
def sensitive_word_list(admin=Depends(require_admin), db: Session = Depends(get_db)):
    items = service.list_sensitive_words(db)
    return success([SensitiveWordOut.model_validate(item).model_dump() for item in items])


@router.patch("/audit-queue/{item_id}")
def audit_queue_decision(
    item_id: int,
    payload: AuditDecisionIn,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    item = service.decide_audit_item(db, item_id, payload.action)
    return success(AuditQueueItemOut.model_validate(item).model_dump(), "审核状态已更新")


@router.patch("/reports/{item_id}")
def report_decision(
    item_id: int,
    payload: ReportDecisionIn,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    item = service.decide_report_item(db, item_id, payload.action)
    return success(ReportItemOut.model_validate(item).model_dump(), "举报处理结果已更新")


@router.patch("/sensitive-words/{word_id}")
def sensitive_word_toggle(
    word_id: int,
    payload: SensitiveWordToggleIn,
    admin=Depends(require_admin),
    db: Session = Depends(get_db),
):
    word = service.toggle_sensitive_word(db, word_id, payload.enabled)
    return success(SensitiveWordOut.model_validate(word).model_dump(), "敏感词状态已更新")


@router.get("/user-moderation")
def user_moderation_records(admin=Depends(require_admin), db: Session = Depends(get_db)):
    items = service.list_user_moderation_records(db)
    return success([UserModerationRecordOut.model_validate(item).model_dump() for item in items])


@router.get("/statistics")
def admin_statistics(admin=Depends(require_admin)):
    return success(AdminStatistics.model_validate(service.get_admin_statistics()).model_dump())
