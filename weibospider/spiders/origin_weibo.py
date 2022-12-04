import scrapy
import json
from scrapy.http import Request
from weibospider.mytools.common import parse_bloc, parse_long_bloc


# scrapy crawl origin_weibo -a max_page=5
class OriginWeiboSpider(scrapy.Spider):
    name = 'origin_weibo'
    # allowed_domains = ['weibo.com']
    base_url = "https://weibo.com"  # 微博的接口

    def __init__(self, max_page=None, *args, **kwargs):
        super(OriginWeiboSpider, self).__init__(*args, **kwargs)
        self.max_page = max_page

    def start_requests(self):
        # 这里user_ids可替换成实际待采集的数据
        user_ids = ['6239620007']  # 深圳大学的pid
        for user_id in user_ids:
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={user_id}&page=1"
            yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': 1})

    def parse(self, response, **kwargs):
        self.logger.info('Parse function called on %s', response.url)
        data = json.loads(response.text)
        blocs = data['data']['list']
        for bloc in blocs:
            item = parse_bloc(bloc)
            # 长文的正文需要另外请求处理
            if bloc["isLongText"]:
                url = "https://weibo.com/ajax/statuses/longtext?id=" + bloc['mblogid']
                print(item)
                print("\n\n")
                yield Request(url, callback=parse_long_bloc, meta={'item': item})
            else:
                yield item
        # 如果还有数据 就尝试请求下一页数据
        if blocs:
            user_id, page_num = response.meta['user_id'], response.meta['page_num']
            page_num += 1
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={user_id}&page={page_num}"
            if self.max_page:  # max_page限制
                if page_num <= int(self.max_page):
                    yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})
            else:  # 无限制请求
                yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})
