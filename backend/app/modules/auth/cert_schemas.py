from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class CertificationRequest(BaseModel):
    certification_type: Literal["REAL_NAME", "PROFESSIONAL"] = Field(alias="certificationType")
    real_name: str = Field(alias="realName")
    material_urls: Optional[List[str]] = Field(None, alias="materialUrls")

    class Config:
        populate_by_name = True


class CertificationResponse(BaseModel):
    auth_level: int = Field(alias="authLevel")
    certification_type: Optional[str] = Field(None, alias="certificationType")
    status: str

    class Config:
        populate_by_name = True


class RiskAssessmentRequest(BaseModel):
    answers: List[int]


class RiskAssessmentResponse(BaseModel):
    risk_preference: int = Field(alias="riskPreference")
    label: str

    class Config:
        populate_by_name = True
