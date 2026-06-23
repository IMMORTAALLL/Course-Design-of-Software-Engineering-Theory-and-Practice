"""End-to-end smoke checks for the FastAPI backend.

The script uses an isolated SQLite database in the system temp directory, so it
does not touch the repository's local demo database. Run it with a Python
environment that has backend/requirements.txt installed.
"""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"
TEMP_DB = Path(tempfile.gettempdir()) / "stock_forum_backend_smoke.db"


def configure_environment() -> None:
    if TEMP_DB.exists():
        TEMP_DB.unlink()
    os.environ["DATABASE_URL"] = "sqlite:///" + TEMP_DB.as_posix()
    os.environ["JWT_SECRET_KEY"] = "smoke-test-secret"
    os.environ["DEBUG"] = "false"
    sys.path.insert(0, str(BACKEND_DIR))
    os.chdir(BACKEND_DIR)


configure_environment()

try:
    from fastapi.testclient import TestClient

    from app.database import SessionLocal, engine
    from app.main import app
    from app.modules.auth.models import Role, User, UserProfile, UserRole
    from app.modules.forum.models import Section, Tag
    from app.security.password import hash_password
except ImportError as exc:
    raise SystemExit(
        "Missing backend dependencies. Install backend/requirements.txt in the "
        f"current Python environment first. Import error: {exc}"
    ) from exc


client = TestClient(app)
failures: list[tuple[str, Any]] = []


def body(response) -> dict[str, Any]:
    try:
        return response.json()
    except Exception as exc:  # pragma: no cover - diagnostic path
        return {"parse_error": str(exc), "text": response.text[:300]}


def expect(name: str, condition: bool, detail: Any = "") -> None:
    if condition:
        print(f"PASS {name}")
        return
    print(f"FAIL {name}: {detail}")
    failures.append((name, detail))


def headers(token: str | None = None) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"} if token else {}


def seed_minimal_data() -> None:
    with SessionLocal() as db:
        for role_name in ["USER", "ADMIN"]:
            if db.query(Role).filter(Role.name == role_name).first() is None:
                db.add(Role(name=role_name, description=role_name))
        db.flush()

        if db.query(Section).first() is None:
            db.add(Section(name="A-share Market", description="Market discussion", sort_order=10, is_active=1))
        if db.query(Tag).first() is None:
            db.add(Tag(name="Value Investing", tag_type="TOPIC"))

        admin_role = db.query(Role).filter(Role.name == "ADMIN").first()
        if db.query(User).filter(User.email == "admin@example.com").first() is None:
            admin = User(email="admin@example.com", password_hash=hash_password("Admin123456"))
            db.add(admin)
            db.flush()
            db.add(UserProfile(user_id=admin.id, nickname="Admin", auth_level=2))
            db.add(UserRole(user_id=admin.id, role_id=admin_role.id))
        db.commit()


