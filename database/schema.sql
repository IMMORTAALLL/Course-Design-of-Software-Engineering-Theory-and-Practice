-- 智投社区数据库建表脚本
-- 基于（模块2）db.md 设计文档生成，并合并成员A用户权限模块、成员B论坛内容模块与成员D后台审核模块。

CREATE DATABASE IF NOT EXISTS `forum_system_db`
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE `forum_system_db`;

SET FOREIGN_KEY_CHECKS = 0;

-- ==========================================================
-- 清理旧表
-- ==========================================================
DROP TABLE IF EXISTS `post_tags`;
DROP TABLE IF EXISTS `poll_votes`;
DROP TABLE IF EXISTS `poll_options`;
DROP TABLE IF EXISTS `notifications`;
DROP TABLE IF EXISTS `user_moderation_records`;
DROP TABLE IF EXISTS `sensitive_words`;
DROP TABLE IF EXISTS `report_items`;
DROP TABLE IF EXISTS `audit_queue_items`;
DROP TABLE IF EXISTS `reports`;
DROP TABLE IF EXISTS `audit_logs`;
DROP TABLE IF EXISTS `hot_topics`;
DROP TABLE IF EXISTS `search_history`;
DROP TABLE IF EXISTS `group_join_requests`;
DROP TABLE IF EXISTS `group_resources`;
DROP TABLE IF EXISTS `group_posts`;
DROP TABLE IF EXISTS `group_members`;
DROP TABLE IF EXISTS `groups`;
DROP TABLE IF EXISTS `private_messages`;
DROP TABLE IF EXISTS `user_follows`;
DROP TABLE IF EXISTS `user_actions`;
DROP TABLE IF EXISTS `attachments`;
DROP TABLE IF EXISTS `comments`;
DROP TABLE IF EXISTS `posts`;
DROP TABLE IF EXISTS `tags`;
DROP TABLE IF EXISTS `sections`;
DROP TABLE IF EXISTS `user_roles`;
DROP TABLE IF EXISTS `roles`;
DROP TABLE IF EXISTS `user_profiles`;
DROP TABLE IF EXISTS `users`;

-- ==========================================================
-- 模块 1：用户系统 (User System)
-- ==========================================================

CREATE TABLE `users` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '自增主键',
    `phone` VARCHAR(20) UNIQUE COMMENT '手机号',
    `email` VARCHAR(100) UNIQUE COMMENT '邮箱',
    `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '0:正常, 1:禁言, 2:封禁',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户基础表';

CREATE TABLE `user_profiles` (
    `user_id` BIGINT PRIMARY KEY COMMENT '关联用户ID',
    `nickname` VARCHAR(50) NOT NULL COMMENT '昵称',
    `avatar_url` VARCHAR(255) COMMENT '头像地址',
    `bio` VARCHAR(255) COMMENT '简介',
    `auth_level` TINYINT NOT NULL DEFAULT 0 COMMENT '0:基础, 1:实名, 2:专业',
    `risk_preference` TINYINT COMMENT '1:保守, 2:稳健, 3:进取',
    `influence_score` INT NOT NULL DEFAULT 0 COMMENT '影响力值',
    `experience_tags` VARCHAR(255) COMMENT 'experience tags JSON',
    `interest_markets` VARCHAR(255) COMMENT 'interest markets JSON',
    `privacy_level` TINYINT NOT NULL DEFAULT 0 COMMENT '0 public, 1 partial, 2 private',
    `post_count` INT NOT NULL DEFAULT 0 COMMENT 'post count',
    `elite_count` INT NOT NULL DEFAULT 0 COMMENT 'elite post count',
    `points` INT NOT NULL DEFAULT 0 COMMENT 'user points',
    `level` INT NOT NULL DEFAULT 1 COMMENT 'user level',
    `badge_title` VARCHAR(50) COMMENT 'achievement badge',
    CONSTRAINT `fk_profile_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户资料表';

CREATE TABLE `roles` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL UNIQUE COMMENT '角色标识',
    `description` VARCHAR(100) COMMENT '角色描述',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';

