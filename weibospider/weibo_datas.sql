/*
 Navicat Premium Data Transfer

 Source Server         : root_server
 Source Server Type    : MySQL
 Source Server Version : 80031 (8.0.31)
 Source Host           : 175.178.248.178:3306
 Source Schema         : weibo_datas_copy

 Target Server Type    : MySQL
 Target Server Version : 80031 (8.0.31)
 File Encoding         : 65001

 Date: 09/02/2023 09:58:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for repost_weibo
-- ----------------------------
DROP TABLE IF EXISTS `repost_weibo`;
CREATE TABLE `repost_weibo` (
  `repost_weibo_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `origin_weibo_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `origin_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `repost_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `repost_weibo_content` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `repost_publish_time` datetime DEFAULT NULL,
  PRIMARY KEY (`repost_weibo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for repost_weibo_hotsearch
-- ----------------------------
DROP TABLE IF EXISTS `repost_weibo_hotsearch`;
CREATE TABLE `repost_weibo_hotsearch` (
  `repost_weibo_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `origin_weibo_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `origin_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `repost_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `repost_weibo_content` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `repost_publish_time` datetime DEFAULT NULL,
  PRIMARY KEY (`repost_weibo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for user_info
-- ----------------------------
DROP TABLE IF EXISTS `user_info`;
CREATE TABLE `user_info` (
  `user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `friends_count` int DEFAULT NULL,
  `followers_count` int DEFAULT NULL,
  `statuses_count` int DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for user_info_hotsearch
-- ----------------------------
DROP TABLE IF EXISTS `user_info_hotsearch`;
CREATE TABLE `user_info_hotsearch` (
  `user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `friends_count` int DEFAULT NULL,
  `followers_count` int DEFAULT NULL,
  `statuses_count` int DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for weibo
-- ----------------------------
DROP TABLE IF EXISTS `weibo`;
CREATE TABLE `weibo` (
  `origin_weibo_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `origin_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `origin_weibo_content` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `publish_time` datetime DEFAULT NULL,
  `repost_count` int DEFAULT NULL,
  `like_count` int DEFAULT NULL,
  PRIMARY KEY (`origin_weibo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Table structure for weibo_hotsearch
-- ----------------------------
DROP TABLE IF EXISTS `weibo_hotsearch`;
CREATE TABLE `weibo_hotsearch` (
  `origin_weibo_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `origin_user_id` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `origin_weibo_content` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `publish_time` datetime DEFAULT NULL,
  `repost_count` int DEFAULT NULL,
  `like_count` int DEFAULT NULL,
  PRIMARY KEY (`origin_weibo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SET FOREIGN_KEY_CHECKS = 1;
