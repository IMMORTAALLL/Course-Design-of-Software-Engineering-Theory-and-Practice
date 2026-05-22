from typing import Optional, Literal
from pydantic import BaseModel, Field, validator


class RegisterRequest(BaseModel):
    account_type: Literal["phone", "email"] = Field(alias="accountType")
    phone: Optional[str] = None
    email: Optional[str] = None
    password: str
    nickname: str
    verify_code: str = Field(alias="verifyCode")

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("密码长度不能少于8位")
        has_letter = any(c.isalpha() for c in v)
        has_digit = any(c.isdigit() for c in v)
        if not (has_letter and has_digit):
            raise ValueError("密码必须包含字母和数字")
        return v

    @validator("nickname")
    def validate_nickname(cls, v):
        if len(v) < 2 or len(v) > 20:
            raise ValueError("昵称长度需在2-20个字符之间")
        return v

    class Config:
        populate_by_name = True


class LoginRequest(BaseModel):
    account: str
    password: str


class UserBrief(BaseModel):
    id: int
    nickname: str
    auth_level: int = Field(alias="authLevel", default=0)
    role: str = "USER"
    status: int = 0

    class Config:
        populate_by_name = True
        from_attributes = True


class LoginResponseData(BaseModel):
    token: str
    user: UserBrief


class VerifyCodeRequest(BaseModel):
    account_type: Literal["phone", "email"] = Field(alias="accountType")
    target: str

    class Config:
        populate_by_name = True
