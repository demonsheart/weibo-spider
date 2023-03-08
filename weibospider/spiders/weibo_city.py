# https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=1&group_id=1028032222&containerid=102803_2222&extparam=discover%7Cnew_feed&max_id=0&count=10
# https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=1&group_id=1028032222&containerid=102803_2222&extparam=discover%7Cnew_feed&max_id=0&count=10
# https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=1028032222&containerid=102803_2222&extparam=discover%7Cnew_feed&max_id=2_-_m_-___-_1_-_8008644050000000000_-__-_1_-__-_1_-_a_56_49_-__-__-_0&count=10
# https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=1028032222&containerid=102803_2222&extparam=discover%7Cnew_feed&max_id=3_-_m_-___-_1_-_8008644050000000000_-__-_1_-__-_1_-_a_56_49_-__-__-_0&count=10
# https://weibo.com/ajax/feed/hottimeline?refresh=2&group_id=1028032222&containerid=102803_2222&extparam=discover%7Cnew_feed&max_id=4_-_m_-___-_1_-_8008644050000000000_-__-_1_-__-_1_-_a_56_49_-__-__-_0&count=10
# https://weibo.com/ajax/statuses/buildComments?is_reload=1&id=4869902765131454&is_show_bulletin=2&is_mix=0&count=20&type=feed&uid=5748965292
# https://weibo.com/ajax/statuses/repostTimeline?id=4866323853084327&page=1&moduleID=feed&type=feed
# https://d.weibo.com/102803_2222_oid_8008644050000000000_name_%E6%B1%95%E5%A4%B4#
import time
import scrapy
import json
import pymysql

from diskcache import Cache
from scrapy.http import Request
from weibospider.items import CityUserInfoItem
from weibospider.mytools.common import city_parse_bloc, parse_long_bloc, city_parse_repost_bloc
from weibospider import private_setting
from scrapy.mail import MailSender


# scrapy crawl origin_weibo -a max_page=5 -a reset_page=True
class OriginWeiboSpider(scrapy.Spider):
    name = 'weibo_city'
    # allowed_domains = ['weibo.com']
    base_url = "https://weibo.com"  # 微博的接口
    connect = None
    cursor = None
    user_ids = ['102803_2222']  # 汕头的cityid
    SAVED_PAGE_KEY = 'weibo__city_downloaded_pages'
    SAVED_REPOST_PAGE_KEY = 'weibo__city_repost_pages'

    def __init__(self, max_page=1000, reset_page=True, *args, **kwargs):
        super(OriginWeiboSpider, self).__init__(*args, **kwargs)
        self.max_page = max_page

        # TODO 目前是通过项目的disk下的db缓存当前的page_num 这需要每次都更新本地的disk 这里可以使用云redis优化
        # 根据cache初始化user_ids_pages 从上一次失败的page开始爬起
        self.cache = Cache(r"weibospider/disk")
        if reset_page:
            self.cache.set(self.SAVED_PAGE_KEY, {key: 1 for key in self.user_ids})
        self.user_ids_pages = self.cache.get(self.SAVED_PAGE_KEY, default={key: 1 for key in self.user_ids})
        self.repost_ids_pages = self.cache.get(self.SAVED_REPOST_PAGE_KEY, default={})
        self.open_connect()

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
        sql = 'select * from user_info_city where user_id = %s'
        data = user_id
        self.cursor.execute(database)
        self.cursor.execute(sql, data)
        ret = self.cursor.fetchone()
        return ret is not None

    def start_requests(self):
        # 这里user_ids可替换成实际待采集的数据
        for user_id in self.user_ids:
            # 请求user信息
            # if not self.is_user_saved(user_id):
            #     user_url = f'https://weibo.com/ajax/profile/info?uid={user_id}'
            #     yield Request(user_url, callback=self.parse_user)
            # 请求 weibo正文
            url = f"https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=1&group_id=1028032222&containerid={user_id}&extparam=discover%7Cnew_feed&max_id={0}&count=10"
