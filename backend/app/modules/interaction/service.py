from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session, joinedload

from app.common.exceptions import ConflictError, ForbiddenError, ResourceNotFoundError, StateNotAllowedError
from app.modules.admin.models import ReportItem
from app.modules.auth.models import User
from app.modules.forum.crud import get_post, post_to_item
from app.modules.forum.models import Post
from app.modules.interaction.models import (
    Comment,
    Group,
    GroupJoinRequest,
    GroupMember,
    Notification,
    UserAction,
    UserFollow,
)

POST_TARGET = 1
COMMENT_TARGET = 2
LIKE_ACTION = 1
FAVORITE_ACTION = 2


def _user_brief(user: User | None) -> dict:
    profile = user.profile if user and user.profile else None
    return {
        "id": user.id if user else 0,
        "nickname": profile.nickname if profile else "社区用户",
        "avatarUrl": profile.avatar_url if profile else None,
        "authLevel": profile.auth_level if profile else 0,
        "influenceScore": profile.influence_score if profile else 0,
    }


def _comment_to_dict(comment: Comment, replies: list[dict] | None = None) -> dict:
    author = _user_brief(comment.author)
    return {
        "id": comment.id,
        "postId": comment.post_id,
        "userId": comment.user_id,
        "parentId": comment.parent_id,
        "authorNickname": author["nickname"],
        "authorAuthLevel": author["authLevel"],
        "content": comment.content,
        "likeCount": comment.like_count,
        "createdAt": comment.created_at,
        "replies": replies or [],
    }


def _notification_to_dict(item: Notification) -> dict:
    return {
        "id": item.id,
        "title": item.title,
        "content": item.content,
        "notificationType": item.notification_type,
        "targetType": item.target_type,
        "targetId": item.target_id,
        "isRead": item.is_read,
        "createdAt": item.created_at,
    }


def _group_to_dict(db: Session, group: Group, current_user_id: int | None = None) -> dict:
    creator = _user_brief(group.creator)
    member_count = db.query(func.count(GroupMember.user_id)).filter(GroupMember.group_id == group.id).scalar() or 0
    joined = False
    pending = False
    if current_user_id:
        joined = db.get(GroupMember, {"group_id": group.id, "user_id": current_user_id}) is not None
        pending = (
            db.query(GroupJoinRequest)
            .filter(
                GroupJoinRequest.group_id == group.id,
                GroupJoinRequest.user_id == current_user_id,
                GroupJoinRequest.status == "pending",
            )
            .first()
            is not None
        )
    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "permission": group.permission,
        "creatorId": group.creator_id,
        "creatorNickname": creator["nickname"],
        "memberCount": member_count,
        "joined": joined,
        "pending": pending,
        "createdAt": group.created_at,
    }


def create_notification(
    db: Session,
    user_id: int,
    title: str,
    content: str,
    notification_type: str = "interaction",
    target_type: str | None = None,
    target_id: int | None = None,
) -> None:
    db.add(
        Notification(
            user_id=user_id,
            title=title,
            content=content,
            notification_type=notification_type,
            target_type=target_type,
            target_id=target_id,
        )
    )


def list_comments(db: Session, post_id: int) -> list[dict]:
    get_post(db, post_id, increase_view=False)
    comments = (
        db.query(Comment)
        .options(joinedload(Comment.author).joinedload(User.profile))
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.asc())
        .all()
    )
    replies_by_parent: dict[int, list[dict]] = {}
    roots: list[Comment] = []
    for comment in comments:
        if comment.parent_id:
            replies_by_parent.setdefault(comment.parent_id, []).append(_comment_to_dict(comment))
        else:
            roots.append(comment)
    return [_comment_to_dict(comment, replies_by_parent.get(comment.id, [])) for comment in roots]


