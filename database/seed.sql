-- 智投社区初始化演示数据
-- 合并成员A用户权限模块与成员B论坛内容模块演示数据。

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
