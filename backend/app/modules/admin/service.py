from sqlalchemy import func
from sqlalchemy.orm import Session

from app.common.exceptions import ParamValidationError, ResourceNotFoundError, StateNotAllowedError
from app.modules.admin.models import AuditQueueItem, ReportItem, SensitiveWord, UserModerationRecord


def get_admin_overview(db: Session) -> dict:
    pending_audits = db.query(func.count(AuditQueueItem.id)).filter(AuditQueueItem.status == "pending").scalar() or 0
    pending_reports = db.query(func.count(ReportItem.id)).filter(ReportItem.status == "pending").scalar() or 0
    active_sensitive_words = db.query(func.count(SensitiveWord.id)).filter(SensitiveWord.enabled.is_(True)).scalar() or 0

    return {
        "today_posts": 328,
        "pending_audits": pending_audits,
        "pending_reports": pending_reports,
        "active_sensitive_words": active_sensitive_words,
    }


def list_audit_queue(db: Session) -> list[AuditQueueItem]:
    return db.query(AuditQueueItem).order_by(AuditQueueItem.created_at.desc()).all()


def list_reports(db: Session) -> list[ReportItem]:
    return db.query(ReportItem).order_by(ReportItem.created_at.desc()).all()


def list_sensitive_words(db: Session) -> list[SensitiveWord]:
    return db.query(SensitiveWord).order_by(SensitiveWord.created_at.desc()).all()


def list_user_moderation_records(db: Session) -> list[UserModerationRecord]:
    return db.query(UserModerationRecord).order_by(UserModerationRecord.created_at.desc()).all()


def get_admin_statistics() -> dict:
    return {
        "hot_topics": ["新能源", "宽基定投", "高股息", "ETF 轮动", "风险提示"],
        "active_sections": [
            {"name": "A股讨论区", "value": 128},
            {"name": "基金投资专区", "value": 96},
            {"name": "量化投资专区", "value": 74},
            {"name": "问答求助区", "value": 53},
        ],
    }


def decide_audit_item(db: Session, item_id: int, action: str) -> AuditQueueItem:
    item = db.query(AuditQueueItem).filter(AuditQueueItem.id == item_id).first()
    if item is None:
        raise ResourceNotFoundError("审核内容不存在")
    if item.status not in {"pending", "reviewing"}:
        raise StateNotAllowedError("当前状态下不能继续审核")

    if action == "approve":
        item.status = "approved"
    elif action == "reject":
        item.status = "rejected"
    else:
        raise ParamValidationError("不支持的审核动作")

    db.commit()
    db.refresh(item)
    return item


def decide_report_item(db: Session, item_id: int, action: str) -> ReportItem:
    item = db.query(ReportItem).filter(ReportItem.id == item_id).first()
    if item is None:
        raise ResourceNotFoundError("举报记录不存在")
    if item.status not in {"pending", "reviewing"}:
        raise StateNotAllowedError("当前状态下不能继续处理举报")

    allowed_actions = {"dismissed", "warning_issued", "banned"}
    if action not in allowed_actions:
        raise ParamValidationError("不支持的举报处理动作")

    item.status = action
    db.commit()
    db.refresh(item)
    return item


def toggle_sensitive_word(db: Session, word_id: int, enabled: bool) -> SensitiveWord:
    word = db.query(SensitiveWord).filter(SensitiveWord.id == word_id).first()
    if word is None:
        raise ResourceNotFoundError("敏感词不存在")

    word.enabled = enabled
    db.commit()
    db.refresh(word)
    return word
