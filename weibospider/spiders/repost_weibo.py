import scrapy
import json
from scrapy.http import Request

from weibospider.mytools.common import parse_repost_bloc, parse_long_bloc

class RepostWeiboSpider(scrapy.Spider):
    name = 'repost_weibo'
    # allowed_domains = ['weibo.com']
    base_url = "https://weibo.com/ajax/statuses/repostTimeline"  # 微博的接口

    def __init__(self, max_page=None, *args, **kwargs):
        super(RepostWeiboSpider, self).__init__(*args, **kwargs)
        self.max_page = max_page

    def start_requests(self):
        pids = ['4842349060955034']  # 深大口袋的微博id
        for pid in pids:
            url = f"https://weibo.com/ajax/statuses/repostTimeline?id={pid}&page=1&moduleID=feed&type=feed"
            yield Request(url, callback=self.parse, meta={'pid': pid, 'page_num': 1})

    def parse(self, response):
        data = json.loads(response.text)
        blocs = data['data']
        for bloc in blocs:
            item = parse_repost_bloc(bloc)
            yield item
        if blocs:
            pid, page_num = response.meta['pid'], response.meta['page_num']
            page_num += 1
            url = f"https://weibo.com/ajax/statuses/repostTimeline?id={pid}&page={page_num}&moduleID=feed&type=feed"
            if self.max_page:  # max_page限制
                if page_num <= int(self.max_page):
                    yield Request(url, callback=self.parse, meta={'pid': pid, 'page_num': page_num})
            else:  # 无限制请求
                yield Request(url, callback=self.parse, meta={'pid': pid, 'page_num': page_num})    
