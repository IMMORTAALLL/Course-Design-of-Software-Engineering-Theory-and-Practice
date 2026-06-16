from sqlalchemy import and_, desc, or_, select
from sqlalchemy.orm import Session, joinedload

from app.common.exceptions import ResourceNotFoundError
from app.modules.auth.models import User
from app.modules.forum.models import Post, PostTag, Section, Tag
from app.modules.forum.schemas import PostCreate, PostUpdate, SectionCreate, TagCreate

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


def _base_post_query():
    return select(Post).options(
        joinedload(Post.section),
        joinedload(Post.author).joinedload(User.profile),
        joinedload(Post.tags).joinedload(PostTag.tag),
    )


def list_posts(
    db: Session,
    section_id: int | None = None,
    keyword: str | None = None,
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

    total = db.query(Post).filter(and_(*filters)).count()
    posts = (
        db.execute(
            _base_post_query()
            .where(and_(*filters))
            .order_by(desc(Post.created_at))
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


def create_post(db: Session, payload: PostCreate, user_id: int, post_type: int = 1) -> Post:
    get_section(db, payload.section_id)
    post = Post(
        section_id=payload.section_id,
        user_id=user_id,
        title=payload.title,
        post_type=post_type,
        content=payload.content,
        status=PUBLISHED_STATUS,
    )
    db.add(post)
    db.flush()
    _sync_post_tags(db, post, payload.tag_ids)
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


def search_posts(db: Session, keyword: str, page: int = 1, size: int = 10) -> tuple[list[Post], int]:
    return list_posts(db, keyword=keyword, page=page, size=size)


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