def add_comment(db: Session, post_id: int, user: User, content: str, parent_id: int | None = None) -> dict:
    post = get_post(db, post_id, increase_view=False)
    if parent_id is not None:
        parent = db.query(Comment).filter(Comment.id == parent_id, Comment.post_id == post_id).first()
        if parent is None:
            raise ResourceNotFoundError("父级评论不存在")

    comment = Comment(post_id=post_id, user_id=user.id, parent_id=parent_id, content=content)
    db.add(comment)
    post.comment_count += 1

    if post.user_id != user.id:
        create_notification(
            db,
            post.user_id,
            "帖子收到新评论",
            f"{user.profile.nickname if user.profile else '社区用户'} 评论了你的帖子《{post.title}》",
            target_type="post",
            target_id=post.id,
        )

    db.commit()
    db.refresh(comment)
    comment = (
        db.query(Comment)
        .options(joinedload(Comment.author).joinedload(User.profile))
        .filter(Comment.id == comment.id)
        .first()
    )
    return _comment_to_dict(comment)


def delete_comment(db: Session, comment_id: int, user: User) -> dict:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise ResourceNotFoundError("评论不存在")
    role_names = {role.name for role in user.roles}
    if comment.user_id != user.id and "ADMIN" not in role_names:
        raise ForbiddenError("只能删除自己的评论")

    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if post and post.comment_count > 0:
        child_count = db.query(func.count(Comment.id)).filter(Comment.parent_id == comment.id).scalar() or 0
        post.comment_count = max(0, post.comment_count - 1 - child_count)
    db.query(Comment).filter((Comment.id == comment_id) | (Comment.parent_id == comment_id)).delete(synchronize_session=False)
    db.commit()
    return {"id": comment_id}


def _toggle_action(db: Session, user_id: int, target_id: int, target_type: int, action_type: int) -> bool:
    action = (
        db.query(UserAction)
        .filter(
            UserAction.user_id == user_id,
            UserAction.target_id == target_id,
            UserAction.target_type == target_type,
            UserAction.action_type == action_type,
        )
        .first()
    )
    if action:
        db.delete(action)
        return False
    db.add(
        UserAction(
            user_id=user_id,
            target_id=target_id,
            target_type=target_type,
            action_type=action_type,
        )
    )
    return True


def toggle_post_like(db: Session, post_id: int, user: User) -> dict:
    post = get_post(db, post_id, increase_view=False)
    active = _toggle_action(db, user.id, post_id, POST_TARGET, LIKE_ACTION)
    post.like_count = max(0, post.like_count + (1 if active else -1))
    if active and post.user_id != user.id:
        create_notification(
            db,
            post.user_id,
            "帖子收到点赞",
            f"{user.profile.nickname if user.profile else '社区用户'} 点赞了你的帖子《{post.title}》",
            target_type="post",
            target_id=post.id,
        )
    db.commit()
    return {"active": active, "count": post.like_count}


def toggle_comment_like(db: Session, comment_id: int, user: User) -> dict:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise ResourceNotFoundError("评论不存在")
    active = _toggle_action(db, user.id, comment_id, COMMENT_TARGET, LIKE_ACTION)
    comment.like_count = max(0, comment.like_count + (1 if active else -1))
    db.commit()
    return {"active": active, "count": comment.like_count}


def get_post_interaction_status(db: Session, post_id: int, user: User) -> dict:
    post = get_post(db, post_id, increase_view=False)
    liked = (
        db.query(UserAction.id)
        .filter(
            UserAction.user_id == user.id,
            UserAction.target_id == post_id,
            UserAction.target_type == POST_TARGET,
            UserAction.action_type == LIKE_ACTION,
        )
        .first()
        is not None
    )
    favorited = (
        db.query(UserAction.id)
        .filter(
            UserAction.user_id == user.id,
            UserAction.target_id == post_id,
            UserAction.target_type == POST_TARGET,
            UserAction.action_type == FAVORITE_ACTION,
        )
        .first()
        is not None
    )
    following_author = False
    if post.user_id != user.id:
        following_author = db.get(UserFollow, {"follower_id": user.id, "followed_id": post.user_id}) is not None
    return {"liked": liked, "favorited": favorited, "followingAuthor": following_author}


