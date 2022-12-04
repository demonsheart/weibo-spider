import scrapy
import json
from scrapy.http import Request
from weibospider.items import UserInfoItem


class UserInfoSpider(scrapy.Spider):
    name = 'user_info'
    # allowed_domains = ['weibo.com']
    base_url = "https://weibo.com/ajax/profile/info"  # 微博的接口
    # https://weibo.com/ajax/profile/info?uid=6239439310
    cur_page = 1

    def start_requests(self):
        pids = ['6239439310']  # 用户的pid
        # https://weibo.com/ajax/profile/info?uid=6239439310
        start_urls = [f'{self.base_url}?uid={pid}' for pid in pids]
        for url in start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        bloc = data['data']
        item = UserInfoItem()
        item['user_id'] = str(bloc['user']['id'])  # 源微博id
        item['friends_count'] = str(bloc['user']['friends_count'])  # 关注数
        item['followers_count'] = str(bloc['user']['followers_count'])  # 粉丝数
        item['statuses_count'] = str(bloc['user']['statuses_count'])  # 微博数
        print(item)
        print("\n\n")
        yield item