def run_smoke_checks() -> None:
    seed_minimal_data()

    health = client.get("/api/health")
    expect("health", health.status_code == 200 and body(health).get("code") == 0, body(health))

    sections_body = body(client.get("/api/sections"))
    expect("list sections", sections_body.get("code") == 0 and len(sections_body.get("data", [])) >= 1, sections_body)
    section_id = sections_body["data"][0]["id"]

    tags_body = body(client.get("/api/tags"))
    expect("list tags", tags_body.get("code") == 0 and len(tags_body.get("data", [])) >= 1, tags_body)
    tag_id = tags_body["data"][0]["id"]

    register_payload = {
        "accountType": "email",
        "email": "user1@example.com",
        "password": "User123456",
        "nickname": "SmokeUser",
        "verifyCode": "123456",
    }
    expect("register", body(client.post("/api/auth/register", json=register_payload)).get("code") == 0)

    login_body = body(client.post("/api/auth/login", json={"account": "user1@example.com", "password": "User123456"}))
    expect("login", login_body.get("code") == 0 and bool(login_body.get("data", {}).get("token")), login_body)
    user_token = login_body["data"]["token"]

    admin_login_body = body(
        client.post("/api/auth/login", json={"account": "admin@example.com", "password": "Admin123456"})
    )
    expect(
        "admin login",
        admin_login_body.get("code") == 0 and bool(admin_login_body.get("data", {}).get("token")),
        admin_login_body,
    )
    admin_token = admin_login_body["data"]["token"]
    admin_me_body = body(client.get("/api/users/me", headers=headers(admin_token)))
    expect("admin current user", admin_me_body.get("code") == 0 and admin_me_body.get("data", {}).get("role") == "ADMIN", admin_me_body)
    admin_id = admin_me_body["data"]["id"]

    me_body = body(client.get("/api/users/me", headers=headers(user_token)))
    expect("current user", me_body.get("code") == 0 and me_body.get("data", {}).get("email") == "user1@example.com", me_body)

    update_profile_body = body(
        client.put(
            "/api/users/me/profile",
            json={
                "experienceTags": ["ETF", "A-share"],
                "interestMarkets": ["CSI300", "HK"],
                "privacyLevel": 1,
            },
            headers=headers(user_token),
        )
    )
    expect("update profile extension", update_profile_body.get("code") == 0, update_profile_body)

    post_body = body(
        client.post(
            "/api/posts",
            json={
                "section_id": section_id,
                "title": "Smoke test post",
                "content": "Smoke test content",
                "tag_ids": [tag_id],
            },
            headers=headers(user_token),
        )
    )
    expect("create post", post_body.get("code") == 0 and bool(post_body.get("data", {}).get("id")), post_body)
    post_id = post_body["data"]["id"]

    detail_body = body(client.get(f"/api/posts/{post_id}"))
    expect("post detail", detail_body.get("code") == 0 and detail_body.get("data", {}).get("id") == post_id, detail_body)

    attachment_body = body(
        client.post(
            f"/api/posts/{post_id}/attachments",
            json={"fileUrl": "https://example.com/chart.png", "fileType": "image"},
            headers=headers(user_token),
        )
    )
    expect("add attachment", attachment_body.get("code") == 0 and attachment_body.get("data", {}).get("fileUrl"), attachment_body)

    poll_option_body = body(
        client.post(
            f"/api/posts/{post_id}/poll-options",
            json={"optionText": "Bullish"},
            headers=headers(user_token),
        )
    )
    expect("add poll option", poll_option_body.get("code") == 0 and poll_option_body.get("data", {}).get("id"), poll_option_body)
    poll_option_id = poll_option_body["data"]["id"]

    vote_body = body(client.post(f"/api/poll-options/{poll_option_id}/vote", headers=headers(user_token)))
    expect("vote poll option", vote_body.get("code") == 0 and vote_body.get("data", {}).get("selectedOptionId") == poll_option_id, vote_body)

    suggestions_body = body(client.get("/api/search/suggestions", params={"keyword": "Smoke"}))
    expect("search suggestions", suggestions_body.get("code") == 0 and len(suggestions_body.get("data", [])) >= 1, suggestions_body)

    hot_topics_body = body(client.get("/api/hot-topics", params={"period": "weekly"}))
    expect("hot topics", hot_topics_body.get("code") == 0 and isinstance(hot_topics_body.get("data"), list), hot_topics_body)

    comment_body = body(
        client.post(f"/api/posts/{post_id}/comments", json={"content": "Smoke comment"}, headers=headers(user_token))
    )
    expect("create comment", comment_body.get("code") == 0 and bool(comment_body.get("data", {}).get("id")), comment_body)
    comment_id = comment_body["data"]["id"]

    reply_body = body(
        client.post(f"/api/comments/{comment_id}/replies", json={"content": "Smoke reply"}, headers=headers(user_token))
    )
    expect("create reply", reply_body.get("code") == 0, reply_body)

    like_body = body(client.post(f"/api/posts/{post_id}/like", headers=headers(user_token)))
    expect("toggle post like", like_body.get("code") == 0 and "active" in like_body.get("data", {}), like_body)

    favorite_body = body(client.post(f"/api/posts/{post_id}/favorite", headers=headers(user_token)))
    expect("toggle favorite", favorite_body.get("code") == 0 and "active" in favorite_body.get("data", {}), favorite_body)

    star_body = body(client.put(f"/api/users/{admin_id}/follow/star", params={"starred": True}, headers=headers(user_token)))
    expect("star follow", star_body.get("code") == 0 and star_body.get("data", {}).get("starred") is True, star_body)

    message_body = body(
        client.post(f"/api/users/{admin_id}/messages", json={"content": "Smoke private message"}, headers=headers(user_token))
    )
    expect("send private message", message_body.get("code") == 0 and message_body.get("data", {}).get("id"), message_body)

    status_body = body(client.get(f"/api/posts/{post_id}/interaction-status", headers=headers(user_token)))
    expect("interaction status", status_body.get("code") == 0 and status_body.get("data", {}).get("liked") is True, status_body)

    report_body = body(
        client.post(f"/api/posts/{post_id}/report", json={"reason": "Smoke report"}, headers=headers(user_token))
    )
    expect("report post", report_body.get("code") == 0 and bool(report_body.get("data", {}).get("id")), report_body)

    group_body = body(
        client.post(
            "/api/groups",
            json={"name": "Smoke Group", "description": "Smoke group", "permission": 1},
            headers=headers(user_token),
        )
    )
    expect("create group", group_body.get("code") == 0 and group_body.get("data", {}).get("joined") is True, group_body)
    group_id = group_body["data"]["id"]

    get_group_body = body(client.get(f"/api/groups/{group_id}", headers=headers(user_token)))
    expect("get group", get_group_body.get("code") == 0 and get_group_body.get("data", {}).get("id") == group_id, get_group_body)

    group_post_body = body(
        client.post(f"/api/groups/{group_id}/posts", json={"content": "Smoke group post"}, headers=headers(user_token))
    )
    expect("create group post", group_post_body.get("code") == 0 and group_post_body.get("data", {}).get("id"), group_post_body)

    group_resource_body = body(
        client.post(
            f"/api/groups/{group_id}/resources",
            json={"title": "Smoke resource", "resourceUrl": "https://example.com/report.pdf"},
            headers=headers(user_token),
        )
    )
    expect("create group resource", group_resource_body.get("code") == 0 and group_resource_body.get("data", {}).get("id"), group_resource_body)

    admin_overview_body = body(client.get("/api/admin/overview", headers=headers(admin_token)))
    expect(
        "admin overview",
        admin_overview_body.get("code") == 0 and "pending_audits" in admin_overview_body.get("data", {}),
        admin_overview_body,
    )

    admin_forbidden_body = body(client.get("/api/admin/overview", headers=headers(user_token)))
    expect("admin forbidden", admin_forbidden_body.get("code") == 40301, admin_forbidden_body)

    reports_body = body(client.get("/api/admin/reports", headers=headers(admin_token)))
    expect("admin reports", reports_body.get("code") == 0 and len(reports_body.get("data", [])) >= 1, reports_body)

    openapi_body = body(client.get("/openapi.json"))
    expect("openapi generated", "/api/posts" in openapi_body.get("paths", {}), "missing /api/posts")


def main() -> int:
    try:
        run_smoke_checks()
        if failures:
            print(f"\nSMOKE TEST FAILURES: {len(failures)}")
            for name, detail in failures:
                print(f"- {name}: {detail}")
            return 1
        print("\nSMOKE TESTS PASSED")
        return 0
    finally:
        engine.dispose()
        if TEMP_DB.exists():
            TEMP_DB.unlink()


if __name__ == "__main__":
    raise SystemExit(main())
