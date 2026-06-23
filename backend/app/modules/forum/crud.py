from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.common.exceptions import ResourceNotFoundError
from app.modules.admin.models import AuditQueueItem, SensitiveWord
from app.modules.auth.models import User, UserProfile
from app.modules.forum.models import Attachment, PollOption, PollVote, Post, PostTag, Section, Tag
from app.modules.forum.schemas import (
    AttachmentCreate,
    PollOptionCreate,
    PostCreate,
    PostUpdate,
    SectionCreate,
    SectionUpdate,
    TagCreate,
    TagUpdate,
)

PUBLISHED_STATUS = "PUBLISHED"
DELETED_STATUS = "DELETED"


def _post_tags(post: Post) -> list[Tag]:
    return [item.tag for item in post.tags if item.tag is not None]


def section_to_read(section: Section) -> dict:
    return {
        "id": section.id,
        "name": section.name,
        "description": section.description,
        "sort_order": section.sort_order,
        "is_active": section.is_active,
        "created_at": section.created_at,
    }


def tag_to_read(tag: Tag) -> dict:
    return {"id": tag.id, "name": tag.name, "tag_type": tag.tag_type}


def post_to_item(post: Post) -> dict:
    summary = post.content[:120] + ("..." if len(post.content) > 120 else "")
    author_profile = post.author.profile if post.author and post.author.profile else None
    return {
        "id": post.id,
        "section_id": post.section_id,
        "section_name": post.section.name if post.section else "",
        "user_id": post.user_id,
        "author_nickname": author_profile.nickname if author_profile else "社区用户",
        "author_auth_level": author_profile.auth_level if author_profile else 0,
        "title": post.title,
        "summary": summary,
        "post_type": post.post_type,
        "status": post.status,
        "view_count": post.view_count,
        "like_count": post.like_count,
        "comment_count": post.comment_count,
        "is_elite": post.is_elite,
        "created_at": post.created_at,
        "tags": [tag_to_read(tag) for tag in _post_tags(post)],
    }


def post_to_detail(post: Post) -> dict:
    data = post_to_item(post)
    data.update({"content": post.content, "updated_at": post.updated_at})
    return data


def list_sections(db: Session) -> list[Section]:
    return (
        db.execute(
            select(Section)
            .where(Section.is_active == 1)
            .order_by(desc(Section.sort_order), Section.id)
        )
        .scalars()
        .all()
    )


def get_section(db: Session, section_id: int) -> Section:
    section = db.get(Section, section_id)
    if section is None or section.is_active != 1:
        raise ResourceNotFoundError("板块不存在")
    return section


def create_section(db: Session, payload: SectionCreate) -> Section:
    section = Section(**payload.model_dump())
    db.add(section)
    db.commit()
    db.refresh(section)
    return section


def update_section(db: Session, section_id: int, payload: SectionUpdate) -> Section:
    section = db.get(Section, section_id)
    if section is None:
        raise ResourceNotFoundError("Section not found")
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        if value is not None:
            setattr(section, field, value)
    db.commit()
    db.refresh(section)
    return section


def delete_section(db: Session, section_id: int) -> Section:
    section = db.get(Section, section_id)
    if section is None:
        raise ResourceNotFoundError("Section not found")
    section.is_active = 0
    db.commit()
    db.refresh(section)
    return section


def _base_post_query():
    return select(Post).options(
        joinedload(Post.section),
        joinedload(Post.author).joinedload(User.profile),
        joinedload(Post.tags).joinedload(PostTag.tag),
    )


