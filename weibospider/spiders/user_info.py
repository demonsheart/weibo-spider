import scrapy
import json
from scrapy.http import Request
from weibospider.items import UserInfoItem
import time


class UserInfoSpider(scrapy.Spider):
    name = 'user_info'
    # allowed_domains = ['weibo.com']

    base_url = "https://weibo.com/ajax/profile/info"  # 微博的接口
    # https://weibo.com/ajax/profile/info?uid=6239439310

    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0",
        "referer": "https://weibo.com",
    }
    cookies = [
        'XSRF-TOKEN=_FFO4YhiMmUtzHRNDzPezDbM; PC_TOKEN=5a5fccc4f3; login_sid_t=365e4ca48859984ff9ad828ed9be8544; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; PPA_CI=d0daeaa2f9f6a0cfea8bc665a83e9749; SCF=Auboes_7CrdRZ4K6_J3TjCIKrFIZ0txQqXfRo_LZO0FThdO7yesdOake1aOnvBjQzzkwe2MJITShpHUbGL1weC0.; SUB=_2A25JDmdKDeRhGeNH4lEW9inNzziIHXVqet-CrDV8PUNbmtAGLVL7kW9NSnAePV42zsfDqdztxi3aEDjyKadc43df; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF.sG7_X0HX15pY5xDmTs5A5JpX5KzhUgL.Fo-41KeNSoMpShB2dJLoI0YLxKMLB.eL1KnLxKML1KBL1-qLxKMLB.eL1KnLxKML1h2LB-BLxKMLB.eL1KnLxK-LBo5LB.BLxKqL1K-LBKet; ALF=1709918874; SSOLoginState=1678382874; WBPSESS=kTzxXaFYfeELPFRjS_d8EHEAFHiaqY-3K1QrxDD54Yaq1jmuQ4auYnjWbn2d4uBI0F_kC7PNtN4-roHL5ORtoza0Y3RseceRMj2Vlqo3bIo1zZFB6lOS21pdbonLxaHSvizZMrhXpwr6mxJwQ8jj6w==',
        'XSRF-TOKEN=_FFO4YhiMmUtzHRNDzPezDbM; PC_TOKEN=5a5fccc4f3; login_sid_t=365e4ca48859984ff9ad828ed9be8544; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; PPA_CI=d0daeaa2f9f6a0cfea8bc665a83e9749; SCF=Auboes_7CrdRZ4K6_J3TjCIKrFIZ0txQqXfRo_LZO0FThdO7yesdOake1aOnvBjQzzkwe2MJITShpHUbGL1weC0.; SUB=_2A25JDmdKDeRhGeNH4lEW9inNzziIHXVqet-CrDV8PUNbmtAGLVL7kW9NSnAePV42zsfDqdztxi3aEDjyKadc43df; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF.sG7_X0HX15pY5xDmTs5A5JpX5KzhUgL.Fo-41KeNSoMpShB2dJLoI0YLxKMLB.eL1KnLxKML1KBL1-qLxKMLB.eL1KnLxKML1h2LB-BLxKMLB.eL1KnLxK-LBo5LB.BLxKqL1K-LBKet; ALF=1709918874; SSOLoginState=1678382874; WBPSESS=kTzxXaFYfeELPFRjS_d8EHEAFHiaqY-3K1QrxDD54YbWabiABdSktEHqEYA6uVy6hus1LwLBNPYmfxk_9-3f2MRep38z2Ff5zqE_RKSXd0ReMzhGGpdYkxzl00k-bVPfcnquHn4nlbq9PYGr9F2m1w==',
        'XSRF-TOKEN=l0KmKUrqlCdVfCH_p5Ocyrae; PC_TOKEN=fae474401d; login_sid_t=e3716e00e7d8da9e1727b104b7345aba; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; _s_tentry=passport.weibo.com; Apache=9506464120689.297.1678383053107; SINAGLOBAL=9506464120689.297.1678383053107; ULV=1678383053110:1:1:1:9506464120689.297.1678383053107:; wb_view_log=1512*9822; SUB=_2A25JDme6DeRhGeFG61cY8ynPzzuIHXVqet5yrDV8PUNbmtANLVPYkW9Nfns5JT8mIVf-lCnecrHLrgVubGrTkMLp; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2cqyzWB5Y4.VnBuB4ySmB5JpX5KzhUgL.FoMReh-4e0M0ShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1h5f1KeNe0BN; ALF=1709919081; SSOLoginState=1678383082; WBPSESS=RG7REZfowQtB4h7VOHh181o8rYucmnnCQpbrRryYKBrL6gewegjYIlJbLr70G-Ul7er5RBPOL5wdKSJ0_HLIqCdDpY7MnwZ2Dg7hgP854A1qs1JBtu0SA414Dw16KUAyTJs5R8niQNRfj6steW1u3A==',
        'XSRF-TOKEN=l0KmKUrqlCdVfCH_p5Ocyrae; PC_TOKEN=fae474401d; login_sid_t=e3716e00e7d8da9e1727b104b7345aba; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; _s_tentry=passport.weibo.com; Apache=9506464120689.297.1678383053107; SINAGLOBAL=9506464120689.297.1678383053107; ULV=1678383053110:1:1:1:9506464120689.297.1678383053107:; wb_view_log=1512*9822; SUB=_2A25JDme6DeRhGeFG61cY8ynPzzuIHXVqet5yrDV8PUNbmtANLVPYkW9Nfns5JT8mIVf-lCnecrHLrgVubGrTkMLp; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2cqyzWB5Y4.VnBuB4ySmB5JpX5KzhUgL.FoMReh-4e0M0ShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1h5f1KeNe0BN; ALF=1709919081; SSOLoginState=1678383082; WBPSESS=RG7REZfowQtB4h7VOHh181o8rYucmnnCQpbrRryYKBrUXXf6XXjjxswMFrC4EAjVMtwAk0JEfTTARDTrPSROI9LLmbOY3oCs7NgF6EsUMrtMYTfqbzFhn5xV78y3swOdVoKjXN7L1jkPBpYee-PfZg==',
        'XSRF-TOKEN=l0KmKUrqlCdVfCH_p5Ocyrae; PC_TOKEN=fae474401d; login_sid_t=e3716e00e7d8da9e1727b104b7345aba; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; _s_tentry=passport.weibo.com; Apache=9506464120689.297.1678383053107; SINAGLOBAL=9506464120689.297.1678383053107; ULV=1678383053110:1:1:1:9506464120689.297.1678383053107:; wb_view_log=1512*9822; SUB=_2A25JDme6DeRhGeFG61cY8ynPzzuIHXVqet5yrDV8PUNbmtANLVPYkW9Nfns5JT8mIVf-lCnecrHLrgVubGrTkMLp; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2cqyzWB5Y4.VnBuB4ySmB5JpX5KzhUgL.FoMReh-4e0M0ShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1h5f1KeNe0BN; ALF=1709919081; SSOLoginState=1678383082; WBPSESS=RG7REZfowQtB4h7VOHh181o8rYucmnnCQpbrRryYKBrUXXf6XXjjxswMFrC4EAjVatvxqg0Hb_YZcE02Ecyih9nCfAj3ahboWhwNboPEZYzsl-G-At2T7l2eesro3YFd7t7DqX4fOHRwZ7mgdw-l0g=='
    ]
    count = 0

    def __init__(self, *args, **kwargs):
        super(UserInfoSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        uids = ['6239620007'] * 1000  # 生成1000条
        start_urls = [f'{self.base_url}?uid={uid}' for uid in uids]
        for url in start_urls:
            # time.sleep(0.2)  # 提交延迟 实测最小值0.2 再小会414
            self.count += 1
            cookie_idx = self.count % len(self.cookies)
            self.headers["cookie"] = self.cookies[cookie_idx]

            # 使用本机代理
            # cur_ip = f'http://127.0.0.1:7890'
            # yield Request(url, callback=self.parse, headers=self.headers, dont_filter=True, meta={'proxy': cur_ip})

            # 默认走通过全局代理
            yield Request(url, callback=self.parse, headers=self.headers, dont_filter=True)

    def parse(self, response):
        data = json.loads(response.text)
        ok = bool(data['ok'])
        if ok:
            print(data['data'])
            bloc = data['data']
            item = UserInfoItem()
            item['user_id'] = str(bloc['user']['id'])  # 源微博id
            item['friends_count'] = str(bloc['user']['friends_count'])  # 关注数
            item['followers_count'] = str(bloc['user']['followers_count'])  # 粉丝数
            item['statuses_count'] = str(bloc['user']['statuses_count'])  # 微博数
            yield item
        else:
            print(data)
            pass