def toggle_post_favorite(db: Session, post_id: int, user: User) -> dict:
    get_post(db, post_id, increase_view=False)
    active = _toggle_action(db, user.id, post_id, POST_TARGET, FAVORITE_ACTION)
    db.flush()
    total = (
        db.query(func.count(UserAction.id))
        .filter(
            UserAction.target_id == post_id,
            UserAction.target_type == POST_TARGET,
            UserAction.action_type == FAVORITE_ACTION,
        )
        .scalar()
        or 0
    )
    db.commit()
    return {"active": active, "count": total}


def report_post(db: Session, post_id: int, user: User, reason: str) -> dict:
    post = get_post(db, post_id, increase_view=False)
    reporter_name = user.profile.nickname if user.profile else "社区用户"
    item = ReportItem(
        target_type="post",
        target_title=post.title,
        reporter_name=reporter_name,
        reason=reason,
        status="pending",
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "status": item.status}


def report_comment(db: Session, comment_id: int, user: User, reason: str) -> dict:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment is None:
        raise ResourceNotFoundError("评论不存在")
    reporter_name = user.profile.nickname if user.profile else "社区用户"
    content_summary = comment.content[:60] + ("..." if len(comment.content) > 60 else "")
    item = ReportItem(
        target_type="comment",
        target_title=content_summary,
        reporter_name=reporter_name,
        reason=reason,
        status="pending",
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "status": item.status}


def list_favorite_posts(db: Session, user: User, page: int, size: int) -> tuple[list[dict], int]:
    base = (
        db.query(Post)
        .join(UserAction, UserAction.target_id == Post.id)
        .filter(
            UserAction.user_id == user.id,
            UserAction.target_type == POST_TARGET,
            UserAction.action_type == FAVORITE_ACTION,
            Post.status == "PUBLISHED",
        )
    )
    total = base.count()
    posts = (
        base.options(
            joinedload(Post.section),
            joinedload(Post.author).joinedload(User.profile),
            joinedload(Post.tags),
        )
        .order_by(desc(UserAction.created_at))
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return [post_to_item(post) for post in posts], total


def toggle_follow(db: Session, target_user_id: int, user: User) -> dict:
    if target_user_id == user.id:
        raise ConflictError("不能关注自己")
    target = db.query(User).filter(User.id == target_user_id).first()
    if target is None:
        raise ResourceNotFoundError("用户不存在")
    follow = db.get(UserFollow, {"follower_id": user.id, "followed_id": target_user_id})
    following = follow is None
    if follow:
        db.delete(follow)
    else:
        db.add(UserFollow(follower_id=user.id, followed_id=target_user_id))
        create_notification(
            db,
            target_user_id,
            "新增关注",
            f"{user.profile.nickname if user.profile else '社区用户'} 关注了你",
            target_type="user",
            target_id=user.id,
        )
    follower_count = db.query(func.count(UserFollow.follower_id)).filter(UserFollow.followed_id == target_user_id).scalar() or 0
    db.commit()
    return {"following": following, "followerCount": follower_count}


def list_followers(db: Session, user_id: int) -> list[dict]:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ResourceNotFoundError("用户不存在")
    followers = (
        db.query(User)
        .join(UserFollow, UserFollow.follower_id == User.id)
        .options(joinedload(User.profile))
        .filter(UserFollow.followed_id == user_id)
        .order_by(desc(UserFollow.created_at))
        .all()
    )
    return [_user_brief(item) for item in followers]


def list_following(db: Session, user_id: int) -> list[dict]:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise ResourceNotFoundError("用户不存在")
    following = (
        db.query(User)
        .join(UserFollow, UserFollow.followed_id == User.id)
        .options(joinedload(User.profile))
        .filter(UserFollow.follower_id == user_id)
        .order_by(desc(UserFollow.created_at))
        .all()
    )
    return [_user_brief(item) for item in following]


def list_following_feed(db: Session, user: User, page: int, size: int) -> tuple[list[dict], int]:
    followed_ids = select(UserFollow.followed_id).filter(UserFollow.follower_id == user.id)
    base = db.query(Post).filter(Post.user_id.in_(followed_ids), Post.status == "PUBLISHED")
    total = base.count()
    posts = (
        base.options(
            joinedload(Post.section),
            joinedload(Post.author).joinedload(User.profile),
            joinedload(Post.tags),
        )
        .order_by(desc(Post.created_at))
        .offset((page - 1) * size)
        .limit(size)
        .all()
    )
    return [post_to_item(post) for post in posts], total


def list_notifications(db: Session, user: User) -> list[dict]:
    items = (
        db.query(Notification)
        .filter(Notification.user_id == user.id)
        .order_by(Notification.is_read.asc(), Notification.created_at.desc())
        .all()
    )
    return [_notification_to_dict(item) for item in items]


def mark_notification_read(db: Session, notification_id: int, user: User) -> dict:
    item = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user.id).first()
    if item is None:
        raise ResourceNotFoundError("通知不存在")
    item.is_read = True
    db.commit()
    db.refresh(item)
    return _notification_to_dict(item)


