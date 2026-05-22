-- 智投社区数据库建表脚本
-- 成员B：论坛内容模块（板块、帖子、标签、搜索、热榜）

CREATE DATABASE IF NOT EXISTS `forum_system_db`
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE `forum_system_db`;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS `post_tags`;
DROP TABLE IF EXISTS `posts`;
DROP TABLE IF EXISTS `tags`;
DROP TABLE IF EXISTS `sections`;

CREATE TABLE `sections` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '板块ID',
    `name` VARCHAR(50) NOT NULL COMMENT '板块名称',
    `description` VARCHAR(255) NULL COMMENT '板块简介',
    `sort_order` INT NOT NULL DEFAULT 0 COMMENT '排序权重',
    `is_active` TINYINT NOT NULL DEFAULT 1 COMMENT '是否启用：1启用，0停用',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_sections_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='论坛板块表';

CREATE TABLE `posts` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '帖子ID',
    `section_id` INT NOT NULL COMMENT '所属板块ID',
    `user_id` BIGINT NOT NULL DEFAULT 1 COMMENT '发布者ID，模块联调前使用模拟用户',
    `title` VARCHAR(120) NOT NULL COMMENT '帖子标题',
    `content` TEXT NOT NULL COMMENT '帖子正文',
    `status` VARCHAR(20) NOT NULL DEFAULT 'PUBLISHED' COMMENT 'PENDING/PUBLISHED/REJECTED/DELETED',
    `view_count` INT NOT NULL DEFAULT 0 COMMENT '浏览数',
    `like_count` INT NOT NULL DEFAULT 0 COMMENT '点赞数',
    `comment_count` INT NOT NULL DEFAULT 0 COMMENT '评论数',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '发布时间',
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_posts_section_status` (`section_id`, `status`),
    KEY `idx_posts_hot` (`view_count`, `like_count`, `comment_count`),
    CONSTRAINT `fk_posts_section` FOREIGN KEY (`section_id`) REFERENCES `sections` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='论坛帖子表';

CREATE TABLE `tags` (
    `id` INT NOT NULL AUTO_INCREMENT COMMENT '标签ID',
    `name` VARCHAR(50) NOT NULL COMMENT '标签名称',
    `tag_type` VARCHAR(20) NOT NULL DEFAULT 'TOPIC' COMMENT 'STOCK/FUND/TOPIC',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_tags_name` (`name`),
    KEY `idx_tags_type` (`tag_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='股票基金主题标签表';

CREATE TABLE `post_tags` (
    `post_id` BIGINT NOT NULL COMMENT '帖子ID',
    `tag_id` INT NOT NULL COMMENT '标签ID',
    PRIMARY KEY (`post_id`, `tag_id`),
    CONSTRAINT `fk_post_tags_post` FOREIGN KEY (`post_id`) REFERENCES `posts` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_post_tags_tag` FOREIGN KEY (`tag_id`) REFERENCES `tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='帖子标签关联表';

SET FOREIGN_KEY_CHECKS = 1;

