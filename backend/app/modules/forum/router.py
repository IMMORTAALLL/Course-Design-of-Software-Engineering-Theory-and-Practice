from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.deps import get_current_user, require_admin
from app.common.exceptions import ForbiddenError
from app.common.response import paginated, success
from app.database import get_db
from app.modules.auth.models import User
from app.modules.forum import crud
from app.modules.forum.schemas import (
    PostCreate,
    PostUpdate,
    SectionCreate,
    TagCreate,
)

router = APIRouter(prefix="/api", tags=["forum"])


def _can_manage_post(current_user: User, post_user_id: int) -> bool:
    role_names = {role.name for role in current_user.roles}
    return current_user.id == post_user_id or "ADMIN" in role_names


@router.get("/sections")
def list_sections(db: Session = Depends(get_db)):
    return success([crud.section_to_read(section) for section in crud.list_sections(db)])


@router.post("/sections")
def create_section(
    payload: SectionCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    section = crud.create_section(db, payload)
    return success(crud.section_to_read(section), "板块创建成功")


@router.post("/admin/sections")
def admin_create_section(
    payload: SectionCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    section = crud.create_section(db, payload)
    return success(crud.section_to_read(section), "板块创建成功")


@router.get("/sections/{section_id}")
def get_section(section_id: int, db: Session = Depends(get_db)):
    return success(crud.section_to_read(crud.get_section(db, section_id)))


@router.get("/posts/hot")
def list_hot_posts(limit: int = Query(10, ge=1, le=50), db: Session = Depends(get_db)):
    posts = [crud.post_to_item(post) for post in crud.list_hot_posts(db, limit)]
    return success(posts)


@router.get("/posts")
def list_posts(
    section_id: int | None = None,
    keyword: str | None = None,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    posts, total = crud.list_posts(db, section_id=section_id, keyword=keyword, page=page, size=size)
    return paginated([crud.post_to_item(post) for post in posts], page, size, total)


@router.post("/posts")
def create_post(
    payload: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = crud.create_post(db, payload, user_id=current_user.id)
    return success(crud.post_to_detail(post), "帖子发布成功")


@router.post("/posts/analysis")
def create_analysis_post(
    payload: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    auth_level = current_user.profile.auth_level if current_user.profile else 0
    if auth_level < 2:
        raise ForbiddenError("需要专业认证后才能发布长文分析")
    post = crud.create_post(db, payload, user_id=current_user.id, post_type=2)
    return success(crud.post_to_detail(post), "长文分析发布成功")


@router.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    return success(crud.post_to_detail(post))


@router.put("/posts/{post_id}")
def update_post(
    post_id: int,
    payload: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = crud.get_post(db, post_id, increase_view=False)
    if not _can_manage_post(current_user, existing.user_id):
        raise ForbiddenError("只能编辑自己的帖子")
    post = crud.update_post(db, post_id, payload)
    return success(crud.post_to_detail(post), "帖子更新成功")


@router.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = crud.get_post(db, post_id, increase_view=False)
    if not _can_manage_post(current_user, existing.user_id):
        raise ForbiddenError("只能删除自己的帖子")
    post = crud.delete_post(db, post_id)
    return success({"id": post.id, "status": post.status}, "帖子已删除")


@router.get("/tags")
def list_tags(tag_type: str | None = None, db: Session = Depends(get_db)):
    return success([crud.tag_to_read(tag) for tag in crud.list_tags(db, tag_type=tag_type)])


@router.post("/tags")
def create_tag(
    payload: TagCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    tag = crud.create_tag(db, payload)
    return success(crud.tag_to_read(tag), "标签创建成功")


@router.post("/admin/tags")
def admin_create_tag(
    payload: TagCreate,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    tag = crud.create_tag(db, payload)
    return success(crud.tag_to_read(tag), "标签创建成功")


@router.get("/search/posts")
def search_posts(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    posts, total = crud.search_posts(db, keyword=keyword, page=page, size=size)
    return paginated([crud.post_to_item(post) for post in posts], page, size, total)