# https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=1&group_id=1028032222&containerid=102803_2222&extparam=discover%7Cnew_feed&max_id=0&count=10
            yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': 0})

    def parse(self, response, **kwargs):
        self.logger.info('Parse function called on %s', response.url)
        data = json.loads(response.text)
        blocs = data['statuses']
        for bloc in blocs:
            item = city_parse_bloc(bloc)
            # 长文的正文需要另外请求处理
            # if bloc["isLongText"]:
            #     url = "https://weibo.com/ajax/statuses/longtext?id=" + bloc['mblogid']
            #     print(item)
            #     print("\n\n")
            #     yield Request(url, callback=parse_long_bloc, meta={'item': item})
            # else:
            yield item
            # 对每一条微博 请求转发它的微博 为了简化 每次从第一页开始请求
            # 必须也得缓存当前的page 因为有的微博转发数量也很大 当cookie挂了重新爬取的时候 需要恢复现场
            mid = str(bloc['mid'])
            repost_page =  1

            repost_url = f'https://weibo.com/ajax/statuses/repostTimeline?page={repost_page}&moduleID=feed&id={mid}'
            yield Request(repost_url, callback=self.parse_repost, meta={'page_num': repost_page, 'mid': mid})

        # 如果还有数据 就尝试请求下一页数据
        if len(blocs) > 0:
            user_id, page_num = response.meta['user_id'], response.meta['page_num']
            page_num += 1
            url = f"https://weibo.com/ajax/feed/hottimeline?since_id=0&refresh=1&group_id=1028032222&containerid={user_id}&extparam=discover%7Cnew_feed&max_id={page_num}&count=10"
            
            # weibo降低频率
            time.sleep(1)
            if self.max_page:  # max_page限制
                if page_num <= int(self.max_page):
                    self.user_ids_pages[user_id] = page_num
                    self.cache.set(self.SAVED_PAGE_KEY, self.user_ids_pages)
                    yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})
            else:  # 无限制请求
                self.user_ids_pages[user_id] = page_num
                self.cache.set(self.SAVED_PAGE_KEY, self.user_ids_pages)
                yield Request(url, callback=self.parse, meta={'user_id': user_id, 'page_num': page_num})

    def parse_user(self, response):
        self.logger.info('Parse function called on %s', response.url)
        data = json.loads(response.text)
        user_info = data['data']
        item = CityUserInfoItem()
        item['user_id'] = str(user_info['user']['id'])  # 源微博id
        item['friends_count'] = str(user_info['user']['friends_count'])  # 关注数
        item['followers_count'] = str(user_info['user']['followers_count'])  # 粉丝数
        item['statuses_count'] = str(user_info['user']['statuses_count'])  # 微博数
        yield item

    def parse_repost(self, response):
        self.logger.info('Parse function called on %s', response.url)
        data = json.loads(response.text)
        blocs = data['data']
        for bloc in blocs:
            item = city_parse_repost_bloc(bloc)
            yield item
            # 对每一个转发的微博 请求其user信息
            user_id = str(bloc['user']['id'])
            # 请求user信息
            if not self.is_user_saved(user_id):
                user_url = f'https://weibo.com/ajax/profile/info?uid={user_id}'
                yield Request(user_url, callback=self.parse_user)
        # 如果还有数据 就尝试请求下一页数据
        if len(blocs) > 0:
            mid, page_num = response.meta['mid'], response.meta['page_num']
            page_num += 1
            url = f"https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page={page_num}&moduleID=feed&type=feed"
            # https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page={page_num}&moduleID=feed&type=feed
            if page_num <= 2000:  # 转发推文请求限制页数
                self.repost_ids_pages[mid] = page_num
                self.cache.set(self.SAVED_REPOST_PAGE_KEY, self.repost_ids_pages)
                yield Request(url, callback=self.parse_repost, meta={'mid': mid, 'page_num': page_num})

    def close(self, reason):
        # # 爬虫停止则发送邮件通知
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
        self.cache.set(self.SAVED_PAGE_KEY, self.user_ids_pages)
        self.cache.set(self.SAVED_REPOST_PAGE_KEY, self.repost_ids_pages)
        self.connect.close()
