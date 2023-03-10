import random

import scrapy
import json
import re
import urllib.parse
import copy
from scrapy.http import Request
from weibospider.mytools.common import hot_search_parse_repost_bloc
from weibospider.items import WeiboHotSearchItem, HotsearchUserInfoItem
from weibospider.mytools.common import parse_time


# feature - 爬取某个搜索结果
# scrapy crawl weibo_hot_search
class WeiboHotSearchSpider(scrapy.Spider):
    name = 'weibo_hot_search'
    start_urls = ['https://weibo.com/ajax/statuses/hot_band']

    # allowed_domains = ['s.weibo.com']

    base_headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0",
        "referer": "https://weibo.com",
    }

    # weibo与user需要cookie repost则不需要
    cookies = [
        'XSRF-TOKEN=_FFO4YhiMmUtzHRNDzPezDbM; PC_TOKEN=5a5fccc4f3; login_sid_t=365e4ca48859984ff9ad828ed9be8544; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; PPA_CI=d0daeaa2f9f6a0cfea8bc665a83e9749; SCF=Auboes_7CrdRZ4K6_J3TjCIKrFIZ0txQqXfRo_LZO0FThdO7yesdOake1aOnvBjQzzkwe2MJITShpHUbGL1weC0.; SUB=_2A25JDmdKDeRhGeNH4lEW9inNzziIHXVqet-CrDV8PUNbmtAGLVL7kW9NSnAePV42zsfDqdztxi3aEDjyKadc43df; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF.sG7_X0HX15pY5xDmTs5A5JpX5KzhUgL.Fo-41KeNSoMpShB2dJLoI0YLxKMLB.eL1KnLxKML1KBL1-qLxKMLB.eL1KnLxKML1h2LB-BLxKMLB.eL1KnLxK-LBo5LB.BLxKqL1K-LBKet; ALF=1709918874; SSOLoginState=1678382874; WBPSESS=kTzxXaFYfeELPFRjS_d8EHEAFHiaqY-3K1QrxDD54Yaq1jmuQ4auYnjWbn2d4uBI0F_kC7PNtN4-roHL5ORtoza0Y3RseceRMj2Vlqo3bIo1zZFB6lOS21pdbonLxaHSvizZMrhXpwr6mxJwQ8jj6w==',
        'XSRF-TOKEN=_FFO4YhiMmUtzHRNDzPezDbM; PC_TOKEN=5a5fccc4f3; login_sid_t=365e4ca48859984ff9ad828ed9be8544; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; PPA_CI=d0daeaa2f9f6a0cfea8bc665a83e9749; SCF=Auboes_7CrdRZ4K6_J3TjCIKrFIZ0txQqXfRo_LZO0FThdO7yesdOake1aOnvBjQzzkwe2MJITShpHUbGL1weC0.; SUB=_2A25JDmdKDeRhGeNH4lEW9inNzziIHXVqet-CrDV8PUNbmtAGLVL7kW9NSnAePV42zsfDqdztxi3aEDjyKadc43df; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF.sG7_X0HX15pY5xDmTs5A5JpX5KzhUgL.Fo-41KeNSoMpShB2dJLoI0YLxKMLB.eL1KnLxKML1KBL1-qLxKMLB.eL1KnLxKML1h2LB-BLxKMLB.eL1KnLxK-LBo5LB.BLxKqL1K-LBKet; ALF=1709918874; SSOLoginState=1678382874; WBPSESS=kTzxXaFYfeELPFRjS_d8EHEAFHiaqY-3K1QrxDD54YbWabiABdSktEHqEYA6uVy6hus1LwLBNPYmfxk_9-3f2MRep38z2Ff5zqE_RKSXd0ReMzhGGpdYkxzl00k-bVPfcnquHn4nlbq9PYGr9F2m1w==',
        'XSRF-TOKEN=l0KmKUrqlCdVfCH_p5Ocyrae; PC_TOKEN=fae474401d; login_sid_t=e3716e00e7d8da9e1727b104b7345aba; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; _s_tentry=passport.weibo.com; Apache=9506464120689.297.1678383053107; SINAGLOBAL=9506464120689.297.1678383053107; ULV=1678383053110:1:1:1:9506464120689.297.1678383053107:; wb_view_log=1512*9822; SUB=_2A25JDme6DeRhGeFG61cY8ynPzzuIHXVqet5yrDV8PUNbmtANLVPYkW9Nfns5JT8mIVf-lCnecrHLrgVubGrTkMLp; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2cqyzWB5Y4.VnBuB4ySmB5JpX5KzhUgL.FoMReh-4e0M0ShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1h5f1KeNe0BN; ALF=1709919081; SSOLoginState=1678383082; WBPSESS=RG7REZfowQtB4h7VOHh181o8rYucmnnCQpbrRryYKBrL6gewegjYIlJbLr70G-Ul7er5RBPOL5wdKSJ0_HLIqCdDpY7MnwZ2Dg7hgP854A1qs1JBtu0SA414Dw16KUAyTJs5R8niQNRfj6steW1u3A==',
        'XSRF-TOKEN=l0KmKUrqlCdVfCH_p5Ocyrae; PC_TOKEN=fae474401d; login_sid_t=e3716e00e7d8da9e1727b104b7345aba; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; _s_tentry=passport.weibo.com; Apache=9506464120689.297.1678383053107; SINAGLOBAL=9506464120689.297.1678383053107; ULV=1678383053110:1:1:1:9506464120689.297.1678383053107:; wb_view_log=1512*9822; SUB=_2A25JDme6DeRhGeFG61cY8ynPzzuIHXVqet5yrDV8PUNbmtANLVPYkW9Nfns5JT8mIVf-lCnecrHLrgVubGrTkMLp; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2cqyzWB5Y4.VnBuB4ySmB5JpX5KzhUgL.FoMReh-4e0M0ShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1h5f1KeNe0BN; ALF=1709919081; SSOLoginState=1678383082; WBPSESS=RG7REZfowQtB4h7VOHh181o8rYucmnnCQpbrRryYKBrUXXf6XXjjxswMFrC4EAjVMtwAk0JEfTTARDTrPSROI9LLmbOY3oCs7NgF6EsUMrtMYTfqbzFhn5xV78y3swOdVoKjXN7L1jkPBpYee-PfZg==',
        'XSRF-TOKEN=l0KmKUrqlCdVfCH_p5Ocyrae; PC_TOKEN=fae474401d; login_sid_t=e3716e00e7d8da9e1727b104b7345aba; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; _s_tentry=passport.weibo.com; Apache=9506464120689.297.1678383053107; SINAGLOBAL=9506464120689.297.1678383053107; ULV=1678383053110:1:1:1:9506464120689.297.1678383053107:; wb_view_log=1512*9822; SUB=_2A25JDme6DeRhGeFG61cY8ynPzzuIHXVqet5yrDV8PUNbmtANLVPYkW9Nfns5JT8mIVf-lCnecrHLrgVubGrTkMLp; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2cqyzWB5Y4.VnBuB4ySmB5JpX5KzhUgL.FoMReh-4e0M0ShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1h5f1KeNe0BN; ALF=1709919081; SSOLoginState=1678383082; WBPSESS=RG7REZfowQtB4h7VOHh181o8rYucmnnCQpbrRryYKBrUXXf6XXjjxswMFrC4EAjVatvxqg0Hb_YZcE02Ecyih9nCfAj3ahboWhwNboPEZYzsl-G-At2T7l2eesro3YFd7t7DqX4fOHRwZ7mgdw-l0g=='
    ]
    user_count = 0

    def __init__(self, *args, **kwargs):
        super(WeiboHotSearchSpider, self).__init__(*args, **kwargs)

    # def start_requests(self):
    #     yield scrapy.Request(start_urls, callback=self.parse)

    # for key in self.key_words:
    #     hot_search_url = f'https://s.weibo.com/weibo?q={key}&page={self.key_words_pages[key]}'
    #     yield scrapy.Request(hot_search_url, callback=self.parse,
    #                          meta={'user_id': key, 'page_num': self.key_words_pages[key]})

    # weibo与user使用cookie池
    def generate_cookie_header(self):
        headers = copy.deepcopy(self.base_headers)
        headers['cookie'] = random.choice(self.cookies)
        return headers

    def parse(self, response):
        data = json.loads(response.text)
        band_list = data['data']['band_list']
        for band in band_list:
            if 'word_scheme' in band:
                key = urllib.parse.quote(band['word_scheme'])
                hot_search_url = f'https://s.weibo.com/weibo?q={key}&page={1}'
                yield scrapy.Request(hot_search_url, callback=self.parse_origin, headers=self.generate_cookie_header(),
                                     meta={'user_id': key, 'page_num': 1})

    def parse_origin(self, response):
        # page_text = response.text
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

            # 对每一个源微博 请求user信息
            user_url = f'https://weibo.com/ajax/profile/info?uid={origin_user_id}'
            yield Request(user_url, headers=self.generate_cookie_header(), callback=self.parse_user)

            # 提交转发队列
            mid = origin_weibo_id
            repost_url = f'https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page={1}&moduleID=feed'
            yield Request(repost_url, callback=self.parse_repost, meta={'page_num': 1, 'mid': mid})

        user_id, page_num = response.meta['user_id'], response.meta['page_num']
        page_num += 1
        url = f"https://s.weibo.com/weibo?q={user_id}&page={page_num}"
        # weibo降低频率
        # time.sleep(0.25)
        if page_num <= 50:
            yield Request(url, callback=self.parse_origin, headers=self.generate_cookie_header(),
                          meta={'user_id': user_id, 'page_num': page_num})

    def parse_repost(self, response):
        self.logger.info('Parse function called on %s', response.url)
        data = json.loads(response.text)
        blocs = data['data']
        print('转发测试  ------------------- --------------- --------------- --------------- --------------- \n')
        for bloc in blocs:
            item = hot_search_parse_repost_bloc(bloc)
            yield item
            # 对每一个转发的微博 请求转发者的user信息
            user_id = str(bloc['user']['id'])
            user_url = f'https://weibo.com/ajax/profile/info?uid={user_id}'
            yield Request(user_url, headers=self.generate_cookie_header(), callback=self.parse_user)
        # 如果还有数据 就尝试请求下一页数据
        if len(blocs) > 0:
            mid, page_num = response.meta['mid'], response.meta['page_num']
            page_num += 1
            url = f"https://weibo.com/ajax/statuses/repostTimeline?id={mid}&page={page_num}&moduleID=feed"
            if page_num <= 5000:  # 转发推文请求限制页数 每页大概有20个数据
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
        pass
