from typing import Optional
from pydantic import BaseModel, Field


class UserStatusUpdateRequest(BaseModel):
    status: int
    reason: Optional[str] = None
