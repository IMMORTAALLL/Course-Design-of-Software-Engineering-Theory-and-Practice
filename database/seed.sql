-- 智投社区初始化演示数据
-- 合并成员A用户权限模块、成员B论坛内容模块与成员D后台审核模块演示数据。

USE `forum_system_db`;

-- 初始化角色
INSERT INTO `roles` (`id`, `name`, `description`) VALUES
(1, 'USER', '普通用户'),
(2, 'VERIFIED', '认证用户'),
(3, 'MODERATOR', '版主'),
(4, 'ADMIN', '管理员')
ON DUPLICATE KEY UPDATE
    `name` = VALUES(`name`),
    `description` = VALUES(`description`);

-- 初始化管理员账号（密码: Admin123456）
INSERT INTO `users` (`id`, `phone`, `email`, `password_hash`, `status`) VALUES
(1, '13800000001', 'admin@stockforum.com', '$2b$12$LJ3a4PmYlMQ8M8GZmBZ5aOJXHf9wMq5Y3xKjF5vN0yL8VfKjzKXXi', 0)
ON DUPLICATE KEY UPDATE
    `phone` = VALUES(`phone`),
    `email` = VALUES(`email`),
    `password_hash` = VALUES(`password_hash`),
    `status` = VALUES(`status`);

INSERT INTO `user_profiles` (`user_id`, `nickname`, `auth_level`) VALUES
(1, '系统管理员', 2)
ON DUPLICATE KEY UPDATE
    `nickname` = VALUES(`nickname`),
    `auth_level` = VALUES(`auth_level`);

INSERT INTO `user_roles` (`user_id`, `role_id`) VALUES
(1, 4)
ON DUPLICATE KEY UPDATE
    `role_id` = VALUES(`role_id`);

-- 初始化普通演示用户（演示密码同管理员账号: Admin123456）
INSERT INTO `users` (`id`, `phone`, `email`, `password_hash`, `status`) VALUES
(2, '13800000002', 'value@stockforum.com', '$2b$12$LJ3a4PmYlMQ8M8GZmBZ5aOJXHf9wMq5Y3xKjF5vN0yL8VfKjzKXXi', 0),
(3, '13800000003', 'quant@stockforum.com', '$2b$12$LJ3a4PmYlMQ8M8GZmBZ5aOJXHf9wMq5Y3xKjF5vN0yL8VfKjzKXXi', 0)
ON DUPLICATE KEY UPDATE
    `phone` = VALUES(`phone`),
    `email` = VALUES(`email`),
    `status` = VALUES(`status`);

INSERT INTO `user_profiles` (`user_id`, `nickname`, `bio`, `auth_level`, `risk_preference`, `influence_score`) VALUES
(2, '价值观察员', '关注长期主义和指数基金配置。', 1, 2, 86),
(3, '量化研究员', '分享量化策略、因子研究和回测经验。', 2, 3, 128)
ON DUPLICATE KEY UPDATE
    `nickname` = VALUES(`nickname`),
    `bio` = VALUES(`bio`),
    `auth_level` = VALUES(`auth_level`),
    `risk_preference` = VALUES(`risk_preference`),
    `influence_score` = VALUES(`influence_score`);

INSERT INTO `user_roles` (`user_id`, `role_id`) VALUES
(2, 1),
(3, 2)
ON DUPLICATE KEY UPDATE
    `role_id` = VALUES(`role_id`);

