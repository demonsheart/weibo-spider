import json
import dateutil.parser
from weibospider.items import OriginWeiboItem
from weibospider.items import RepostWeiboItem
from weibospider.items import HotSearchRepostWeiboItem


def parse_time(s):
    """
    Wed Oct 19 23:44:36 +0800 2022 => 2022-10-19 23:44:36
    """
    return dateutil.parser.parse(s).strftime('%Y-%m-%d %H:%M:%S')


def parse_bloc(bloc):
    item = OriginWeiboItem()
    item['origin_weibo_id'] = str(bloc['mid'])  # 源微博id
    item['origin_user_id'] = str(bloc['user']['id'])  # 源用户id
    item['origin_weibo_content'] = bloc['text_raw'].replace('\u200b', '')  # 源微博文本内容
    item['publish_time'] = parse_time(bloc['created_at'])  # 发布时间
    item['repost_count'] = bloc['reposts_count']  # 转发数
    item['like_count'] = bloc['attitudes_count']  # 点赞数
    return item

def parse_repost_bloc(bloc):
    item = RepostWeiboItem()
    item['origin_weibo_id'] = str(bloc['retweeted_status']['id'])  # 源微博id
    item['origin_user_id'] = str(bloc['retweeted_status']['user']['id'])  # 源用户id
    item['repost_weibo_id'] = str(bloc['id'])  # 转发微博id
    item['repost_user_id'] = str(bloc['user']['id'])  # 转发用户id
    item['repost_weibo_content'] = bloc['text_raw']  # 转发正文
    item['repost_publish_time'] = parse_time(bloc['created_at'])  # 转发时间
    return item

def hot_search_parse_repost_bloc(bloc):
    item = HotSearchRepostWeiboItem()
    item['origin_weibo_id'] = str(bloc['retweeted_status']['id'])  # 源微博id
    item['origin_user_id'] = str(bloc['retweeted_status']['user']['id'])  # 源用户id
    item['repost_weibo_id'] = str(bloc['id'])  # 转发微博id
    item['repost_user_id'] = str(bloc['user']['id'])  # 转发用户id
    item['repost_weibo_content'] = bloc['text_raw']  # 转发正文
    item['repost_publish_time'] = parse_time(bloc['created_at'])  # 转发时间
    return item

def parse_long_bloc(response):
    """
    解析长推文
    """
    data = json.loads(response.text)['data']
    item = response.meta['item']
    item['origin_weibo_content'] = data['longTextContent']
    print("========LongText=========")
    print(item)
    print("\n\n")
    yield item
