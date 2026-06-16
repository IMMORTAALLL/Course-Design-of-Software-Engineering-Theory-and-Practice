from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.modules.admin.models import AuditQueueItem, ReportItem, SensitiveWord, UserModerationRecord
from app.modules.auth.models import Role, User, UserProfile, UserRole
from app.modules.forum.models import Post, PostTag, Section, Tag
from app.modules.interaction.models import (
    Comment,
    Group,
    GroupJoinRequest,
    GroupMember,
    Notification,
    UserAction,
    UserFollow,
)
from app.security.password import hash_password


def _ensure_role(db: Session, name: str, description: str) -> Role:
    role = db.query(Role).filter(Role.name == name).first()
    if role is None:
        role = Role(name=name, description=description)
        db.add(role)
        db.flush()
    return role


def _ensure_user(
    db: Session,
    *,
    phone: str,
    email: str,
    nickname: str,
    role: Role,
    auth_level: int = 0,
    risk_preference: int | None = None,
    influence_score: int = 0,
    bio: str | None = None,
) -> User:
    user = db.query(User).filter(or_(User.email == email, User.phone == phone)).first()
    if user is None:
        user = User(phone=phone, email=email, password_hash=hash_password("Admin123456"), status=0)
        db.add(user)
        db.flush()
    else:
        if user.phone is None:
            user.phone = phone
        if user.email is None:
            user.email = email
    if user.profile is None:
        db.add(
            UserProfile(
                user_id=user.id,
                nickname=nickname,
                bio=bio,
                auth_level=auth_level,
                risk_preference=risk_preference,
                influence_score=influence_score,
            )
        )
    else:
        user.profile.nickname = user.profile.nickname or nickname
        user.profile.bio = user.profile.bio or bio
        user.profile.auth_level = max(user.profile.auth_level, auth_level)
        user.profile.risk_preference = user.profile.risk_preference or risk_preference
        user.profile.influence_score = max(user.profile.influence_score, influence_score)
    if db.get(UserRole, {"user_id": user.id, "role_id": role.id}) is None:
        db.add(UserRole(user_id=user.id, role_id=role.id))
    db.flush()
    return user


def _ensure_section(db: Session, name: str, description: str, sort_order: int) -> Section:
    section = db.query(Section).filter(Section.name == name).first()
    if section is None:
        section = Section(name=name, description=description, sort_order=sort_order, is_active=1)
        db.add(section)
        db.flush()
    return section


def _ensure_tag(db: Session, name: str, tag_type: str) -> Tag:
    tag = db.query(Tag).filter(Tag.name == name).first()
    if tag is None:
        tag = Tag(name=name, tag_type=tag_type)
        db.add(tag)
        db.flush()
    return tag


def _ensure_post(
    db: Session,
    *,
    section: Section,
    author: User,
    title: str,
    content: str,
    tags: list[Tag],
    view_count: int,
    like_count: int,
    comment_count: int,
    is_elite: int = 0,
    post_type: int = 1,
) -> Post:
    post = db.query(Post).filter(Post.title == title).first()
    if post is None:
        post = Post(
            section_id=section.id,
            user_id=author.id,
            title=title,
            post_type=post_type,
            content=content,
            status="PUBLISHED",
            view_count=view_count,
            like_count=like_count,
            comment_count=comment_count,
            is_elite=is_elite,
        )
        db.add(post)
        db.flush()
    for tag in tags:
        if db.get(PostTag, {"post_id": post.id, "tag_id": tag.id}) is None:
            db.add(PostTag(post_id=post.id, tag_id=tag.id))
    return post


