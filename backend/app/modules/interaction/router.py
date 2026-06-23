from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.deps import get_current_user, get_db, oauth2_scheme
from app.common.response import paginated, success
from app.modules.auth.models import User
from app.security.jwt import decode_access_token
from app.modules.interaction import service
from app.modules.interaction.models import Comment
from app.modules.interaction.schemas import (
    CommentCreate,
    GroupCreate,
    GroupPostCreate,
    GroupResourceCreate,
    PrivateMessageCreate,
    ReportCreate,
)

router = APIRouter(prefix="/api", tags=["interaction"])


def get_optional_user_id(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[int]:
    if not token:
        return None
    payload = decode_access_token(token)
    if not payload:
        return None
    try:
        user_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        return None
    exists = db.query(User.id).filter(User.id == user_id).first()
    return user_id if exists else None


@router.get("/posts/{post_id}/comments")
def list_post_comments(post_id: int, db: Session = Depends(get_db)):
    return success(service.list_comments(db, post_id))


@router.post("/posts/{post_id}/comments")
def create_post_comment(
    post_id: int,
    payload: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.add_comment(db, post_id, current_user, payload.content), "评论发布成功")


@router.post("/comments/{comment_id}/replies")
def create_comment_reply(
    comment_id: int,
    payload: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    parent = db.query(Comment).filter(Comment.id == comment_id).first()
    if parent is None:
        from app.common.exceptions import ResourceNotFoundError

        raise ResourceNotFoundError("评论不存在")
    return success(
        service.add_comment(db, parent.post_id, current_user, payload.content, parent_id=comment_id),
        "回复发布成功",
    )


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.delete_comment(db, comment_id, current_user), "评论已删除")


@router.post("/posts/{post_id}/like")
def toggle_post_like(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.toggle_post_like(db, post_id, current_user))


@router.get("/posts/{post_id}/interaction-status")
def get_post_interaction_status(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.get_post_interaction_status(db, post_id, current_user))


@router.post("/comments/{comment_id}/like")
def toggle_comment_like(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.toggle_comment_like(db, comment_id, current_user))


@router.post("/posts/{post_id}/report")
def report_post(
    post_id: int,
    payload: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.report_post(db, post_id, current_user, payload.reason), "举报已提交")


@router.post("/comments/{comment_id}/report")
def report_comment(
    comment_id: int,
    payload: ReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.report_comment(db, comment_id, current_user, payload.reason), "举报已提交")


@router.post("/posts/{post_id}/favorite")
def toggle_post_favorite(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.toggle_post_favorite(db, post_id, current_user))


@router.get("/me/favorites")
def list_my_favorites(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = service.list_favorite_posts(db, current_user, page, size)
    return paginated(items, page, size, total)


@router.post("/users/{user_id}/follow")
def toggle_user_follow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.toggle_follow(db, user_id, current_user))


@router.put("/users/{user_id}/follow/star")
def set_starred_follow(
    user_id: int,
    starred: bool = Query(True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.set_starred_follow(db, user_id, current_user, starred))


@router.get("/users/{user_id}/followers")
def list_user_followers(user_id: int, db: Session = Depends(get_db)):
    return success(service.list_followers(db, user_id))


@router.get("/users/{user_id}/following")
def list_user_following(user_id: int, db: Session = Depends(get_db)):
    return success(service.list_following(db, user_id))


@router.get("/feed/following")
def list_following_feed(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = service.list_following_feed(db, current_user, page, size)
    return paginated(items, page, size, total)


@router.get("/me/notifications")
def list_my_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.list_notifications(db, current_user))


@router.put("/me/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.mark_notification_read(db, notification_id, current_user), "通知已标记为已读")


@router.get("/me/messages")
def list_my_messages(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.list_private_messages(db, current_user))


@router.post("/users/{user_id}/messages")
def send_user_message(
    user_id: int,
    payload: PrivateMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.send_private_message(db, user_id, current_user, payload.content), "Message sent")


@router.get("/groups")
def list_groups(
    current_user_id: Optional[int] = Depends(get_optional_user_id),
    db: Session = Depends(get_db),
):
    return success(service.list_groups(db, current_user_id))


@router.post("/groups")
def create_group(
    payload: GroupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(
        service.create_group(db, current_user, payload.name, payload.description, payload.permission),
        "群组创建成功",
    )


@router.get("/groups/{group_id}")
def get_group(
    group_id: int,
    current_user_id: Optional[int] = Depends(get_optional_user_id),
    db: Session = Depends(get_db),
):
    return success(service.get_group(db, group_id, current_user_id))


@router.get("/groups/{group_id}/posts")
def list_group_posts(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.list_group_posts(db, group_id, current_user))


@router.post("/groups/{group_id}/posts")
def create_group_post(
    group_id: int,
    payload: GroupPostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.create_group_post(db, group_id, current_user, payload.content), "Group post created")


@router.get("/groups/{group_id}/resources")
def list_group_resources(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.list_group_resources(db, group_id, current_user))


@router.post("/groups/{group_id}/resources")
def create_group_resource(
    group_id: int,
    payload: GroupResourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(
        service.create_group_resource(
            db,
            group_id,
            current_user,
            payload.title,
            payload.resource_url,
            payload.description,
        ),
        "Group resource created",
    )


@router.post("/groups/{group_id}/join")
def join_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    data = service.join_group(db, group_id, current_user)
    message = "已提交加入申请" if data.get("pending") and not data.get("joined") else "已加入群组"
    return success(data, message)


@router.delete("/groups/{group_id}/members/me")
def leave_group(
    group_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success(service.leave_group(db, group_id, current_user), "已退出群组")
