import time
from copy import deepcopy
import scrapy
import json
# import pymysql
import re
from time import sleep
# from diskcache import Cache
from scrapy.http import Request
# from weibospider.items import WeiboItem
# from weibospider.mytools.common import parse_bloc, parse_long_bloc, parse_repost_bloc
# from weibospider import private_setting
# from scrapy.mail import MailSender
from weibospider.items import WeiboHotSearchItem
from weibospider.mytools.common import parse_repost_bloc


# scrapy crawl origin_weibo -a max_page=5 -a reset_page=True
class WeiboHotSearchSpider(scrapy.Spider):
    name = 'weibo_hot_search'
    allowed_domains = ['s.weibo.com']
    start_urls=['https://s.weibo.com/weibo?q=%23%E4%B8%8A%E7%8F%AD%E9%98%B3%E4%BA%86%E7%AE%97%E5%B7%A5%E4%BC%A4%E5%90%97%23']
    def start_requests(self):
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
        )    
    def __init__(self, max_page=None, reset_page=False, *args, **kwargs):
      pass

    def parse(self, response, **kwargs):
        page_text = response.text
        with open('first.html','w',encoding='utf-8') as fp:
            fp.write(page_text)
        div_list = response.xpath('//div[@id="pl_feedlist_index"]//div[@class="card-wrap"]')[1:]            
        for div in div_list:
            item = WeiboHotSearchItem()

            publish_time = div.xpath(".//div[@class='from']/a[1]/text()").extract()
            publish_time = ''.join(publish_time)
            publish_time = publish_time.strip()
            print("发布时间:", publish_time)

            origin_weibo_content = div.xpath('.//p[@node-type="feed_list_content_full"]//text()').extract()#长文
            if origin_weibo_content:
                pass
            else:
                origin_weibo_content = div.xpath('.//p[@node-type="feed_list_content"]//text()').extract()#短文
            origin_weibo_content = ''.join(origin_weibo_content)
            origin_weibo_content = origin_weibo_content.strip()
            print("内容 : ",origin_weibo_content)

            like_count=div.xpath(".//span[@class='woo-like-count']/text()").extract()#点赞数
            like_count=like_count[0]
            if  "赞" in like_count:
                like_count ="0"
            print("点赞数 : ",like_count)

            repost_count=div.xpath(".//a[@action-type='feed_list_forward']/text()").extract()#转发数
            repost_count=repost_count[1]
            if  "转发" in repost_count :
                repost_count="0"
            print("转发数 : ",repost_count)
        
            orid=div.xpath(".//ul[@node-type='fl_menu_right']/li/a/@onclick").extract()#点赞数  
            orid=orid[0]
            rule = re.compile(r"\d+")
            orid = rule.findall(orid)
            origin_weibo_id=orid[0]
            origin_user_id=orid[1]
            print("这是mid : ",origin_weibo_id)
            print("这是uid : ",origin_user_id)

            print('--------------------------------   ------------------- --------------- --------------- --------------- --------------- \n')

            item['origin_weibo_id'] = origin_weibo_id  # 源微博id
            item['origin_user_id'] = origin_user_id  # 源用户id
            item['origin_weibo_content'] = origin_weibo_content.replace('\u200b', '')  # 源微博文本内容
            item['publish_time'] = publish_time  # 发布时间
            item['repost_count'] = repost_count  # 转发数
            item['like_count'] = like_count # 点赞数
            yield item

            # mid = origin_weibo_id
            # repost_page = self.repost_ids_pages[mid] if mid in self.repost_ids_pages else 1
            # repost_url = f'https://weibo.com/ajax/statuses/repostTimeline?page={1}&moduleID=feed&id={mid}'
            # yield Request(repost_url, callback=self.parse_repost, meta={'page_num': 1, 'mid': mid})



# def parse_repost(self, response):
#         self.logger.info('Parse function called on %s', response.url)
#         data = json.loads(response.text)
#         blocs = data['data']
#         for bloc in blocs:
#             item = parse_repost_bloc(bloc)
#             yield item
#             # 对每一个转发的微博 请求其user信息
#             user_id = str(bloc['user']['id'])
#             # 请求user信息
#             if not self.is_user_saved(user_id):
#                 user_url = f'https://weibo.com/ajax/profile/info?uid={user_id}'
#                 yield Request(user_url, callback=self.parse_user)
#         # 如果还有数据 就尝试请求下一页数据
#         if len(blocs) > 0:
#             mid, page_num = response.meta['mid'], response.meta['page_num']
#             page_num += 1
#             url = f"https://weibo.com/ajax/statuses/repostTimeline?page={page_num}&moduleID=feed&id={mid}"
#             if page_num <= 100:  # 转发推文请求限制页数
#                 self.repost_ids_pages[mid] = page_num
#                 self.cache.set(self.SAVED_REPOST_PAGE_KEY, self.repost_ids_pages)
#                 yield Request(url, callback=self.parse_repost, meta={'mid': mid, 'page_num': page_num})