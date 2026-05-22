from typing import Optional
from pydantic import BaseModel, Field, validator


class ProfileUpdateRequest(BaseModel):
    nickname: Optional[str] = None
    avatar_url: Optional[str] = Field(None, alias="avatarUrl")
    bio: Optional[str] = None
    risk_preference: Optional[int] = Field(None, alias="riskPreference")

    @validator("nickname")
    def validate_nickname(cls, v):
        if v is not None and (len(v) < 2 or len(v) > 20):
            raise ValueError("昵称长度需在2-20个字符之间")
        return v

    @validator("risk_preference")
    def validate_risk(cls, v):
        if v is not None and v not in (1, 2, 3):
            raise ValueError("风险偏好只能为1(保守)、2(稳健)、3(进取)")
        return v

    class Config:
        populate_by_name = True


class UserPublicProfile(BaseModel):
    id: int
    nickname: Optional[str] = None
    avatar_url: Optional[str] = Field(None, alias="avatarUrl")
    bio: Optional[str] = None
    auth_level: int = Field(0, alias="authLevel")
    influence_score: int = Field(0, alias="influenceScore")

    class Config:
        populate_by_name = True
        from_attributes = True
