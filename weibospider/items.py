# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# 源微博文件Item
class OriginWeiboItem(scrapy.Item):
    origin_weibo_id = scrapy.Field()  # 源微博id
    origin_user_id = scrapy.Field()  # 源用户id
    origin_weibo_content = scrapy.Field()  # 源微博文本内容
    publish_time = scrapy.Field()  # 发布时间
    repost_count = scrapy.Field()  # 转发数
    like_count = scrapy.Field()  # 点赞数


# 转发微博文件Item
class RepostWeiboItem(scrapy.Item):
    origin_weibo_id = scrapy.Field()  # 源微博id
    origin_user_id = scrapy.Field()  # 源用户id
    repost_weibo_id = scrapy.Field()  # 转发微博id
    repost_user_id = scrapy.Field()  # 转发用户id
    repost_weibo_content = scrapy.Field()  # 转发正文
    repost_publish_time = scrapy.Field()  # 转发时间


# 用户信息文件
class UserInfoItem(scrapy.Item):
    user_id = scrapy.Field()  # 用户id
    friends_count = scrapy.Field()  # 关注数
    followers_count = scrapy.Field()  # 粉丝数
    statuses_count = scrapy.Field()  # 微博数


class WeiboHotSearchItem(scrapy.Item):
    origin_weibo_id = scrapy.Field()  # 源微博id
    origin_user_id = scrapy.Field()  # 源用户id
    origin_weibo_content = scrapy.Field()  # 源微博文本内容
    publish_time = scrapy.Field()  # 发布时间
    repost_count = scrapy.Field()  # 转发数
    like_count = scrapy.Field()  # 点赞数


class HotSearchRepostWeiboItem(scrapy.Item):
    origin_weibo_id = scrapy.Field()  # 源微博id
    origin_user_id = scrapy.Field()  # 源用户id
    repost_weibo_id = scrapy.Field()  # 转发微博id
    repost_user_id = scrapy.Field()  # 转发用户id
    repost_weibo_content = scrapy.Field()  # 转发正文
    repost_publish_time = scrapy.Field()  # 转发时间


# 用户信息文件
class HotsearchUserInfoItem(scrapy.Item):
    user_id = scrapy.Field()  # 用户id
    friends_count = scrapy.Field()  # 关注数
    followers_count = scrapy.Field()  # 粉丝数
    statuses_count = scrapy.Field()  # 微博数

class WeiboCityItem(scrapy.Item):
    origin_weibo_id = scrapy.Field()  # 源微博id
    origin_user_id = scrapy.Field()  # 源用户id
    origin_weibo_content = scrapy.Field()  # 源微博文本内容
    publish_time = scrapy.Field()  # 发布时间
    repost_count = scrapy.Field()  # 转发数
    like_count = scrapy.Field()  # 点赞数


class CityRepostWeiboItem(scrapy.Item):
    origin_weibo_id = scrapy.Field()  # 源微博id
    origin_user_id = scrapy.Field()  # 源用户id
    repost_weibo_id = scrapy.Field()  # 转发微博id
    repost_user_id = scrapy.Field()  # 转发用户id
    repost_weibo_content = scrapy.Field()  # 转发正文
    repost_publish_time = scrapy.Field()  # 转发时间


# 用户信息文件
class CityUserInfoItem(scrapy.Item):
    user_id = scrapy.Field()  # 用户id
    friends_count = scrapy.Field()  # 关注数
    followers_count = scrapy.Field()  # 粉丝数
    statuses_count = scrapy.Field()  # 微博数

class HotBandItem(scrapy.Item):
    num = scrapy.Field()  # id
    word = scrapy.Field()  # 热榜关键词
    onboard_time = scrapy.Field()  # 时间
    raw_hot = scrapy.Field()  # 热度
    category = scrapy.Field()  # 类别
    note = scrapy.Field()
    star_name = scrapy.Field()  # 大V名字列表
    word_scheme = scrapy.Field()  # 关键字 用来搜索
    label_name = scrapy.Field()  # 爆/热/新
    rank = scrapy.Field()  # 排行
