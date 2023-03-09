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
        "cookie": "XSRF-TOKEN=f1ylOXkszg_AP0lHTUabtbob; PC_TOKEN=7a75513bfb; SUB=_2AkMTVcHXf8NxqwJRmP8dzGjgaIR3zwjEieKlCTAMJRMxHRl-yT92qmw9tRB6ONXvONBrvegUbIWoE_G9kQgjPgkYu5fj; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF4caSRdfd-0bgiPHBzp40y; login_sid_t=24c75056b75b94ec66e86887484de8cd; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; PPA_CI=8b3b7cf8cd9fcc8c6f3b6ef4b3aacdcb; _s_tentry=passport.weibo.com; Apache=3357902004956.5967.1678331617664; SINAGLOBAL=3357902004956.5967.1678331617664; ULV=1678331617668:1:1:1:3357902004956.5967.1678331617664:; wb_view_log=2560*14401; WBPSESS=5fStQf4aE0d6e7rh9d-P6iVkJJKQ7jNoHEp9VPgTJjpPVzxa0Znrfq9b7F84wp4U10i_ou9YxCDDhqxPMnt9tg0cpL_KHWDdn7dwXa-Z35RRP_EcluFRKtQ8aHGBcJjyFyrajr6Nwjvu4vkXn0fZ8AZSU1NNezX9dCxr_Hf0LtE="
    }
    cookies=["XSRF-TOKEN=f1ylOXkszg_AP0lHTUabtbob; PC_TOKEN=7a75513bfb; SUB=_2AkMTVcHXf8NxqwJRmP8dzGjgaIR3zwjEieKlCTAMJRMxHRl-yT92qmw9tRB6ONXvONBrvegUbIWoE_G9kQgjPgkYu5fj; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF4caSRdfd-0bgiPHBzp40y; login_sid_t=24c75056b75b94ec66e86887484de8cd; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; PPA_CI=8b3b7cf8cd9fcc8c6f3b6ef4b3aacdcb; _s_tentry=passport.weibo.com; Apache=3357902004956.5967.1678331617664; SINAGLOBAL=3357902004956.5967.1678331617664; ULV=1678331617668:1:1:1:3357902004956.5967.1678331617664:; wb_view_log=2560*14401; WBPSESS=5fStQf4aE0d6e7rh9d-P6iVkJJKQ7jNoHEp9VPgTJjpPVzxa0Znrfq9b7F84wp4U10i_ou9YxCDDhqxPMnt9tg0cpL_KHWDdn7dwXa-Z35RRP_EcluFRKtQ8aHGBcJjyFyrajr6Nwjvu4vkXn0fZ8AZSU1NNezX9dCxr_Hf0LtE=",
    "PPA_CI=87997b1a42cfaf82393e0ff425846864; _s_tentry=weibo.com; Apache=778240836238.1066.1678296824306; SINAGLOBAL=778240836238.1066.1678296824306; ULV=1678296824338:1:1:1:778240836238.1066.1678296824306:; SCF=Auboes_7CrdRZ4K6_J3TjCIKrFIZ0txQqXfRo_LZO0FTDqeUFz4M0yoJSbW2hJooMM60s9mFtb7DnPQ2NC_tr04.; SUB=_2A25JDLdXDeRhGeFG61cY8ynPzzuIHXVqe6-frDV8PUNbmtAGLUPSkW9Nfns5JYG4YvlJuHHFRLccdzuTRYDjYclX; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2cqyzWB5Y4.VnBuB4ySmB5JpX5KzhUgL.FoMReh-4e0M0ShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1h5f1KeNe0BN; ALF=1709832838; SSOLoginState=1678296839",
    "XSRF-TOKEN=jnxviBAnMg0gFt0k2o0sWrAa; SSOLoginState=1678346636; SUB=_2A25JDfncDeRhGeNH7FEZ8ijEwzWIHXVqe2wUrDV8PUNbmtAfLVjakW9NSp-OmY9q3wkkeZfUJO5j6ezIJAWtByVr; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFUhZPzXjKGWvmg4.wRlvEb5JpX5KzhUgL.Fo-4S0eReoqR1h.2dJLoIEBLxK.LBK-LB--LxKBLBonL12zLxK-LB.-L1h5LxKBLB.2L12zt; ALF=1709882634; WBPSESS=Kk2oDI_W7tKQzED2TYhnVKdxFxtvMbQwZcAgWXiQpKYFy4B7803YXQu1S9xgM1qtkqwfADEje8j3R76KD4eAX-ZQOQJKcmij56gLy1kjxocfPJZfbWbdhf-GoyMQR2PFHKegP8X0j-oRe4elWAVEUQ=="]
    count = 0

    def start_requests(self):
        uids = ['6239620007']
        start_urls = [f'{self.base_url}?uid={uid}' for uid in uids]
        for url in start_urls:
            yield Request(url, callback=self.parse, headers=self.headers, dont_filter=True)

    def parse(self, response):
        data = json.loads(response.text)
        ok = bool(data['ok'])
        if ok:
            print(data['data'])
            # 死循环测试
            time.sleep(0.05)
            self.count += 1
            if self.count <= 1500:  # 测试1500条
                self.headers["cookie"]=self.cookies[self.count%len(self.cookies)]
                yield Request(response.url, callback=self.parse, headers=self.headers, dont_filter=True)
        else:
            print(data)
            pass

        # bloc = data['data']
        # item = UserInfoItem()
        # item['user_id'] = str(bloc['user']['id'])  # 源微博id
        # item['friends_count'] = str(bloc['user']['friends_count'])  # 关注数
        # item['followers_count'] = str(bloc['user']['followers_count'])  # 粉丝数
        # item['statuses_count'] = str(bloc['user']['statuses_count'])  # 微博数
        # yield item
