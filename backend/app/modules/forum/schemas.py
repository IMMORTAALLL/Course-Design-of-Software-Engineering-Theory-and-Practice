from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class TagRead(BaseModel):
    id: int
    name: str
    tag_type: str

    model_config = {"from_attributes": True}


class SectionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    sort_order: int = 0
    is_active: int = 1


class SectionUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    description: Optional[str] = Field(default=None, max_length=255)
    sort_order: Optional[int] = None
    is_active: Optional[int] = None


class SectionRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    sort_order: int
    is_active: int
    created_at: datetime

    model_config = {"from_attributes": True}


class PostCreate(BaseModel):
    section_id: int
    title: str = Field(..., min_length=1, max_length=120)
    content: str = Field(..., min_length=1)
    post_type: int = 1
    tag_ids: List[int] = Field(default_factory=list)


class PostUpdate(BaseModel):
    section_id: Optional[int] = None
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    content: Optional[str] = Field(default=None, min_length=1)
    tag_ids: Optional[List[int]] = None
    status: Optional[str] = None


class PostListItem(BaseModel):
    id: int
    section_id: int
    section_name: str
    user_id: int
    author_nickname: Optional[str] = None
    author_auth_level: int = 0
    title: str
    summary: str
    post_type: int
    status: str
    view_count: int
    like_count: int
    comment_count: int
    is_elite: int
    created_at: datetime
    tags: List[TagRead] = Field(default_factory=list)


class PostRead(PostListItem):
    content: str
    updated_at: datetime


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    tag_type: str = "TOPIC"


class TagUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    tag_type: Optional[str] = None


class AttachmentCreate(BaseModel):
    file_url: str = Field(..., alias="fileUrl", min_length=1, max_length=255)
    file_type: str = Field(..., alias="fileType", min_length=1, max_length=20)

    model_config = {"populate_by_name": True}


class AttachmentRead(BaseModel):
    id: int
    post_id: int = Field(alias="postId")
    file_url: str = Field(alias="fileUrl")
    file_type: str = Field(alias="fileType")
    created_at: datetime = Field(alias="createdAt")

    model_config = {"populate_by_name": True}


class PollOptionCreate(BaseModel):
    option_text: str = Field(..., alias="optionText", min_length=1, max_length=120)

    model_config = {"populate_by_name": True}


class PollOptionRead(BaseModel):
    id: int
    post_id: int = Field(alias="postId")
    option_text: str = Field(alias="optionText")
    vote_count: int = Field(alias="voteCount")

    model_config = {"populate_by_name": True}
