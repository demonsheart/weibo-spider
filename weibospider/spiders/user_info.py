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
        pids = ['6239439310']  # 深圳大学的pid
        # https://weibo.com/ajax/profile/info?uid=6239439310
        start_urls = [f'{self.base_url}?uid={pid}' for pid in pids]
        for url in start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        blocs = data['data']
        for bloc in blocs:
            user_id = bloc['user']['id']  # 用户id
            followee_count = bloc['user']['friends_count']  # 关注数
            follower_count = bloc['user']['followers_count']  # 粉丝数
            statuses_count = bloc['user']['statuses_count']  # 微博数
            item = UserInfoItem()
            item['user_id'] = user_id
            item['followee_count'] = followee_count
            item['follower_count'] = follower_count
            item['statuses_count'] = statuses_count
            print(item)
            print("\n\n")
            yield item
