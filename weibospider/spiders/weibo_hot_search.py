import time
import scrapy
import json
import pymysql
import re
import urllib.parse
from diskcache import Cache
from scrapy.http import Request
from weibospider.mytools.common import hot_search_parse_repost_bloc
from weibospider import private_setting
from weibospider.items import WeiboHotSearchItem, HotsearchUserInfoItem
from weibospider.mytools.common import parse_time
import csv
from itertools import islice
from weibospider.items import HotBandItem


# feature - 爬取某个搜索结果
# scrapy crawl weibo_hot_search -a max_page=5 -a reset_page=True
class WeiboHotSearchSpider(scrapy.Spider):
    name = 'weibo_hot_search'
    SAVED_PAGE_KEY = 'weibo_hot_search_downloaded_pages'
    SAVED_REPOST_PAGE_KEY = 'weibo_hot_search_repost_pages'
    start_urls = ['https://weibo.com/ajax/statuses/hot_band']

    # allowed_domains = ['s.weibo.com']

    # 1：#阳性感染者只咳嗽发烧算无症状吗#
    # 2：#二次感染新冠会更严重吗#
    # 3：#上班阳了算工伤吗#
    # key_words = [urllib.parse.quote('#阳性感染者只咳嗽发烧算无症状吗#')]

    def __init__(self, max_page=None, reset_page=True, *args, **kwargs):
        super(WeiboHotSearchSpider, self).__init__(*args, **kwargs)
        # 读取热搜csv
        # with open('hot_band.csv', 'r') as csvfile:
        #     reader = csv.reader(csvfile)
        #     keys = [row[2] for row in islice(reader, 1, None)]
        # self.max_page = max_page
        # self.cache = Cache(r"weibospider/disk")
        # self.key_words = [urllib.parse.quote(key) for key in keys]
        # if reset_page:
        #     self.cache.set(self.SAVED_PAGE_KEY, {key: 1 for key in self.key_words})
        # self.key_words_pages = self.cache.get(self.SAVED_PAGE_KEY, default={key: 1 for key in self.key_words})
        # self.key_words_pages = {key: 1 for key in self.key_words}
        # self.repost_ids_pages = self.cache.get(self.SAVED_REPOST_PAGE_KEY, default={})

        self.connect = pymysql.connect(
            host=private_setting.MYSQL_HOST,
            db=private_setting.MYSQL_DATABASE,
            user=private_setting.MYSQL_USERNAME,
            passwd=private_setting.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        self.cursor = self.connect.cursor()

    # def start_requests(self):
    #     yield scrapy.Request(start_urls, callback=self.parse)
        
        # for key in self.key_words:
        #     hot_search_url = f'https://s.weibo.com/weibo?q={key}&page={self.key_words_pages[key]}'
        #     yield scrapy.Request(hot_search_url, callback=self.parse,
        #                          meta={'user_id': key, 'page_num': self.key_words_pages[key]})

    def parse(self, response):
        data = json.loads(response.text)
        band_list = data['data']['band_list']
        for band in band_list:
            item = HotBandItem()
            if 'num' in band and 'onboard_time' in band and 'word_scheme' in band:
                item['num'] = band['num']
                item['onboard_time'] = band['onboard_time']
                item['word_scheme'] = band['word_scheme']
                key=band['word_scheme']
                key=urllib.parse.quote(key)
                hot_search_url = f'https://s.weibo.com/weibo?q={key}&page={1}'
                yield scrapy.Request(hot_search_url, callback=self.parse,
                                meta={'user_id': key, 'page_num': 1})

    # def is_user_saved(self, user_id):
    #     database = 'use weibo_datas;'
    #     sql = 'select * from user_info_hotsearch where user_id = %s'
    #     data = user_id
    #     self.cursor.execute(database)
    #     self.cursor.execute(sql, data)
    #     ret = self.cursor.fetchone()
    #     return ret is not None

    def parse(self, response, **kwargs):
        page_text = response.text
        # with open('first.html','w',encoding='utf-8') as fp:
        #     fp.write(page_text)
        div_list = response.xpath('//div[@id="pl_feedlist_index"]//div[@action-type="feed_list_item"]')
        for div in div_list:
            item = WeiboHotSearchItem()

            ttime = div.xpath(".//div[@class='from']/a[1]/text()").extract()
            ttime = ''.join(ttime)
            ttime = ttime.strip()
            # print("发布时间:", ttime)
            publish_time = parse_time(ttime)
            origin_weibo_content = div.xpath('.//p[@node-type="feed_list_content_full"]//text()').extract()  # 长文
            if origin_weibo_content:
                pass
            else:
                origin_weibo_content = div.xpath('.//p[@node-type="feed_list_content"]//text()').extract()  # 短文
            origin_weibo_content = ''.join(origin_weibo_content)
            origin_weibo_content = origin_weibo_content.strip()
            # print("内容 : ",origin_weibo_content)

            like = div.xpath(".//a[@action-type='feed_list_like']/em/text()").extract()  # 点赞数
            like_count = like if like else "0"
            # print("点赞数 : ",like_count)

            repost_count = div.xpath(".//a[@action-type='feed_list_forward']/text()").extract()  # 转发数
            count_list = re.compile(r"\d+").findall(str(repost_count))
            if len(count_list) == 0:
                repost_count = '0'
            else:
                repost_count = str(count_list[0])
            # print("转发数 : ",repost_count)

            origin_weibo_id = div.xpath('./@mid').extract()[0]
            # allowForward=1&mid=4856417351631314&name=玥X159&uid=2680492275.....
            orid = div.xpath(".//a[@action-type='feed_list_forward']/@action-data").extract()
            uid_list = re.compile(r"uid=(\d+)").findall(str(orid))
            if len(uid_list) == 0:
                origin_user_id = '-'
            else:
                origin_user_id = str(uid_list[0])
            # print("这是mid : ",origin_weibo_id)
            # print("这是uid : ",origin_user_id)

            # print('--------------------------------   ------------------- ---------------- \n')

            item['origin_weibo_id'] = origin_weibo_id  # 源微博id
            item['origin_user_id'] = origin_user_id  # 源用户id
            item['origin_weibo_content'] = origin_weibo_content.replace('\u200b', '')  # 源微博文本内容
            item['publish_time'] = publish_time  # 发布时间
            item['repost_count'] = repost_count  # 转发数
            item['like_count'] = like_count  # 点赞数
            yield item

            mid = origin_weibo_id
            # repost_page = self.repost_ids_pages[mid] if mid in self.repost_ids_pages else 1
            repost_page = 1
            repost_url = f'https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page={1}&moduleID=feed'
            yield Request(repost_url, callback=self.parse_repost, meta={'page_num': repost_page, 'mid': mid})
        # next = response.xpath('//a[@class="next"]').extract()
        # if next:
        user_id, page_num = response.meta['user_id'], response.meta['page_num']
        page_num += 1
        url = f"https://s.weibo.com/weibo?q={user_id}&page={page_num}"
        # weibo降低频率
        # time.sleep(0.25)
        if page_num <= 50:
            # self.key_words_pages[user_id] = page_num
            # self.cache.set(self.SAVED_PAGE_KEY, self.key_words_pages)
            yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})
            # else:  # 无限制请求
            #     self.key_words_pages[user_id] = page_num
            #     self.cache.set(self.SAVED_PAGE_KEY, self.key_words_pages)
            #     yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})

    def parse_repost(self, response):
        self.logger.info('Parse function called on %s', response.url)
        data = json.loads(response.text)
        blocs = data['data']
        print('转发测试  ------------------- --------------- --------------- --------------- --------------- \n')
        for bloc in blocs:
            item = hot_search_parse_repost_bloc(bloc)
            yield item
            # 对每一个转发的微博 请求其user信息
            user_id = str(bloc['user']['id'])
            # 请求user信息
            # if not self.is_user_saved(user_id):
            user_url = f'https://weibo.com/ajax/profile/info?uid={user_id}'
            yield Request(user_url, callback=self.parse_user)
        # 如果还有数据 就尝试请求下一页数据
        if len(blocs) > 0:
            mid, page_num = response.meta['mid'], response.meta['page_num']
            page_num += 1
            url = f"https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page={page_num}&moduleID=feed"
            if page_num <= 5000:  # 转发推文请求限制页数 每页大概有20个数据
                # self.repost_ids_pages[mid] = page_num
                # self.cache.set(self.SAVED_REPOST_PAGE_KEY, self.repost_ids_pages)
                yield Request(url, callback=self.parse_repost, meta={'mid': mid, 'page_num': page_num})

    def parse_user(self, response):
        self.logger.info('Parse function called on %s', response.url)
        data = json.loads(response.text)
        user_info = data['data']
        item = HotsearchUserInfoItem()
        item['user_id'] = str(user_info['user']['id'])  # 源微博id
        item['friends_count'] = str(user_info['user']['friends_count'])  # 关注数
        item['followers_count'] = str(user_info['user']['followers_count'])  # 粉丝数
        item['statuses_count'] = str(user_info['user']['statuses_count'])  # 微博数
        yield item

    def close(self, reason):
        # 爬虫停止则发送邮件通知
        # mailer = MailSender(smtphost=private_setting.MAIL_HOST,
        #                     smtpport=private_setting.MAIL_PORT,
        #                     smtpuser=private_setting.MAIL_USER,
        #                     smtppass=private_setting.MAIL_PASS,
        #                     smtpssl=private_setting.MAIL_SSL,
        #                     smtptls=private_setting.MAIL_TLS,
        #                     mailfrom=private_setting.MAIL_FROM)
        # mailer.send(to=["2509875617@qq.com"], subject="Scrapy Pause", body="请更新cookie",
        #             cc=["2509875617@qq.com"])

        # 同时记录当前的{userid : page} 下次启动入口时从page开始
        # self.cache.set(self.SAVED_PAGE_KEY, self.key_words_pages)
        # self.cache.set(self.SAVED_REPOST_PAGE_KEY, self.repost_ids_pages)
        self.connect.close()
