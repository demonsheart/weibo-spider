import scrapy
import json
from weibospider.items import HotBandItem

# scrapy crawl hot_band -O hot_band.csv  导出此刻热搜榜
class HotBandSpider(scrapy.Spider):
    name = 'hot_band'
    allowed_domains = ['weibo.com']
    start_urls = ['https://weibo.com/ajax/statuses/hot_band']

    def parse(self, response):
        data = json.loads(response.text)
        band_list = data['data']['band_list']
        for band in band_list:
            item = HotBandItem()
            if 'num' in band and 'onboard_time' in band and 'word_scheme' in band:
                item['num'] = band['num']
                item['onboard_time'] = band['onboard_time']
                item['word_scheme'] = band['word_scheme']
                yield item
