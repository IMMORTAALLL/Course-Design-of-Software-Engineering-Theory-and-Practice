from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.response import paginated, success
from app.database import get_db
from app.modules.forum import crud
from app.modules.forum.schemas import (
    PostCreate,
    PostUpdate,
    SectionCreate,
    TagCreate,
)

router = APIRouter(prefix="/api", tags=["forum"])


@router.get("/sections")
def list_sections(db: Session = Depends(get_db)):
    return success([crud.section_to_read(section) for section in crud.list_sections(db)])


@router.post("/sections")
def create_section(payload: SectionCreate, db: Session = Depends(get_db)):
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
def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    post = crud.create_post(db, payload, user_id=1)
    return success(crud.post_to_detail(post), "帖子发布成功")


@router.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.get_post(db, post_id)
    return success(crud.post_to_detail(post))


@router.put("/posts/{post_id}")
def update_post(post_id: int, payload: PostUpdate, db: Session = Depends(get_db)):
    post = crud.update_post(db, post_id, payload)
    return success(crud.post_to_detail(post), "帖子更新成功")


@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.delete_post(db, post_id)
    return success({"id": post.id, "status": post.status}, "帖子已删除")


@router.get("/tags")
def list_tags(tag_type: str | None = None, db: Session = Depends(get_db)):
    return success([crud.tag_to_read(tag) for tag in crud.list_tags(db, tag_type=tag_type)])


@router.post("/tags")
def create_tag(payload: TagCreate, db: Session = Depends(get_db)):
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
