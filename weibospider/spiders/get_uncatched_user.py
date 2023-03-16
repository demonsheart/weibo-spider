import pymysql
import scrapy
import json
from scrapy.http import Request
from weibospider.items import HotsearchUserInfoItem
from weibospider import private_setting


# 获取由于抓取失败没拿到的user_info
class GetUncatchedUserSpider(scrapy.Spider):
    name = 'get_uncatched_user'
    # allowed_domains = ['weibo.com']

    base_url = "https://weibo.com/ajax/profile/info"  # 微博的接口

    def __init__(self, *args, **kwargs):
        super(GetUncatchedUserSpider, self).__init__(*args, **kwargs)
        self.connect = pymysql.connect(
            host=private_setting.MYSQL_HOST,
            db=private_setting.MYSQL_DATABASE,
            user=private_setting.MYSQL_USERNAME,
            passwd=private_setting.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        self.cursor = self.connect.cursor()

    def start_requests(self):
        # 查询差集 寻找没被存下来的user
        sql1 = '''
        CREATE OR REPLACE VIEW total_user AS
        SELECT origin_user_id AS user_id FROM weibo_hotsearch
        UNION
        SELECT repost_user_id AS user_id FROM repost_weibo_hotsearch
        '''

        sql2 = '''
        SELECT user_id FROM total_user
        WHERE NOT EXISTS
        (SELECT user_id FROM user_info_hotsearch 
        WHERE total_user.user_id = user_info_hotsearch.user_id)
        '''

        self.cursor.execute(sql1)
        self.cursor.execute(sql2)
        ret = list(self.cursor.fetchall())
        if ret:
            uids = [str(i[0]) for i in ret]
            start_urls = [f'{self.base_url}?uid={uid}' for uid in uids]
            for url in start_urls:
                # 使用本机代理
                # cur_ip = f'http://127.0.0.1:7890'
                # yield Request(url, callback=self.parse, headers=self.headers, dont_filter=True, meta={'proxy': cur_ip})

                # 默认走通过全局代理
                yield Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        ok = bool(data['ok'])
        if ok:
            user_info = data['data']
            item = HotsearchUserInfoItem()
            item['user_id'] = str(user_info['user']['id'])  # 源微博id
            item['friends_count'] = str(user_info['user']['friends_count'])  # 关注数
            item['followers_count'] = str(user_info['user']['followers_count'])  # 粉丝数
            item['statuses_count'] = str(user_info['user']['statuses_count'])  # 微博数
            yield item
        else:
            print(data)
            pass