def list_groups(db: Session, current_user_id: int | None = None) -> list[dict]:
    groups = (
        db.query(Group)
        .options(joinedload(Group.creator).joinedload(User.profile))
        .order_by(desc(Group.created_at))
        .all()
    )
    return [_group_to_dict(db, group, current_user_id) for group in groups]


def create_group(db: Session, user: User, name: str, description: str | None, permission: int) -> dict:
    group = Group(creator_id=user.id, name=name, description=description, permission=permission)
    db.add(group)
    db.flush()
    db.add(GroupMember(group_id=group.id, user_id=user.id))
    db.commit()
    db.refresh(group)
    group = (
        db.query(Group)
        .options(joinedload(Group.creator).joinedload(User.profile))
        .filter(Group.id == group.id)
        .first()
    )
    return _group_to_dict(db, group, user.id)


def get_group(db: Session, group_id: int, current_user_id: int | None = None) -> dict:
    group = (
        db.query(Group)
        .options(joinedload(Group.creator).joinedload(User.profile))
        .filter(Group.id == group_id)
        .first()
    )
    if group is None:
        raise ResourceNotFoundError("群组不存在")
    return _group_to_dict(db, group, current_user_id)


def join_group(db: Session, group_id: int, user: User) -> dict:
    group = db.query(Group).filter(Group.id == group_id).first()
    if group is None:
        raise ResourceNotFoundError("群组不存在")
    existing = db.get(GroupMember, {"group_id": group_id, "user_id": user.id})
    if existing is not None:
        return get_group(db, group_id, user.id)
    if group.permission == 3:
        raise ForbiddenError("私密群组暂不开放直接加入")
    if group.permission == 2:
        request = db.get(GroupJoinRequest, {"group_id": group_id, "user_id": user.id})
        if request is None:
            db.add(GroupJoinRequest(group_id=group_id, user_id=user.id, status="pending"))
            if group.creator_id != user.id:
                create_notification(
                    db,
                    group.creator_id,
                    "群组收到加入申请",
                    f"{user.profile.nickname if user.profile else '社区用户'} 申请加入群组「{group.name}」",
                    target_type="group",
                    target_id=group.id,
                )
        elif request.status != "pending":
            request.status = "pending"
        db.commit()
        return get_group(db, group_id, user.id)
    db.add(GroupMember(group_id=group_id, user_id=user.id))
    if group.creator_id != user.id:
        create_notification(
            db,
            group.creator_id,
            "群组新增成员",
            f"{user.profile.nickname if user.profile else '社区用户'} 加入了群组「{group.name}」",
            target_type="group",
            target_id=group.id,
        )
    db.commit()
    return get_group(db, group_id, user.id)


def leave_group(db: Session, group_id: int, user: User) -> dict:
    group = db.query(Group).filter(Group.id == group_id).first()
    if group is None:
        raise ResourceNotFoundError("群组不存在")
    if group.creator_id == user.id:
        raise StateNotAllowedError("群主不能直接退出自己创建的群组")
    member = db.get(GroupMember, {"group_id": group_id, "user_id": user.id})
    if member:
        db.delete(member)
        db.commit()
    else:
        request = db.get(GroupJoinRequest, {"group_id": group_id, "user_id": user.id})
        if request and request.status == "pending":
            db.delete(request)
            db.commit()
    return get_group(db, group_id, user.id)