def list_posts(
    db: Session,
    section_id: Optional[int] = None,
    keyword: Optional[str] = None,
    tag_id: Optional[int] = None,
    is_elite: Optional[int] = None,
    sort: str = "latest",
    status: str = PUBLISHED_STATUS,
    page: int = 1,
    size: int = 10,
) -> tuple[list[Post], int]:
    filters = [Post.status == status]
    if section_id is not None:
        filters.append(Post.section_id == section_id)
    if keyword:
        like_keyword = f"%{keyword}%"
        filters.append(or_(Post.title.like(like_keyword), Post.content.like(like_keyword)))
    if is_elite is not None:
        filters.append(Post.is_elite == is_elite)

    count_query = db.query(Post).filter(and_(*filters))
    query = _base_post_query().where(and_(*filters))
    if tag_id is not None:
        count_query = count_query.join(PostTag, PostTag.post_id == Post.id).filter(PostTag.tag_id == tag_id)
        query = query.join(PostTag, PostTag.post_id == Post.id).where(PostTag.tag_id == tag_id)

    total = count_query.count()
    hot_score = Post.view_count + Post.like_count * 3 + Post.comment_count * 5
    order_by = (desc(hot_score), desc(Post.created_at)) if sort == "hot" else (desc(Post.created_at),)
    posts = (
        db.execute(
            query
            .order_by(*order_by)
            .offset((page - 1) * size)
            .limit(size)
        )
        .unique()
        .scalars()
        .all()
    )
    return posts, total


def get_post(db: Session, post_id: int, increase_view: bool = True) -> Post:
    post = (
        db.execute(_base_post_query().where(Post.id == post_id, Post.status != DELETED_STATUS))
        .unique()
        .scalar_one_or_none()
    )
    if post is None:
        raise ResourceNotFoundError("帖子不存在")
    if increase_view:
        post.view_count += 1
        db.commit()
        db.refresh(post)
    return post


def _sync_post_tags(db: Session, post: Post, tag_ids: list[int]) -> None:
    db.query(PostTag).filter(PostTag.post_id == post.id).delete()
    if not tag_ids:
        return
    tags = db.execute(select(Tag).where(Tag.id.in_(tag_ids))).scalars().all()
    for tag in tags:
        db.add(PostTag(post_id=post.id, tag_id=tag.id))


