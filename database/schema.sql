-- 智投社区数据库建表脚本
-- 基于（模块2）db.md 设计文档生成

-- 1. 创建并切换数据库
CREATE DATABASE IF NOT EXISTS `forum_system_db`
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE `forum_system_db`;

-- 关闭外键检查以确保表创建顺序不影响执行
SET FOREIGN_KEY_CHECKS = 0;

-- ==========================================================
-- 模块 1：用户系统 (User System)
-- ==========================================================

-- 用户基础表
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '自增主键',
    `phone` VARCHAR(20) UNIQUE COMMENT '手机号',
    `email` VARCHAR(100) UNIQUE COMMENT '邮箱',
    `password_hash` VARCHAR(255) NOT NULL COMMENT '密码哈希',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '0:正常, 1:禁言, 2:封禁',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB COMMENT='用户基础表';

-- 用户资料表 (与用户表 1:1)
DROP TABLE IF EXISTS `user_profiles`;
CREATE TABLE `user_profiles` (
    `user_id` BIGINT PRIMARY KEY COMMENT '关联用户ID',
    `nickname` VARCHAR(50) NOT NULL COMMENT '昵称',
    `avatar_url` VARCHAR(255) COMMENT '头像地址',
    `bio` VARCHAR(255) COMMENT '简介',
    `auth_level` TINYINT NOT NULL DEFAULT 0 COMMENT '0:基础, 1:实名, 2:专业',
    `risk_preference` TINYINT COMMENT '1:保守, 2:稳健, 3:进取',
    `influence_score` INT NOT NULL DEFAULT 0 COMMENT '影响力值',
    CONSTRAINT `fk_profile_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='用户资料表';

-- 角色表
DROP TABLE IF EXISTS `roles`;
CREATE TABLE `roles` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(20) NOT NULL UNIQUE COMMENT '角色标识',
    `description` VARCHAR(100) COMMENT '角色描述',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB COMMENT='角色表';

-- 用户角色关联表
DROP TABLE IF EXISTS `user_roles`;
CREATE TABLE `user_roles` (
    `user_id` BIGINT NOT NULL,
    `role_id` INT NOT NULL,
    PRIMARY KEY (`user_id`, `role_id`),
    CONSTRAINT `fk_ur_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_ur_role` FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB COMMENT='用户角色关联表';

-- ==========================================================
-- 模块 2：内容系统 (Content System)
-- ==========================================================

-- 板块表
DROP TABLE IF EXISTS `sections`;
CREATE TABLE `sections` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(50) NOT NULL COMMENT '板块名',
    `description` VARCHAR(255) COMMENT '描述',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序权重',
    `is_active` TINYINT NOT NULL DEFAULT 1 COMMENT '是否展示',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB COMMENT='板块表';

-- 帖子表
DROP TABLE IF EXISTS `posts`;
CREATE TABLE `posts` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `section_id` INT NOT NULL COMMENT '板块ID',
    `user_id` BIGINT NOT NULL COMMENT '发布者ID',
    `title` VARCHAR(100) NOT NULL COMMENT '标题',
    `post_type` TINYINT NOT NULL DEFAULT 1 COMMENT '1:普通, 2:长文, 3:投票, 4:短动态',
    `content` LONGTEXT NOT NULL COMMENT '内容',
    `like_count` INT NOT NULL DEFAULT 0 COMMENT '点赞数',
    `is_elite` TINYINT NOT NULL DEFAULT 0 COMMENT '是否加精',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_post_section` FOREIGN KEY (`section_id`) REFERENCES `sections`(`id`),
    CONSTRAINT `fk_post_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB COMMENT='帖子表';

-- 评论表
DROP TABLE IF EXISTS `comments`;
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
) ENGINE=InnoDB COMMENT='评论表';

-- 附件表
DROP TABLE IF EXISTS `attachments`;
CREATE TABLE `attachments` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `post_id` BIGINT NOT NULL COMMENT '归属帖子ID',
    `file_url` VARCHAR(255) NOT NULL COMMENT '存储路径',
    `file_type` VARCHAR(20) NOT NULL COMMENT '文件格式',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_attachment_post` FOREIGN KEY (`post_id`) REFERENCES `posts`(`id`)
) ENGINE=InnoDB COMMENT='附件表';

