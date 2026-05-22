from datetime import datetime

from pydantic import BaseModel, Field


class TagRead(BaseModel):
    id: int
    name: str
    tag_type: str

    model_config = {"from_attributes": True}


class SectionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    sort_order: int = 0
    is_active: int = 1


class SectionRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    sort_order: int
    is_active: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PostCreate(BaseModel):
    section_id: int
    title: str = Field(..., min_length=1, max_length=120)
    content: str = Field(..., min_length=1)
    tag_ids: list[int] = Field(default_factory=list)


class PostUpdate(BaseModel):
    section_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=120)
    content: str | None = Field(default=None, min_length=1)
    tag_ids: list[int] | None = None
    status: str | None = None


class PostListItem(BaseModel):
    id: int
    section_id: int
    section_name: str
    user_id: int
    title: str
    summary: str
    status: str
    view_count: int
    like_count: int
    comment_count: int
    created_at: datetime
    tags: list[TagRead] = Field(default_factory=list)


class PostRead(PostListItem):
    content: str
    updated_at: datetime


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    tag_type: str = "TOPIC"