-- 初始化板块
INSERT INTO `sections` (`id`, `name`, `description`, `sort_order`, `is_active`) VALUES
(1, 'A股市场', '围绕A股行情、个股研究和交易经验展开讨论。', 100, 1),
(2, '港股市场', '港股市场行情与个股讨论。', 90, 1),
(3, '美股市场', '美股市场行情与个股讨论。', 80, 1),
(4, '基金专区', '交流公募基金、指数基金和基金定投策略。', 70, 1),
(5, '量化交易', '讨论量化模型、因子策略和程序化交易实践。', 60, 1),
(6, '价值投资', '价值投资理念与实践分享。', 50, 1),
(7, '新股新债', '新股申购与可转债讨论。', 40, 1),
(8, '宏观策略', '宏观经济与投资策略研讨。', 30, 1),
(9, '问答求助', '新手提问与投资解惑。', 20, 1)
ON DUPLICATE KEY UPDATE
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_active` = VALUES(`is_active`);

-- 初始化标签
INSERT INTO `tags` (`id`, `name`, `tag_type`) VALUES
(1, '贵州茅台', 'STOCK'),
(2, '沪深300', 'FUND'),
(3, '新能源', 'TOPIC'),
(4, '量化策略', 'TOPIC'),
(5, '风险提示', 'TOPIC')
ON DUPLICATE KEY UPDATE
    `tag_type` = VALUES(`tag_type`);

-- 初始化帖子
INSERT INTO `posts` (`id`, `section_id`, `user_id`, `title`, `post_type`, `content`, `status`, `view_count`, `like_count`, `comment_count`, `is_elite`) VALUES
(1, 1, 1, 'A股市场震荡时如何看待白酒板块？', 1, '最近白酒板块波动较大，本文从估值、业绩和资金情绪三个角度讨论，不构成投资建议。', 'PUBLISHED', 128, 18, 6, 0),
(2, 4, 1, '指数基金定投适合新手吗？', 1, '定投更适合长期资金和纪律性较强的投资者，关键是控制仓位和预期收益。', 'PUBLISHED', 96, 14, 4, 0),
(3, 5, 1, '一个简单的动量因子选股思路', 1, '用过去20日收益率作为动量因子可以形成基础策略，但还需要控制回撤和交易成本。', 'PUBLISHED', 76, 11, 3, 0),
(4, 8, 1, '降息预期下的大类资产配置讨论', 1, '宏观环境变化会影响股票、债券和商品的相对吸引力，需要结合风险偏好做配置。', 'PUBLISHED', 61, 8, 2, 0)
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `content` = VALUES(`content`),
    `status` = VALUES(`status`),
    `view_count` = VALUES(`view_count`),
    `like_count` = VALUES(`like_count`),
    `comment_count` = VALUES(`comment_count`),
    `is_elite` = VALUES(`is_elite`);

INSERT INTO `post_tags` (`post_id`, `tag_id`) VALUES
(1, 1),
(1, 5),
(2, 2),
(3, 4),
(4, 3)
ON DUPLICATE KEY UPDATE
    `post_id` = VALUES(`post_id`);

-- 初始化社交互动数据
INSERT INTO `comments` (`id`, `post_id`, `user_id`, `parent_id`, `content`, `like_count`) VALUES
(1, 1, 2, NULL, '白酒板块更适合结合现金流和估值区间看，短期波动不要线性外推。', 5),
(2, 1, 3, 1, '赞同，最好再叠加成交额和北向资金变化观察。', 2),
(3, 2, 3, NULL, '定投要先确定资金期限，不能把短期备用金放进去。', 4)
ON DUPLICATE KEY UPDATE
    `content` = VALUES(`content`),
    `like_count` = VALUES(`like_count`);

INSERT INTO `user_actions` (`id`, `user_id`, `target_id`, `target_type`, `action_type`) VALUES
(1, 2, 1, 1, 1),
(2, 2, 2, 1, 2),
(3, 3, 1, 1, 2)
ON DUPLICATE KEY UPDATE
    `user_id` = VALUES(`user_id`),
    `target_id` = VALUES(`target_id`),
    `target_type` = VALUES(`target_type`),
    `action_type` = VALUES(`action_type`);

INSERT INTO `user_follows` (`follower_id`, `followed_id`, `is_starred`) VALUES
(2, 3, 1),
(3, 2, 0)
ON DUPLICATE KEY UPDATE
    `is_starred` = VALUES(`is_starred`);

INSERT INTO `groups` (`id`, `creator_id`, `name`, `description`, `permission`) VALUES
(1, 3, '量化策略研究小组', '讨论因子、回测、风控和策略复盘。', 1),
(2, 2, '指数基金长期定投', '适合长期配置和新手基金投资交流。', 1),
(3, 3, '专业策略审核群', '需审核后加入的策略交流小组。', 2)
ON DUPLICATE KEY UPDATE
    `name` = VALUES(`name`),
    `description` = VALUES(`description`),
    `permission` = VALUES(`permission`);

INSERT INTO `group_members` (`group_id`, `user_id`) VALUES
(1, 3),
(1, 2),
(2, 2)
ON DUPLICATE KEY UPDATE
    `group_id` = VALUES(`group_id`);

INSERT INTO `group_join_requests` (`group_id`, `user_id`, `status`) VALUES
(3, 2, 'pending')
ON DUPLICATE KEY UPDATE
    `status` = VALUES(`status`);

INSERT INTO `notifications` (`id`, `user_id`, `title`, `content`, `notification_type`, `target_type`, `target_id`, `is_read`) VALUES
(1, 2, '评论收到回复', '量化研究员回复了你的评论', 'interaction', 'post', 1, 0),
(2, 3, '新增关注', '价值观察员关注了你', 'interaction', 'user', 2, 0)
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `content` = VALUES(`content`),
    `is_read` = VALUES(`is_read`);

-- 初始化后台审核队列
INSERT INTO `audit_queue_items` (`id`, `content_type`, `title`, `author_name`, `reason`, `risk_level`, `status`) VALUES
(1, 'post', '推荐某股票明天必涨停', '短线猎手', '违规荐股', 'high', 'pending'),
(2, 'comment', '保证收益，跟单联系我', '暴涨带队', '广告引流', 'high', 'pending'),
(3, 'attachment', '基金收益分析表', '稳健定投者', '附件待审核', 'medium', 'reviewing')
ON DUPLICATE KEY UPDATE
    `content_type` = VALUES(`content_type`),
    `title` = VALUES(`title`),
    `author_name` = VALUES(`author_name`),
    `reason` = VALUES(`reason`),
    `risk_level` = VALUES(`risk_level`),
    `status` = VALUES(`status`);

-- 初始化举报处理数据
INSERT INTO `report_items` (`id`, `target_type`, `target_title`, `reporter_name`, `reason`, `status`) VALUES
(1, 'post', '内部消息，今晚布局', '价值观察员', '虚假荐股', 'pending'),
(2, 'comment', '拉你进群带你赚钱', '理性投资人', '广告引流', 'pending')
ON DUPLICATE KEY UPDATE
    `target_type` = VALUES(`target_type`),
    `target_title` = VALUES(`target_title`),
    `reporter_name` = VALUES(`reporter_name`),
    `reason` = VALUES(`reason`),
    `status` = VALUES(`status`);

-- 初始化敏感词规则
INSERT INTO `sensitive_words` (`id`, `keyword`, `category`, `risk_level`, `action`, `enabled`, `note`) VALUES
(1, '稳赚不赔', '违规荐股', 'high', 'manual_review', 1, '高风险承诺收益表述'),
(2, '内部消息', '违规荐股', 'high', 'manual_review', 1, '涉及未证实内幕信息'),
(3, '带单', '广告引流', 'medium', 'manual_review', 1, '常见引流词')
ON DUPLICATE KEY UPDATE
    `keyword` = VALUES(`keyword`),
    `category` = VALUES(`category`),
    `risk_level` = VALUES(`risk_level`),
    `action` = VALUES(`action`),
    `enabled` = VALUES(`enabled`),
    `note` = VALUES(`note`);

-- 初始化用户处罚记录
INSERT INTO `user_moderation_records` (`id`, `user_name`, `action`, `reason`, `status`) VALUES
(1, '暴涨带队', 'warning', '多次发布广告引流评论', 'active'),
(2, '内幕先知道', 'mute', '散布未证实内幕消息', 'muted'),
(3, '稳赚俱乐部', 'ban', '反复发布违规荐股内容', 'banned')
ON DUPLICATE KEY UPDATE
    `user_name` = VALUES(`user_name`),
    `action` = VALUES(`action`),
    `reason` = VALUES(`reason`),
    `status` = VALUES(`status`);
