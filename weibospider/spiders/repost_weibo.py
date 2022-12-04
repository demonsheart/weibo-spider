import scrapy
import json
from scrapy.http import Request
from weibospider.items import RepostWeiboItem


class RepostWeiboSpider(scrapy.Spider):
    name = 'repost_weibo'
    # allowed_domains = ['weibo.com']
    base_url = "https://weibo.com/ajax/statuses/repostTimeline"  # 微博的接口
    cur_page = 1

    def start_requests(self):
        pids = ['4842349060955034']  # 深大口袋的微博id
        # https://weibo.com/ajax/statuses/repostTimeline?id=4841505397409288&page=1&moduleID=feed&type=feed
        start_urls = [f'{self.base_url}?id={pid}&page={self.cur_page}&moduleID=feed&type=feed' for pid in pids]
        for url in start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        blocs = data['data']
        for bloc in blocs:
            origin_weibo_id = bloc['retweeted_status']['id']  # 源微博id
            origin_user_id = bloc['retweeted_status']['user']['id']  # 源用户id
            repost_weibo_id = bloc['id']  # 转发微博id
            repost_user_id = bloc['user']['id']  # 转发用户id
            repost_weibo_content = bloc['text_raw']  # 转发正文
            repost_publish_time = bloc['created_at']  # 转发时间
            item = RepostWeiboItem()
            item['origin_weibo_id'] = origin_weibo_id
            item['origin_user_id'] = origin_user_id
            item['repost_weibo_id'] = repost_weibo_id
            item['repost_user_id'] = repost_user_id
            item['repost_weibo_content'] = repost_weibo_content
            item['repost_publish_time'] = repost_publish_time
            # print(item)
            # print("\n\n")
            yield item
