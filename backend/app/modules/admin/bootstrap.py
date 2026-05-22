from sqlalchemy.orm import Session

from app.modules.admin.models import AuditQueueItem, ReportItem, SensitiveWord, UserModerationRecord


def seed_admin_demo_data(db: Session) -> None:
    if db.query(AuditQueueItem).first() is None:
        db.add_all(
            [
                AuditQueueItem(
                    content_type="post",
                    title="推荐某股票明天必涨停",
                    author_name="短线猎手",
                    reason="违规荐股",
                    risk_level="high",
                    status="pending",
                ),
                AuditQueueItem(
                    content_type="comment",
                    title="保证收益，跟单联系我",
                    author_name="暴涨带队",
                    reason="广告引流",
                    risk_level="high",
                    status="pending",
                ),
                AuditQueueItem(
                    content_type="attachment",
                    title="基金收益分析表",
                    author_name="稳健定投者",
                    reason="附件待审核",
                    risk_level="medium",
                    status="reviewing",
                ),
            ]
        )

    if db.query(ReportItem).first() is None:
        db.add_all(
            [
                ReportItem(
                    target_type="post",
                    target_title="内部消息，今晚布局",
                    reporter_name="价值观察员",
                    reason="虚假荐股",
                    status="pending",
                ),
                ReportItem(
                    target_type="comment",
                    target_title="拉你进群带你赚钱",
                    reporter_name="理性投资人",
                    reason="广告引流",
                    status="pending",
                ),
            ]
        )

    if db.query(SensitiveWord).first() is None:
        db.add_all(
            [
                SensitiveWord(
                    keyword="稳赚不赔",
                    category="违规荐股",
                    risk_level="high",
                    action="manual_review",
                    enabled=True,
                    note="高风险承诺收益表述",
                ),
                SensitiveWord(
                    keyword="内部消息",
                    category="违规荐股",
                    risk_level="high",
                    action="manual_review",
                    enabled=True,
                    note="涉及未证实内幕信息",
                ),
                SensitiveWord(
                    keyword="带单",
                    category="广告引流",
                    risk_level="medium",
                    action="manual_review",
                    enabled=True,
                    note="常见引流词",
                ),
            ]
        )

    if db.query(UserModerationRecord).first() is None:
        db.add_all(
            [
                UserModerationRecord(
                    user_name="暴涨带队",
                    action="warning",
                    reason="多次发布广告引流评论",
                    status="active",
                ),
                UserModerationRecord(
                    user_name="内幕先知道",
                    action="mute",
                    reason="散布未证实内幕消息",
                    status="muted",
                ),
                UserModerationRecord(
                    user_name="稳赚俱乐部",
                    action="ban",
                    reason="反复发布违规荐股内容",
                    status="banned",
                ),
            ]
        )

    db.commit()
