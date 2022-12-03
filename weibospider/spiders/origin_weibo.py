import scrapy
import json
from scrapy import Spider
from scrapy.http import Request
from weibospider.items import OriginWeiboItem


class OriginWeiboSpider(scrapy.Spider):
    name = 'origin_weibo'
    # allowed_domains = ['weibo.com']
    base_url = "https://weibo.com/ajax/statuses/mymblog"  # 微博的接口
    cur_page = 1

    def start_requests(self):
        pids = ['6239620007']  # 深圳大学的pid
        # https://weibo.com/ajax/statuses/mymblog?uid=6239620007&page=1
        start_urls = [f'{self.base_url}?uid={pid}&page={self.cur_page}' for pid in pids]
        for url in start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text)
        print(data)

# class DouyuSpider(scrapy.Spider):
#     name = 'douyu'
#     allowed_domains = ['douyucdn.cn']
#
#     baseURL = "http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset="
#     offset = 0
#     start_urls = [baseURL + str(offset)]
#
#     def parse(self, response):
#         data_list = json.loads(response.body)['data']
#         if len(data_list) == 0:
#             return
#         for data in data_list:
#             item = DouyuItem()
#             item['nickname'] = data['nickname']
#             item['imagelink'] = []
#             item['imagelink'].append(data['vertical_src'])
#
#             yield item
#
#         self.offset += 20
#         yield scrapy.Request(self.baseURL + str(self.offset), callback=self.parse)