def _award_post_points(db: Session, user_id: int) -> None:
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if profile is None:
        return
    if hasattr(profile, "post_count"):
        profile.post_count += 1
    if hasattr(profile, "points"):
        profile.points += 5
        profile.level = max(1, profile.points // 100 + 1)
        if hasattr(profile, "badge_title"):
            profile.badge_title = "Active Member" if profile.points >= 100 else profile.badge_title


def _collect_audit_reasons(db: Session, post: Post) -> list[str]:
    text = f"{post.title}\n{post.content}".lower()
    reasons: list[str] = []
    words = db.query(SensitiveWord).filter(SensitiveWord.enabled.is_(True)).all()
    for word in words:
        if word.keyword and word.keyword.lower() in text:
            reasons.append(f"sensitive word: {word.keyword}")

    duplicate = (
        db.query(Post.id)
        .filter(
            Post.id != post.id,
            Post.user_id == post.user_id,
            Post.title == post.title,
            Post.status != DELETED_STATUS,
        )
        .first()
    )
    if duplicate:
        reasons.append("duplicate title by same user")
    return reasons


def _enqueue_post_audit(db: Session, post: Post, reasons: list[str]) -> None:
    if not reasons:
        return
    author = db.get(User, post.user_id)
    profile = author.profile if author and author.profile else None
    db.add(
        AuditQueueItem(
            content_type="post",
            title=post.title,
            author_name=profile.nickname if profile else f"user-{post.user_id}",
            reason="; ".join(reasons)[:255],
            risk_level="high" if any(reason.startswith("sensitive") for reason in reasons) else "medium",
            status="pending",
        )
    )


def create_post(db: Session, payload: PostCreate, user_id: int, post_type: Optional[int] = None) -> Post:
    get_section(db, payload.section_id)
    resolved_post_type = post_type if post_type is not None else payload.post_type
    post = Post(
        section_id=payload.section_id,
        user_id=user_id,
        title=payload.title,
        post_type=resolved_post_type,
        content=payload.content,
        status=PUBLISHED_STATUS,
    )
    db.add(post)
    db.flush()
    _sync_post_tags(db, post, payload.tag_ids)
    _award_post_points(db, user_id)
    reasons = _collect_audit_reasons(db, post)
    if reasons:
        post.status = "PENDING"
        _enqueue_post_audit(db, post, reasons)
    db.commit()
    return get_post(db, post.id, increase_view=False)


def update_post(db: Session, post_id: int, payload: PostUpdate) -> Post:
    post = get_post(db, post_id, increase_view=False)
    data = payload.model_dump(exclude_unset=True)
    tag_ids = data.pop("tag_ids", None)
    if "section_id" in data and data["section_id"] is not None:
        get_section(db, data["section_id"])
    for field, value in data.items():
        if value is not None:
            setattr(post, field, value)
    if tag_ids is not None:
        _sync_post_tags(db, post, tag_ids)
    db.commit()
    return get_post(db, post.id, increase_view=False)


def delete_post(db: Session, post_id: int) -> Post:
    post = get_post(db, post_id, increase_view=False)
    post.status = DELETED_STATUS
    db.commit()
    db.refresh(post)
    return post


def list_tags(db: Session, tag_type: str | None = None) -> list[Tag]:
    query = select(Tag).order_by(Tag.tag_type, Tag.name)
    if tag_type:
        query = query.where(Tag.tag_type == tag_type)
    return db.execute(query).scalars().all()


def create_tag(db: Session, payload: TagCreate) -> Tag:
    tag = Tag(**payload.model_dump())
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def update_tag(db: Session, tag_id: int, payload: TagUpdate) -> Tag:
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise ResourceNotFoundError("Tag not found")
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        if value is not None:
            setattr(tag, field, value)
    db.commit()
    db.refresh(tag)
    return tag


def delete_tag(db: Session, tag_id: int) -> dict:
    tag = db.get(Tag, tag_id)
    if tag is None:
        raise ResourceNotFoundError("Tag not found")
    db.query(PostTag).filter(PostTag.tag_id == tag_id).delete()
    db.delete(tag)
    db.commit()
    return {"id": tag_id}


def search_posts(db: Session, keyword: str, page: int = 1, size: int = 10) -> tuple[list[Post], int]:
    return list_posts(db, keyword=keyword, page=page, size=size)


def search_suggestions(db: Session, keyword: str, limit: int = 8) -> list[dict]:
    like_keyword = f"%{keyword}%"
    suggestions: list[dict] = []
    tags = db.query(Tag).filter(Tag.name.like(like_keyword)).order_by(Tag.name).limit(limit).all()
    for tag in tags:
        suggestions.append({"type": tag.tag_type.lower(), "label": tag.name, "value": tag.name})

    remaining = max(0, limit - len(suggestions))
    if remaining:
        users = (
            db.query(UserProfile)
            .filter(UserProfile.nickname.like(like_keyword))
            .order_by(UserProfile.influence_score.desc())
            .limit(remaining)
            .all()
        )
        for profile in users:
            suggestions.append({"type": "user", "label": profile.nickname, "value": str(profile.user_id)})

    remaining = max(0, limit - len(suggestions))
    if remaining:
        posts = (
            db.query(Post)
            .filter(Post.status == PUBLISHED_STATUS, Post.title.like(like_keyword))
            .order_by(desc(Post.created_at))
            .limit(remaining)
            .all()
        )
        for post in posts:
            suggestions.append({"type": "post", "label": post.title, "value": str(post.id)})
    return suggestions


def list_hot_posts(db: Session, limit: int = 10) -> list[Post]:
    score = Post.view_count + Post.like_count * 3 + Post.comment_count * 5
    return (
        db.execute(
            _base_post_query()
            .where(Post.status == PUBLISHED_STATUS)
            .order_by(desc(score), desc(Post.created_at))
            .limit(limit)
        )
        .unique()
        .scalars()
        .all()
    )


def list_hot_topics(db: Session, period: str = "daily", limit: int = 10) -> list[dict]:
    since = datetime.utcnow() - (timedelta(days=7) if period == "weekly" else timedelta(days=1))
    hot_score = func.coalesce(func.sum(Post.view_count + Post.like_count * 3 + Post.comment_count * 5), 0).label("hot_score")
    post_count = func.count(PostTag.post_id).label("post_count")
    rows = (
        db.query(
            Tag.id,
            Tag.name,
            Tag.tag_type,
            post_count,
            hot_score,
        )
        .join(PostTag, PostTag.tag_id == Tag.id)
        .join(Post, Post.id == PostTag.post_id)
        .filter(Post.status == PUBLISHED_STATUS, Post.created_at >= since)
        .group_by(Tag.id, Tag.name, Tag.tag_type)
        .order_by(desc(hot_score), desc(post_count))
        .limit(limit)
        .all()
    )
    return [
        {
            "id": row.id,
            "name": row.name,
            "tagType": row.tag_type,
            "postCount": row.post_count,
            "hotScore": int(row.hot_score or 0),
        }
        for row in rows
    ]


def attachment_to_read(attachment: Attachment) -> dict:
    return {
        "id": attachment.id,
        "postId": attachment.post_id,
        "fileUrl": attachment.file_url,
        "fileType": attachment.file_type,
        "createdAt": attachment.created_at,
    }


def add_attachment(db: Session, post_id: int, payload: AttachmentCreate, user_id: int) -> Attachment:
    post = get_post(db, post_id, increase_view=False)
    if post.user_id != user_id:
        raise ResourceNotFoundError("Post not found")
    data = payload.model_dump(by_alias=False)
    attachment = Attachment(post_id=post_id, **data)
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment


def list_attachments(db: Session, post_id: int) -> list[Attachment]:
    get_post(db, post_id, increase_view=False)
    return db.query(Attachment).filter(Attachment.post_id == post_id).order_by(Attachment.created_at.asc()).all()


def poll_option_to_read(option: PollOption) -> dict:
    return {
        "id": option.id,
        "postId": option.post_id,
        "optionText": option.option_text,
        "voteCount": option.vote_count,
    }


def add_poll_option(db: Session, post_id: int, payload: PollOptionCreate, user_id: int) -> PollOption:
    post = get_post(db, post_id, increase_view=False)
    if post.user_id != user_id:
        raise ResourceNotFoundError("Post not found")
    post.post_type = 3
    data = payload.model_dump(by_alias=False)
    option = PollOption(post_id=post_id, **data)
    db.add(option)
    db.commit()
    db.refresh(option)
    return option


def list_poll_options(db: Session, post_id: int) -> list[PollOption]:
    get_post(db, post_id, increase_view=False)
    return db.query(PollOption).filter(PollOption.post_id == post_id).order_by(PollOption.id.asc()).all()


def vote_poll_option(db: Session, option_id: int, user_id: int) -> dict:
    option = db.query(PollOption).filter(PollOption.id == option_id).first()
    if option is None:
        raise ResourceNotFoundError("Poll option not found")
    existing = db.get(PollVote, {"post_id": option.post_id, "user_id": user_id})
    if existing:
        previous = db.query(PollOption).filter(PollOption.id == existing.option_id).first()
        if previous and previous.vote_count > 0:
            previous.vote_count -= 1
        existing.option_id = option.id
    else:
        db.add(PollVote(post_id=option.post_id, user_id=user_id, option_id=option.id))
    option.vote_count += 1
    db.commit()
    return {
        "postId": option.post_id,
        "selectedOptionId": option.id,
        "options": [poll_option_to_read(item) for item in list_poll_options(db, option.post_id)],
    }