def _ensure_demo_content(db: Session) -> None:
    user_role = _ensure_role(db, "USER", "普通用户")
    verified_role = _ensure_role(db, "VERIFIED", "认证用户")
    admin_role = _ensure_role(db, "ADMIN", "管理员")

    admin = _ensure_user(
        db,
        phone="13800000001",
        email="admin@stockforum.com",
        nickname="系统管理员",
        role=admin_role,
        auth_level=2,
        risk_preference=2,
        influence_score=120,
        bio="负责社区内容审核、用户管理和运营数据观察。",
    )
    value_user = _ensure_user(
        db,
        phone="13800000002",
        email="value@stockforum.com",
        nickname="价值观察员",
        role=user_role,
        auth_level=1,
        risk_preference=2,
        influence_score=86,
        bio="关注长期主义、指数基金配置和企业基本面研究。",
    )
    quant_user = _ensure_user(
        db,
        phone="13800000003",
        email="quant@stockforum.com",
        nickname="量化研究员",
        role=verified_role,
        auth_level=2,
        risk_preference=3,
        influence_score=128,
        bio="分享量化策略、因子研究和回测经验。",
    )

    a_share = _ensure_section(db, "A股市场", "围绕A股行情、个股研究和交易经验展开讨论。", 100)
    fund = _ensure_section(db, "基金专区", "交流公募基金、指数基金和基金定投策略。", 80)
    quant = _ensure_section(db, "量化交易", "讨论量化模型、因子策略和程序化交易实践。", 70)
    macro = _ensure_section(db, "宏观策略", "研讨宏观经济、资产配置和风险提示。", 60)
    help_section = _ensure_section(db, "问答求助", "新手提问、投资工具使用和经验答疑。", 50)

    maotai = _ensure_tag(db, "贵州茅台", "STOCK")
    csi300 = _ensure_tag(db, "沪深300", "FUND")
    new_energy = _ensure_tag(db, "新能源", "TOPIC")
    quant_tag = _ensure_tag(db, "量化策略", "TOPIC")
    risk_tag = _ensure_tag(db, "风险提示", "TOPIC")

    post1 = _ensure_post(
        db,
        section=a_share,
        author=value_user,
        title="A股市场震荡时如何看待白酒板块？",
        content="最近白酒板块波动较大，可以从估值、业绩韧性和资金情绪三个角度观察。本文仅用于讨论，不构成投资建议。",
        tags=[maotai, risk_tag],
        view_count=128,
        like_count=18,
        comment_count=2,
        is_elite=1,
    )
    post2 = _ensure_post(
        db,
        section=fund,
        author=value_user,
        title="指数基金定投适合新手吗？",
        content="定投更适合长期资金和纪律性较强的投资者，关键是控制仓位、理解波动，并设置合理的收益预期。",
        tags=[csi300],
        view_count=96,
        like_count=14,
        comment_count=1,
    )
    post3 = _ensure_post(
        db,
        section=quant,
        author=quant_user,
        title="一个简单的动量因子选股思路",
        content="用过去20日收益率作为动量因子可以形成基础策略，但还需要结合回撤、换手率和交易成本做稳健性检验。",
        tags=[quant_tag],
        view_count=76,
        like_count=11,
        comment_count=0,
        post_type=2,
    )
    _ensure_post(
        db,
        section=macro,
        author=admin,
        title="降息预期下的大类资产配置讨论",
        content="宏观环境变化会影响股票、债券和商品的相对吸引力，需要结合风险偏好和持有周期做配置。",
        tags=[new_energy, risk_tag],
        view_count=61,
        like_count=8,
        comment_count=0,
    )
    _ensure_post(
        db,
        section=help_section,
        author=value_user,
        title="新手如何理解风险测评结果？",
        content="风险测评不是收益承诺，而是帮助你判断自己能够承受的波动范围，再决定产品类型和仓位比例。",
        tags=[risk_tag],
        view_count=43,
        like_count=6,
        comment_count=0,
    )

    if db.query(Comment).filter(Comment.post_id == post1.id).first() is None:
        root = Comment(post_id=post1.id, user_id=quant_user.id, content="可以再叠加成交额和北向资金变化观察。", like_count=5)
        db.add(root)
        db.flush()
        db.add(Comment(post_id=post1.id, user_id=value_user.id, parent_id=root.id, content="赞同，短期波动还是要回到现金流和估值区间。", like_count=2))
    if db.query(Comment).filter(Comment.post_id == post2.id).first() is None:
        db.add(Comment(post_id=post2.id, user_id=quant_user.id, content="定投前最好先确认资金期限，备用金不要放进去。", like_count=4))

    for action in [
        (value_user.id, post1.id, 1, 1),
        (quant_user.id, post1.id, 1, 2),
        (admin.id, post3.id, 1, 1),
    ]:
        user_id, target_id, target_type, action_type = action
        exists = (
            db.query(UserAction)
            .filter(
                UserAction.user_id == user_id,
                UserAction.target_id == target_id,
                UserAction.target_type == target_type,
                UserAction.action_type == action_type,
            )
            .first()
        )
        if exists is None:
            db.add(UserAction(user_id=user_id, target_id=target_id, target_type=target_type, action_type=action_type))

    for follower, followed, starred in [(value_user, quant_user, 1), (quant_user, value_user, 0)]:
        if db.get(UserFollow, {"follower_id": follower.id, "followed_id": followed.id}) is None:
            db.add(UserFollow(follower_id=follower.id, followed_id=followed.id, is_starred=starred))

    groups = [
        (quant_user, "量化策略研究小组", "讨论因子、回测、风控和策略复盘。", 1, [value_user]),
        (value_user, "指数基金长期定投", "适合长期配置和新手基金投资交流。", 1, [quant_user]),
        (quant_user, "专业策略审核群", "需要审核后加入的策略交流小组。", 2, []),
    ]
    private_group: Group | None = None
    for creator, name, description, permission, members in groups:
        group = db.query(Group).filter(Group.name == name).first()
        if group is None:
            group = Group(creator_id=creator.id, name=name, description=description, permission=permission)
            db.add(group)
            db.flush()
        if db.get(GroupMember, {"group_id": group.id, "user_id": creator.id}) is None:
            db.add(GroupMember(group_id=group.id, user_id=creator.id))
        for member in members:
            if db.get(GroupMember, {"group_id": group.id, "user_id": member.id}) is None:
                db.add(GroupMember(group_id=group.id, user_id=member.id))
        if permission == 2:
            private_group = group
    if private_group and db.get(GroupJoinRequest, {"group_id": private_group.id, "user_id": value_user.id}) is None:
        db.add(GroupJoinRequest(group_id=private_group.id, user_id=value_user.id, status="pending"))

    if db.query(Notification).filter(Notification.user_id == value_user.id).first() is None:
        db.add_all(
            [
                Notification(
                    user_id=value_user.id,
                    title="评论收到回复",
                    content="量化研究员回复了你的讨论。",
                    notification_type="interaction",
                    target_type="post",
                    target_id=post1.id,
                ),
                Notification(
                    user_id=quant_user.id,
                    title="新增关注",
                    content="价值观察员关注了你。",
                    notification_type="interaction",
                    target_type="user",
                    target_id=value_user.id,
                ),
            ]
        )


