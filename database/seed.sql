-- 智投社区初始化演示数据
USE `forum_system_db`;

-- 初始化角色
INSERT INTO `roles` (`name`, `description`) VALUES
('USER', '普通用户'),
('VERIFIED', '认证用户'),
('MODERATOR', '版主'),
('ADMIN', '管理员');

-- 初始化板块
INSERT INTO `sections` (`name`, `description`, `sort_order`) VALUES
('A股市场', '中国A股市场行情与个股讨论', 10),
('港股市场', '港股市场行情与个股讨论', 9),
('美股市场', '美股市场行情与个股讨论', 8),
('基金专区', '各类公募/私募基金交流', 7),
('量化交易', '量化模型与算法策略探讨', 6),
('价值投资', '价值投资理念与实践分享', 5),
('新股新债', '新股申购与可转债讨论', 4),
('宏观策略', '宏观经济与投资策略研讨', 3),
('问答求助', '新手提问与投资解惑', 2);

-- 初始化管理员账号（密码: Admin123456）
-- 密码哈希由 passlib bcrypt 生成
INSERT INTO `users` (`phone`, `email`, `password_hash`, `status`) VALUES
('13800000001', 'admin@stockforum.com', '$2b$12$LJ3a4PmYlMQ8M8GZmBZ5aOJXHf9wMq5Y3xKjF5vN0yL8VfKjzKXXi', 0);

INSERT INTO `user_profiles` (`user_id`, `nickname`, `auth_level`) VALUES
(1, '系统管理员', 2);

INSERT INTO `user_roles` (`user_id`, `role_id`) VALUES
(1, 4);
