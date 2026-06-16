from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("comments.id"), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    like_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    author: Mapped["User"] = relationship("User")
    post: Mapped["Post"] = relationship("Post")


class UserAction(Base):
    __tablename__ = "user_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    target_id: Mapped[int] = mapped_column(Integer, nullable=False)
    target_type: Mapped[int] = mapped_column(Integer, nullable=False)
    action_type: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)


class UserFollow(Base):
    __tablename__ = "user_follows"

    follower_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    followed_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    is_starred: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id])
    followed: Mapped["User"] = relationship("User", foreign_keys=[followed_id])


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    permission: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    creator: Mapped["User"] = relationship("User")
    members: Mapped[list["GroupMember"]] = relationship(
        "GroupMember",
        back_populates="group",
        cascade="all, delete-orphan",
    )


class GroupMember(Base):
    __tablename__ = "group_members"

    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    join_time: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    group: Mapped[Group] = relationship("Group", back_populates="members")
    user: Mapped["User"] = relationship("User")


class GroupJoinRequest(Base):
    __tablename__ = "group_join_requests"

    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    group: Mapped[Group] = relationship("Group")
    user: Mapped["User"] = relationship("User")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    notification_type: Mapped[str] = mapped_column(String(32), nullable=False, default="interaction")
    target_type: Mapped[str | None] = mapped_column(String(32), nullable=True)
    target_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User")
