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

            item['num'] = band['num']
            item['subject_querys'] = band['subject_querys']
            item['subject_label'] = band['subject_label']
            item['word'] = band['word']
            item['onboard_time'] = band['onboard_time']
            item['raw_hot'] = band['raw_hot']
            item['category'] = band['category']
            item['note'] = band['note']
            item['star_name'] = band['star_name']
            item['word_scheme'] = band['word_scheme']
            item['label_name'] = band['label_name']
            item['rank'] = band['rank']

            yield item