CREATE TABLE `user_roles` (
    `user_id` BIGINT NOT NULL,
    `role_id` INT NOT NULL,
    PRIMARY KEY (`user_id`, `role_id`),
    CONSTRAINT `fk_ur_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_ur_role` FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户角色关联表';

-- ==========================================================
-- 模块 2：内容系统 (Content System)
-- ==========================================================

CREATE TABLE `sections` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '板块ID',
    `name` VARCHAR(50) NOT NULL COMMENT '板块名称',
    `description` VARCHAR(255) COMMENT '板块简介',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序权重',
    `is_active` TINYINT NOT NULL DEFAULT 1 COMMENT '是否展示',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_sections_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='板块表';

CREATE TABLE `tags` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '标签ID',
    `name` VARCHAR(50) NOT NULL COMMENT '标签名称',
    `tag_type` VARCHAR(20) NOT NULL DEFAULT 'TOPIC' COMMENT 'STOCK/FUND/TOPIC',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_tags_name` (`name`),
    KEY `idx_tags_type` (`tag_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票基金主题标签表';

CREATE TABLE `posts` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '帖子ID',
    `section_id` INT NOT NULL COMMENT '板块ID',
    `user_id` BIGINT NOT NULL COMMENT '发布者ID',
    `title` VARCHAR(120) NOT NULL COMMENT '标题',
    `post_type` TINYINT NOT NULL DEFAULT 1 COMMENT '1:普通, 2:长文, 3:投票, 4:短动态',
    `content` LONGTEXT NOT NULL COMMENT '内容',
    `status` VARCHAR(20) NOT NULL DEFAULT 'PUBLISHED' COMMENT 'PENDING/PUBLISHED/REJECTED/DELETED',
    `view_count` INT NOT NULL DEFAULT 0 COMMENT '浏览数',
    `like_count` INT NOT NULL DEFAULT 0 COMMENT '点赞数',
    `comment_count` INT NOT NULL DEFAULT 0 COMMENT '评论数',
    `is_elite` TINYINT NOT NULL DEFAULT 0 COMMENT '是否加精',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_posts_section_status` (`section_id`, `status`),
    KEY `idx_posts_hot` (`view_count`, `like_count`, `comment_count`),
    CONSTRAINT `fk_post_section` FOREIGN KEY (`section_id`) REFERENCES `sections`(`id`),
    CONSTRAINT `fk_post_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='帖子表';

CREATE TABLE `post_tags` (
    `post_id` BIGINT NOT NULL COMMENT '帖子ID',
    `tag_id` INT NOT NULL COMMENT '标签ID',
    PRIMARY KEY (`post_id`, `tag_id`),
    CONSTRAINT `fk_post_tags_post` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_post_tags_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='帖子标签关联表';

CREATE TABLE `comments` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `post_id` BIGINT NOT NULL COMMENT '所属帖子ID',
    `user_id` BIGINT NOT NULL COMMENT '评论者ID',
    `parent_id` BIGINT DEFAULT NULL COMMENT '父级评论ID(楼中楼)',
    `content` TEXT NOT NULL COMMENT '内容',
    `like_count` INT NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_comment_post` FOREIGN KEY (`post_id`) REFERENCES `posts`(`id`),
    CONSTRAINT `fk_comment_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='评论表';

CREATE TABLE `attachments` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `post_id` BIGINT NOT NULL COMMENT '归属帖子ID',
    `file_url` VARCHAR(255) NOT NULL COMMENT '存储路径',
    `file_type` VARCHAR(20) NOT NULL COMMENT '文件格式',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_attachment_post` FOREIGN KEY (`post_id`) REFERENCES `posts`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='附件表';

CREATE TABLE `poll_options` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `post_id` BIGINT NOT NULL COMMENT 'poll post id',
    `option_text` VARCHAR(120) NOT NULL COMMENT 'option text',
    `vote_count` INT NOT NULL DEFAULT 0 COMMENT 'vote count',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_poll_option_post` FOREIGN KEY (`post_id`) REFERENCES `posts`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='poll options';

CREATE TABLE `poll_votes` (
    `post_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `option_id` BIGINT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`post_id`, `user_id`),
    CONSTRAINT `fk_poll_vote_post` FOREIGN KEY (`post_id`) REFERENCES `posts`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_poll_vote_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_poll_vote_option` FOREIGN KEY (`option_id`) REFERENCES `poll_options`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='poll votes';

CREATE TABLE `user_actions` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT NOT NULL,
    `target_id` BIGINT NOT NULL COMMENT '帖子或评论ID',
    `target_type` TINYINT NOT NULL COMMENT '1:帖子, 2:评论',
    `action_type` TINYINT NOT NULL COMMENT '1:点赞, 2:收藏',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_action_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='互动行为表';

-- ==========================================================
-- 模块 3：社交与关系系统 (Social System)
-- ==========================================================

CREATE TABLE `private_messages` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `sender_id` BIGINT NOT NULL,
    `receiver_id` BIGINT NOT NULL,
    `content` TEXT NOT NULL,
    `is_read` TINYINT NOT NULL DEFAULT 0,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_private_message_sender` FOREIGN KEY (`sender_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_private_message_receiver` FOREIGN KEY (`receiver_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='private messages';

CREATE TABLE `user_follows` (
    `follower_id` BIGINT NOT NULL,
    `followed_id` BIGINT NOT NULL,
    `is_starred` TINYINT NOT NULL DEFAULT 0 COMMENT '是否特别关注',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`follower_id`, `followed_id`),
    CONSTRAINT `fk_follow_follower` FOREIGN KEY (`follower_id`) REFERENCES `users`(`id`),
    CONSTRAINT `fk_follow_followed` FOREIGN KEY (`followed_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='关注关系表';

CREATE TABLE `groups` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `creator_id` BIGINT NOT NULL COMMENT '群主ID',
    `name` VARCHAR(50) NOT NULL,
    `description` VARCHAR(255) COMMENT '群组简介',
    `permission` TINYINT NOT NULL DEFAULT 1 COMMENT '1:公开, 2:审核, 3:私密',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_group_creator` FOREIGN KEY (`creator_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='群组表';

CREATE TABLE `group_members` (
    `group_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `join_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`group_id`, `user_id`),
    CONSTRAINT `fk_member_group` FOREIGN KEY (`group_id`) REFERENCES `groups`(`id`),
    CONSTRAINT `fk_member_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='群成员表';

CREATE TABLE `group_posts` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `group_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `content` TEXT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_group_post_group` FOREIGN KEY (`group_id`) REFERENCES `groups`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_group_post_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='group discussions';

CREATE TABLE `group_resources` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `group_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `title` VARCHAR(120) NOT NULL,
    `resource_url` VARCHAR(255) NOT NULL,
    `description` VARCHAR(255),
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_group_resource_group` FOREIGN KEY (`group_id`) REFERENCES `groups`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_group_resource_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='group resources';

CREATE TABLE `group_join_requests` (
    `group_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `status` VARCHAR(16) NOT NULL DEFAULT 'pending' COMMENT '申请状态：pending/approved/rejected',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`group_id`, `user_id`),
    CONSTRAINT `fk_join_request_group` FOREIGN KEY (`group_id`) REFERENCES `groups`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_join_request_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='群组加入申请表';

CREATE TABLE `notifications` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT NOT NULL COMMENT '接收用户ID',
    `title` VARCHAR(120) NOT NULL COMMENT '通知标题',
    `content` VARCHAR(255) NOT NULL COMMENT '通知内容',
    `notification_type` VARCHAR(32) NOT NULL DEFAULT 'interaction' COMMENT 'interaction/audit/system',
    `target_type` VARCHAR(32) DEFAULT NULL COMMENT 'post/comment/user/group',
    `target_id` BIGINT DEFAULT NULL COMMENT '关联目标ID',
    `is_read` TINYINT NOT NULL DEFAULT 0 COMMENT '是否已读',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY `idx_notifications_user_read` (`user_id`, `is_read`, `created_at`),
    CONSTRAINT `fk_notification_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户通知表';

-- ==========================================================
-- 模块 4：信息整合系统 (Integration System)
-- ==========================================================

CREATE TABLE `search_history` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT DEFAULT NULL COMMENT '游客搜索此项为空',
    `keyword` VARCHAR(100) NOT NULL COMMENT '关键词/代码',
    `search_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_search_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='搜索历史表';

CREATE TABLE `hot_topics` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `topic_name` VARCHAR(100) NOT NULL COMMENT '热门话题名',
    `rank_pos` INT NOT NULL COMMENT '排名',
    `hot_score` BIGINT NOT NULL COMMENT '热度值',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='热榜缓存表';

-- ==========================================================
-- 模块 5：管理运营系统 (Admin System)
-- ==========================================================

CREATE TABLE `audit_logs` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `target_id` BIGINT NOT NULL,
    `target_type` TINYINT NOT NULL COMMENT '1:帖子, 2:评论',
    `audit_status` TINYINT NOT NULL DEFAULT 0 COMMENT '0:待审, 1:通过, 2:驳回',
    `violation` TINYINT DEFAULT NULL COMMENT '违规类型',
    `admin_id` BIGINT DEFAULT NULL COMMENT '审核管理员ID',
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_audit_admin` FOREIGN KEY (`admin_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审核记录表';

CREATE TABLE `reports` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `reporter_id` BIGINT NOT NULL COMMENT '举报人ID',
    `target_id` BIGINT NOT NULL COMMENT '内容或用户ID',
    `target_type` TINYINT NOT NULL COMMENT '1:帖子, 2:评论, 3:用户',
    `reason` VARCHAR(255) NOT NULL COMMENT '举报理由',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '0:待处理, 1:已处理',
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_report_user` FOREIGN KEY (`reporter_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户举报表';

CREATE TABLE `audit_queue_items` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '审核队列条目ID',
    `content_type` VARCHAR(32) NOT NULL COMMENT '内容类型',
    `title` VARCHAR(255) NOT NULL COMMENT '内容标题',
    `author_name` VARCHAR(64) NOT NULL COMMENT '作者昵称',
    `reason` VARCHAR(255) NOT NULL COMMENT '进入审核队列原因',
    `risk_level` VARCHAR(16) NOT NULL DEFAULT 'medium' COMMENT '风险等级',
    `status` VARCHAR(16) NOT NULL DEFAULT 'pending' COMMENT '审核状态',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='后台审核队列表';

CREATE TABLE `report_items` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '举报处理条目ID',
    `target_type` VARCHAR(32) NOT NULL COMMENT '被举报对象类型',
    `target_title` VARCHAR(255) NOT NULL COMMENT '被举报对象标题',
    `reporter_name` VARCHAR(64) NOT NULL COMMENT '举报人昵称',
    `reason` VARCHAR(255) NOT NULL COMMENT '举报原因',
    `status` VARCHAR(16) NOT NULL DEFAULT 'pending' COMMENT '处理状态',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '举报时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='后台举报处理表';

CREATE TABLE `sensitive_words` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '敏感词ID',
    `keyword` VARCHAR(64) NOT NULL COMMENT '敏感词内容',
    `category` VARCHAR(32) NOT NULL COMMENT '分类',
    `risk_level` VARCHAR(16) NOT NULL DEFAULT 'medium' COMMENT '风险等级',
    `action` VARCHAR(32) NOT NULL DEFAULT 'manual_review' COMMENT '命中后动作',
    `enabled` TINYINT NOT NULL DEFAULT 1 COMMENT '是否启用',
    `note` TEXT NULL COMMENT '备注',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_sensitive_words_keyword` (`keyword`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='敏感词规则表';

CREATE TABLE `user_moderation_records` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '处罚记录ID',
    `user_name` VARCHAR(64) NOT NULL COMMENT '用户昵称',
    `action` VARCHAR(32) NOT NULL COMMENT '处罚动作',
    `reason` VARCHAR(255) NOT NULL COMMENT '处罚原因',
    `status` VARCHAR(16) NOT NULL DEFAULT 'active' COMMENT '当前状态',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '处罚时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户处罚记录表';

SET FOREIGN_KEY_CHECKS = 1;