def seed_admin_demo_data(db: Session) -> None:
    _ensure_demo_content(db)

    if db.query(AuditQueueItem).first() is None:
        db.add_all(
            [
                AuditQueueItem(
                    content_type="post",
                    title="推荐某股票明天必涨停",
                    author_name="短线猎手",
                    reason="违规荐股",
                    risk_level="high",
                    status="pending",
                ),
                AuditQueueItem(
                    content_type="comment",
                    title="保证收益，跟单联系我",
                    author_name="暴涨带队",
                    reason="广告引流",
                    risk_level="high",
                    status="pending",
                ),
                AuditQueueItem(
                    content_type="attachment",
                    title="基金收益分析表",
                    author_name="稳健定投者",
                    reason="附件待审核",
                    risk_level="medium",
                    status="reviewing",
                ),
            ]
        )

    if db.query(ReportItem).first() is None:
        db.add_all(
            [
                ReportItem(
                    target_type="post",
                    target_title="内部消息，今晚布局",
                    reporter_name="价值观察员",
                    reason="虚假荐股",
                    status="pending",
                ),
                ReportItem(
                    target_type="comment",
                    target_title="拉你进群带你赚钱",
                    reporter_name="理性投资人",
                    reason="广告引流",
                    status="pending",
                ),
            ]
        )

    if db.query(SensitiveWord).first() is None:
        db.add_all(
            [
                SensitiveWord(
                    keyword="稳赚不赔",
                    category="违规荐股",
                    risk_level="high",
                    action="manual_review",
                    enabled=True,
                    note="高风险承诺收益表述",
                ),
                SensitiveWord(
                    keyword="内部消息",
                    category="违规荐股",
                    risk_level="high",
                    action="manual_review",
                    enabled=True,
                    note="涉及未证实内幕信息",
                ),
                SensitiveWord(
                    keyword="带单",
                    category="广告引流",
                    risk_level="medium",
                    action="manual_review",
                    enabled=True,
                    note="常见引流词",
                ),
            ]
        )

    if db.query(UserModerationRecord).first() is None:
        db.add_all(
            [
                UserModerationRecord(
                    user_name="暴涨带队",
                    action="warning",
                    reason="多次发布广告引流评论",
                    status="active",
                ),
                UserModerationRecord(
                    user_name="内幕先知道",
                    action="mute",
                    reason="散布未证实内幕消息",
                    status="muted",
                ),
                UserModerationRecord(
                    user_name="稳赚俱乐部",
                    action="ban",
                    reason="反复发布违规荐股内容",
                    status="banned",
                ),
            ]
        )

    db.commit()
