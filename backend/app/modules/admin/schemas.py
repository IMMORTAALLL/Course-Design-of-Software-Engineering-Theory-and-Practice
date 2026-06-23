from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class AdminOverview(BaseModel):
    today_posts: int
    pending_audits: int
    pending_reports: int
    active_sensitive_words: int


class AuditQueueItemOut(BaseModel):
    id: int
    content_type: str
    title: str
    author_name: str
    reason: str
    risk_level: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReportItemOut(BaseModel):
    id: int
    target_type: str
    target_title: str
    reporter_name: str
    reason: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class SensitiveWordOut(BaseModel):
    id: int
    keyword: str
    category: str
    risk_level: str
    action: str
    enabled: bool
    note: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AuditDecisionIn(BaseModel):
    action: str


class ReportDecisionIn(BaseModel):
    action: str


class SensitiveWordToggleIn(BaseModel):
    enabled: bool


class UserModerationRecordOut(BaseModel):
    id: int
    user_name: str
    action: str
    reason: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AdminStatistics(BaseModel):
    hot_topics: List[str]
    active_sections: List[Dict[str, Union[int, str]]]