-- 互动行为表 (点赞/收藏)
DROP TABLE IF EXISTS `user_actions`;
CREATE TABLE `user_actions` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT NOT NULL,
    `target_id` BIGINT NOT NULL COMMENT '帖子或评论ID',
    `target_type` TINYINT NOT NULL COMMENT '1:帖子, 2:评论',
    `action_type` TINYINT NOT NULL COMMENT '1:点赞, 2:收藏',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_action_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB COMMENT='互动行为表';

-- ==========================================================
-- 模块 3：社交与关系系统 (Social System)
-- ==========================================================

-- 关注关系表
DROP TABLE IF EXISTS `user_follows`;
CREATE TABLE `user_follows` (
    `follower_id` BIGINT NOT NULL,
    `followed_id` BIGINT NOT NULL,
    `is_starred` TINYINT NOT NULL DEFAULT 0 COMMENT '是否特别关注',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`follower_id`, `followed_id`),
    CONSTRAINT `fk_follow_follower` FOREIGN KEY (`follower_id`) REFERENCES `users`(`id`),
    CONSTRAINT `fk_follow_followed` FOREIGN KEY (`followed_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB COMMENT='关注关系表';

-- 群组表
DROP TABLE IF EXISTS `groups`;
CREATE TABLE `groups` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `creator_id` BIGINT NOT NULL COMMENT '群主ID',
    `name` VARCHAR(50) NOT NULL,
    `permission` TINYINT NOT NULL DEFAULT 1 COMMENT '1:公开, 2:审核, 3:私密',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_group_creator` FOREIGN KEY (`creator_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB COMMENT='群组表';

-- 群成员关联表
DROP TABLE IF EXISTS `group_members`;
CREATE TABLE `group_members` (
    `group_id` BIGINT NOT NULL,
    `user_id` BIGINT NOT NULL,
    `join_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`group_id`, `user_id`),
    CONSTRAINT `fk_member_group` FOREIGN KEY (`group_id`) REFERENCES `groups`(`id`),
    CONSTRAINT `fk_member_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB COMMENT='群成员表';

-- ==========================================================
-- 模块 4：信息整合系统 (Integration System)
-- ==========================================================

-- 搜索历史表
DROP TABLE IF EXISTS `search_history`;
CREATE TABLE `search_history` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT DEFAULT NULL COMMENT '游客搜索此项为空',
    `keyword` VARCHAR(100) NOT NULL COMMENT '关键词/代码',
    `search_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_search_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB COMMENT='搜索历史表';

-- 热榜缓存表
DROP TABLE IF EXISTS `hot_topics`;
CREATE TABLE `hot_topics` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `topic_name` VARCHAR(100) NOT NULL COMMENT '热门话题名',
    `rank_pos` INT NOT NULL COMMENT '排名',
    `hot_score` BIGINT NOT NULL COMMENT '热度值',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB COMMENT='热榜缓存表';

-- ==========================================================
-- 模块 5：管理运营系统 (Admin System)
-- ==========================================================

-- 审核记录表
DROP TABLE IF EXISTS `audit_logs`;
CREATE TABLE `audit_logs` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `target_id` BIGINT NOT NULL,
    `target_type` TINYINT NOT NULL COMMENT '1:帖子, 2:评论',
    `audit_status` TINYINT NOT NULL DEFAULT 0 COMMENT '0:待审, 1:通过, 2:驳回',
    `violation` TINYINT DEFAULT NULL COMMENT '违规类型',
    `admin_id` BIGINT DEFAULT NULL COMMENT '审核管理员ID',
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_audit_admin` FOREIGN KEY (`admin_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB COMMENT='审核记录表';

-- 用户举报表
DROP TABLE IF EXISTS `reports`;
CREATE TABLE `reports` (
    `id` BIGINT NOT NULL AUTO_INCREMENT,
    `reporter_id` BIGINT NOT NULL COMMENT '举报人ID',
    `target_id` BIGINT NOT NULL COMMENT '内容或用户ID',
    `target_type` TINYINT NOT NULL COMMENT '1:帖子, 2:评论, 3:用户',
    `reason` VARCHAR(255) NOT NULL COMMENT '举报理由',
    `status` TINYINT NOT NULL DEFAULT 0 COMMENT '0:待处理, 1:已处理',
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_report_user` FOREIGN KEY (`reporter_id`) REFERENCES `users`(`id`)
) ENGINE=InnoDB COMMENT='用户举报表';

-- 恢复外键检查
SET FOREIGN_KEY_CHECKS = 1;
