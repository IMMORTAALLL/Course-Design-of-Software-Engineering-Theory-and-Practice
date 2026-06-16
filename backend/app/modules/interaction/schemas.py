from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)


class ReportCreate(BaseModel):
    reason: str = Field(..., min_length=1, max_length=255)


class CommentOut(BaseModel):
    id: int
    post_id: int = Field(alias="postId")
    user_id: int = Field(alias="userId")
    parent_id: int | None = Field(None, alias="parentId")
    author_nickname: str = Field(alias="authorNickname")
    author_auth_level: int = Field(0, alias="authorAuthLevel")
    content: str
    like_count: int = Field(alias="likeCount")
    created_at: datetime = Field(alias="createdAt")
    replies: list["CommentOut"] = Field(default_factory=list)

    model_config = {"populate_by_name": True}


class ToggleResult(BaseModel):
    active: bool
    count: int


class InteractionStatusOut(BaseModel):
    liked: bool = False
    favorited: bool = False
    following_author: bool = Field(False, alias="followingAuthor")

    model_config = {"populate_by_name": True}


class FollowResult(BaseModel):
    following: bool
    follower_count: int = Field(alias="followerCount")

    model_config = {"populate_by_name": True}


class UserBriefOut(BaseModel):
    id: int
    nickname: str | None = None
    avatar_url: str | None = Field(None, alias="avatarUrl")
    auth_level: int = Field(0, alias="authLevel")
    influence_score: int = Field(0, alias="influenceScore")

    model_config = {"populate_by_name": True}


class NotificationOut(BaseModel):
    id: int
    title: str
    content: str
    notification_type: str = Field(alias="notificationType")
    target_type: str | None = Field(None, alias="targetType")
    target_id: int | None = Field(None, alias="targetId")
    is_read: bool = Field(alias="isRead")
    created_at: datetime = Field(alias="createdAt")

    model_config = {"populate_by_name": True}


class GroupCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    permission: Literal[1, 2, 3] = 1


class GroupOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    permission: int
    creator_id: int = Field(alias="creatorId")
    creator_nickname: str = Field(alias="creatorNickname")
    member_count: int = Field(alias="memberCount")
    joined: bool
    pending: bool = False
    created_at: datetime = Field(alias="createdAt")

    model_config = {"populate_by_name": True}
