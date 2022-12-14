import time
from copy import deepcopy
import scrapy
import json
import pymysql
import re
from time import sleep
from diskcache import Cache
from scrapy.http import Request
from weibospider.mytools.common import hot_search_parse_repost_bloc
from weibospider import private_setting
from weibospider.items import WeiboHotSearchItem,HotsearchUserInfoItem
from weibospider.mytools.common import parse_time
from scrapy.mail import MailSender

# scrapy crawl weibo_hot_search -a max_page=5 -a reset_page=True
class WeiboHotSearchSpider(scrapy.Spider):
    name = 'weibo_hot_search'
    SAVED_PAGE_KEY = 'weibo_hot_search_downloaded_pages'
    SAVED_REPOST_PAGE_KEY = 'weibo_hot_search_repost_pages'
    # allowed_domains = ['s.weibo.com']
    user_ids = ['%23%E4%B8%8A%E7%8F%AD%E9%98%B3%E4%BA%86%E7%AE%97%E5%B7%A5%E4%BC%A4%E5%90%97%23']
    # start_urls=['https://s.weibo.com/weibo?q=%23%E4%B8%8A%E7%8F%AD%E9%98%B3%E4%BA%86%E7%AE%97%E5%B7%A5%E4%BC%A4%E5%90%97%23']
    def __init__(self, max_page=None, reset_page=False, *args, **kwargs):
        super(WeiboHotSearchSpider, self).__init__(*args, **kwargs)
        self.max_page = max_page
        self.cache = Cache(r"weibospider/disk")
        if reset_page:
            self.cache.set(self.SAVED_PAGE_KEY, {key: 1 for key in self.user_ids})
        self.user_ids_pages = self.cache.get(self.SAVED_PAGE_KEY, default={key: 1 for key in self.user_ids})
        self.repost_ids_pages = self.cache.get(self.SAVED_REPOST_PAGE_KEY, default={})

        self.open_connect()

    def start_requests(self):
        for user_id in self.user_ids:
            HotsearchUrl=f'https://s.weibo.com/weibo?q={user_id}&page={self.user_ids_pages[user_id]}'
            yield scrapy.Request(HotsearchUrl,callback=self.parse,meta={'user_id': user_id ,'page_num': self.user_ids_pages[user_id]})   

    def open_connect(self):
        self.connect = pymysql.connect(
            host=private_setting.MYSQL_HOST,
            db=private_setting.MYSQL_DATABASE,
            user=private_setting.MYSQL_USERNAME,
            passwd=private_setting.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        self.cursor = self.connect.cursor()

    def is_user_saved(self, user_id):
        database = 'use weibo_datas;'
        sql = 'select * from user_info_hotsearch where user_id = %s'
        data = user_id
        self.cursor.execute(database)
        self.cursor.execute(sql, data)
        ret = self.cursor.fetchone()
        return ret is not None

    def parse(self, response, **kwargs):
        page_text = response.text
        # with open('first.html','w',encoding='utf-8') as fp:
        #     fp.write(page_text)
        div_list = response.xpath('//div[@id="pl_feedlist_index"]//div[@class="card-wrap"]')[1:]            
        for div in div_list:
            item = WeiboHotSearchItem()

            ttime = div.xpath(".//div[@class='from']/a[1]/text()").extract()
            ttime = ''.join(ttime)
            ttime = ttime.strip()
            # print("????????????:", ttime)
            publish_time =parse_time(ttime)
            origin_weibo_content = div.xpath('.//p[@node-type="feed_list_content_full"]//text()').extract()#??????
            if origin_weibo_content:
                pass
            else:
                origin_weibo_content = div.xpath('.//p[@node-type="feed_list_content"]//text()').extract()#??????
            origin_weibo_content = ''.join(origin_weibo_content)
            origin_weibo_content = origin_weibo_content.strip()
            # print("?????? : ",origin_weibo_content)

            like_count=div.xpath(".//span[@class='woo-like-count']/text()").extract()#?????????
            like_count=like_count[0]
            if  "???" in like_count:
                like_count ="0"
            # print("????????? : ",like_count)

            repost_count=div.xpath(".//a[@action-type='feed_list_forward']/text()").extract()#?????????
            repost_count=repost_count[1]
            if  "??????" in repost_count :
                repost_count="0"
            # print("????????? : ",repost_count)
        
            orid=div.xpath(".//ul[@node-type='fl_menu_right']/li/a/@onclick").extract()#?????????  
            orid=orid[0]
            rule = re.compile(r"\d+")
            orid = rule.findall(orid)
            origin_weibo_id=orid[0]
            origin_user_id=orid[1]
            # print("??????mid : ",origin_weibo_id)
            # print("??????uid : ",origin_user_id)

            # print('--------------------------------   ------------------- --------------- --------------- --------------- --------------- \n')

            item['origin_weibo_id'] = origin_weibo_id  # ?????????id
            item['origin_user_id'] = origin_user_id  # ?????????id
            item['origin_weibo_content'] = origin_weibo_content.replace('\u200b', '')  # ?????????????????????
            item['publish_time'] = publish_time  # ????????????
            item['repost_count'] = repost_count  # ?????????
            item['like_count'] = like_count # ?????????
            yield item

            mid = origin_weibo_id
            repost_page = self.repost_ids_pages[mid] if mid in self.repost_ids_pages else 1
            repost_url = f'https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page={1}&moduleID=feed'
            yield Request(repost_url, callback=self.parse_repost, meta={'page_num': repost_page, 'mid': mid})
        next = response.xpath('//a[@class="next"]').extract()   
        if next:
            user_id, page_num = response.meta['user_id'], response.meta['page_num']
            page_num += 1
            url = f"https://s.weibo.com/weibo?q={user_id}&page={page_num}"
            # weibo????????????
            time.sleep(1)
            if self.max_page:  # max_page??????
                if page_num <= int(self.max_page):
                    self.user_ids_pages[user_id] = page_num
                    self.cache.set(self.SAVED_PAGE_KEY, self.user_ids_pages)
                    yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})
            else:  # ???????????????
                self.user_ids_pages[user_id] = page_num
                self.cache.set(self.SAVED_PAGE_KEY, self.user_ids_pages)
                yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})

            


    def parse_repost(self, response):
            self.logger.info('Parse function called on %s', response.url)
            data = json.loads(response.text)
            blocs = data['data']
            # print('????????????  ------------------- --------------- --------------- --------------- --------------- \n')
            for bloc in blocs:
                item = hot_search_parse_repost_bloc(bloc)
                yield item
                # ??????????????????????????? ?????????user??????
                user_id = str(bloc['user']['id'])
                # ??????user??????
                if not self.is_user_saved(user_id):
                    user_url = f'https://weibo.com/ajax/profile/info?uid={user_id}'
                    yield Request(user_url, callback=self.parse_user)
            # ?????????????????? ??????????????????????????????
            if len(blocs) > 0:
                mid, page_num = response.meta['mid'], response.meta['page_num']
                page_num += 1
                url = f"https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page={page_num}&moduleID=feed"
                if page_num <= 100:  # ??????????????????????????????
                    self.repost_ids_pages[mid] = page_num
                    self.cache.set(self.SAVED_REPOST_PAGE_KEY, self.repost_ids_pages)
                    yield Request(url, callback=self.parse_repost, meta={'mid': mid, 'page_num': page_num})

    def parse_user(self, response):
        self.logger.info('Parse function called on %s', response.url)
        data = json.loads(response.text)
        user_info = data['data']
        item = HotsearchUserInfoItem()
        item['user_id'] = str(user_info['user']['id'])  # ?????????id
        item['friends_count'] = str(user_info['user']['friends_count'])  # ?????????
        item['followers_count'] = str(user_info['user']['followers_count'])  # ?????????
        item['statuses_count'] = str(user_info['user']['statuses_count'])  # ?????????
        yield item                    
    
    def close(self, reason):
        # ?????????????????????????????????
        # mailer = MailSender(smtphost=private_setting.MAIL_HOST,
        #                     smtpport=private_setting.MAIL_PORT,
        #                     smtpuser=private_setting.MAIL_USER,
        #                     smtppass=private_setting.MAIL_PASS,
        #                     smtpssl=private_setting.MAIL_SSL,
        #                     smtptls=private_setting.MAIL_TLS,
        #                     mailfrom=private_setting.MAIL_FROM)
        # mailer.send(to=["2509875617@qq.com"], subject="Scrapy Pause", body="?????????cookie",
        #             cc=["2509875617@qq.com"])

        # ?????????????????????{userid : page} ????????????????????????page??????
        self.cache.set(self.SAVED_PAGE_KEY, self.user_ids_pages)
        self.cache.set(self.SAVED_REPOST_PAGE_KEY, self.repost_ids_pages)
        self.connect.close()    