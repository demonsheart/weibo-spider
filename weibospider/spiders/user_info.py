import scrapy
import json
from scrapy.http import Request
from weibospider.items import UserInfoItem
import time


class UserInfoSpider(scrapy.Spider):
    name = 'user_info'
    # allowed_domains = ['weibo.com']

    base_url = "https://weibo.com/ajax/profile/info"  # 微博的接口
    # https://weibo.com/ajax/profile/info?uid=6239439310

    # 轮次
    rounds = 5

    def __init__(self, *args, **kwargs):
        super(UserInfoSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        uids = ['6239620007'] * 50  # 生成50条
        start_urls = [f'{self.base_url}?uid={uid}' for uid in uids]
        cur_round = 0
        while self.rounds > cur_round:
            cur_round += 1
            print(f"===========第{cur_round}轮============")
            for url in start_urls:
                # 使用本机代理
                # cur_ip = f'http://127.0.0.1:7890'
                # yield Request(url, callback=self.parse, headers=self.headers, dont_filter=True, meta={'proxy': cur_ip})

                # 默认走通过全局代理
                yield Request(url, callback=self.parse, dont_filter=True)
            # 每一分钟提交一次
            time.sleep(10)

    def parse(self, response, **kwargs):
        data = json.loads(response.text)
        ok = bool(data['ok'])
        if ok:
            # print(data['data'])
            bloc = data['data']
            item = UserInfoItem()
            item['user_id'] = str(bloc['user']['id'])  # 源微博id
            item['friends_count'] = str(bloc['user']['friends_count'])  # 关注数
            item['followers_count'] = str(bloc['user']['followers_count'])  # 粉丝数
            item['statuses_count'] = str(bloc['user']['statuses_count'])  # 微博数
            yield item
        else:
            print(data)
            pass
