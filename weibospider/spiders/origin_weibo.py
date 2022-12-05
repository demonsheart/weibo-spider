import scrapy
import json
from diskcache import Cache
from scrapy.http import Request
from weibospider.mytools.common import parse_bloc, parse_long_bloc


# scrapy crawl origin_weibo -a max_page=5 -a reset_page=True
class OriginWeiboSpider(scrapy.Spider):
    name = 'origin_weibo'
    # allowed_domains = ['weibo.com']
    base_url = "https://weibo.com"  # 微博的接口

    user_ids = ['6239620007']  # 深圳大学的pid
    SAVED_PAGE_KEY = 'weibo_downloaded_pages'

    def __init__(self, max_page=None, reset_page=False, *args, **kwargs):
        super(OriginWeiboSpider, self).__init__(*args, **kwargs)
        self.max_page = max_page

        # 根据cache初始化user_ids_pages 从上一次失败的page开始爬起
        self.cache = Cache(r"weibospider/disk")
        if reset_page:
            self.cache.set(self.SAVED_PAGE_KEY, {key: 1 for key in self.user_ids})
        self.user_ids_pages = self.cache.get(self.SAVED_PAGE_KEY, default={key: 1 for key in self.user_ids})

    def start_requests(self):
        # 这里user_ids可替换成实际待采集的数据
        for user_id in self.user_ids:
            url = f"https://weibo.com/ajax/statuses/mymblog?uid={user_id}&page={self.user_ids_pages[user_id]}"
            yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': self.user_ids_pages[user_id]})

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
                    self.user_ids_pages[user_id] = page_num
                    yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})
            else:  # 无限制请求
                self.user_ids_pages[user_id] = page_num
                yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})

    def close(self, reason):
        # TODO: 爬虫停止则发送邮件通知

        # 同时记录当前的{userid : page} 下次启动入口时从page开始
        self.cache.set(self.SAVED_PAGE_KEY, self.user_ids_pages)
