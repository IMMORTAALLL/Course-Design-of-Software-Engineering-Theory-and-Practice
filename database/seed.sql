-- 智投社区初始化演示数据
-- 成员B：论坛内容模块演示数据

USE `forum_system_db`;

INSERT INTO `sections` (`id`, `name`, `description`, `sort_order`, `is_active`) VALUES
(1, 'A股市场', '围绕A股行情、个股研究和交易经验展开讨论。', 100, 1),
(2, '基金专区', '交流公募基金、指数基金和基金定投策略。', 90, 1),
(3, '量化交易', '讨论量化模型、因子策略和程序化交易实践。', 80, 1),
(4, '宏观策略', '分享宏观经济、政策变化和资产配置观点。', 70, 1)
ON DUPLICATE KEY UPDATE
    `description` = VALUES(`description`),
    `sort_order` = VALUES(`sort_order`),
    `is_active` = VALUES(`is_active`);

INSERT INTO `tags` (`id`, `name`, `tag_type`) VALUES
(1, '贵州茅台', 'STOCK'),
(2, '沪深300', 'FUND'),
(3, '新能源', 'TOPIC'),
(4, '量化策略', 'TOPIC'),
(5, '风险提示', 'TOPIC')
ON DUPLICATE KEY UPDATE
    `tag_type` = VALUES(`tag_type`);

INSERT INTO `posts` (`id`, `section_id`, `user_id`, `title`, `content`, `status`, `view_count`, `like_count`, `comment_count`) VALUES
(1, 1, 1, 'A股市场震荡时如何看待白酒板块？', '最近白酒板块波动较大，本文从估值、业绩和资金情绪三个角度讨论，不构成投资建议。', 'PUBLISHED', 128, 18, 6),
(2, 2, 1, '指数基金定投适合新手吗？', '定投更适合长期资金和纪律性较强的投资者，关键是控制仓位和预期收益。', 'PUBLISHED', 96, 14, 4),
(3, 3, 1, '一个简单的动量因子选股思路', '用过去20日收益率作为动量因子可以形成基础策略，但还需要控制回撤和交易成本。', 'PUBLISHED', 76, 11, 3),
(4, 4, 1, '降息预期下的大类资产配置讨论', '宏观环境变化会影响股票、债券和商品的相对吸引力，需要结合风险偏好做配置。', 'PUBLISHED', 61, 8, 2)
ON DUPLICATE KEY UPDATE
    `title` = VALUES(`title`),
    `content` = VALUES(`content`),
    `status` = VALUES(`status`),
    `view_count` = VALUES(`view_count`),
    `like_count` = VALUES(`like_count`),
    `comment_count` = VALUES(`comment_count`);

INSERT INTO `post_tags` (`post_id`, `tag_id`) VALUES
(1, 1),
(1, 5),
(2, 2),
(3, 4),
(4, 3)
ON DUPLICATE KEY UPDATE
    `post_id` = VALUES(`post_id`);

