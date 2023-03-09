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
    }
    cookies = [
        "XSRF-TOKEN=f1ylOXkszg_AP0lHTUabtbob; SUB=_2AkMTVcHXf8NxqwJRmP8dzGjgaIR3zwjEieKlCTAMJRMxHRl-yT92qmw9tRB6ONXvONBrvegUbIWoE_G9kQgjPgkYu5fj; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WF4caSRdfd-0bgiPHBzp40y; login_sid_t=24c75056b75b94ec66e86887484de8cd; cross_origin_proto=SSL; PPA_CI=8b3b7cf8cd9fcc8c6f3b6ef4b3aacdcb; _s_tentry=passport.weibo.com; Apache=3357902004956.5967.1678331617664; SINAGLOBAL=3357902004956.5967.1678331617664; ULV=1678331617668:1:1:1:3357902004956.5967.1678331617664:; wb_view_log=2560*14401; WBPSESS=5fStQf4aE0d6e7rh9d-P6iVkJJKQ7jNoHEp9VPgTJjpPVzxa0Znrfq9b7F84wp4U10i_ou9YxCDDhqxPMnt9tg0cpL_KHWDdn7dwXa-Z35RRP_EcluFRKtQ8aHGBcJjyFyrajr6Nwjvu4vkXn0fZ8AZSU1NNezX9dCxr_Hf0LtE=",
        "XSRF-TOKEN=f1ylOXkszg_AP0lHTUabtbob; login_sid_t=24c75056b75b94ec66e86887484de8cd; cross_origin_proto=SSL; PPA_CI=8b3b7cf8cd9fcc8c6f3b6ef4b3aacdcb; _s_tentry=passport.weibo.com; Apache=3357902004956.5967.1678331617664; SINAGLOBAL=3357902004956.5967.1678331617664; ULV=1678331617668:1:1:1:3357902004956.5967.1678331617664:; wb_view_log=2560*14401; SCF=Auboes_7CrdRZ4K6_J3TjCIKrFIZ0txQqXfRo_LZO0FTNcYX7yMRl_iZvcDcM7Ee48SGdZ6HURx1Ri1xsy7OsYo.; SUB=_2A25JDYgxDeRhGeFG61cY8ynPzzuIHXVqev75rDV8PUNbmtAfLWSkkW9Nfns5JRkb5dfOeGQUMOkgmx0lU-dnfT6n; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2cqyzWB5Y4.VnBuB4ySmB5JpX5KzhUgL.FoMReh-4e0M0ShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1h5f1KeNe0BN; ALF=1709911009; SSOLoginState=1678375009; WBPSESS=RG7REZfowQtB4h7VOHh181o8rYucmnnCQpbrRryYKBrL6gewegjYIlJbLr70G-Uly49vjzto_muyf6BswiEeyud_k_piH6YVKHyoStm3UaEIuf55FWb_UEjf2NV41VuNpKTr0z4AxWuMce3dCcBCWw==",
        "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFUhZPzXjKGWvmg4.wRlvEb5JpX5KMhUgL.Fo-4S0eReoqR1h.2dJLoIEBLxK.LBK-LB--LxKBLBonL12zLxK-LB.-L1h5LxKBLB.2L12zt; ALF=1680961538; SSOLoginState=1678369539; SCF=ApTiNa_W18ZQ_g0ULOsgHW5zl4VsHr4Oq4JxhFwIWOsMckiqNHApB6Xzmixqoe8lhMXNFagIljHlmB4GT_DyDns.; SUB=_2A25JDZNUDeRhGeNH7FEZ8ijEwzWIHXVqeoOcrDV8PUNbmtAfLVHQkW9NSp-OmSTS7E5KCigDX1tFpDECa6VhlkVS; XSRF-TOKEN=cJUloUmXVJszhTVOkUXz1Oz3; WBPSESS=Kk2oDI_W7tKQzED2TYhnVKdxFxtvMbQwZcAgWXiQpKYFy4B7803YXQu1S9xgM1qt9J0QVYQpYVMwcUWAgg83VBb9ADzMWfVzEYxpJ62TJeNpkm8Q6etCQXc_NV9AMPr1Jzq-uoFnM7-BbwctcuuLpw==",
        "SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFUhZPzXjKGWvmg4.wRlvEb5JpX5KMhUgL.Fo-4S0eReoqR1h.2dJLoIEBLxK.LBK-LB--LxKBLBonL12zLxK-LB.-L1h5LxKBLB.2L12zt; ALF=1680961538; SSOLoginState=1678369539; SCF=ApTiNa_W18ZQ_g0ULOsgHW5zl4VsHr4Oq4JxhFwIWOsMckiqNHApB6Xzmixqoe8lhMXNFagIljHlmB4GT_DyDns.; SUB=_2A25JDZNUDeRhGeNH7FEZ8ijEwzWIHXVqeoOcrDV8PUNbmtAfLVHQkW9NSp-OmSTS7E5KCigDX1tFpDECa6VhlkVS; _s_tentry=-; Apache=2606992518245.235.1678374876720; SINAGLOBAL=2606992518245.235.1678374876720; ULV=1678374876725:1:1:1:2606992518245.235.1678374876720:",
        "XSRF-TOKEN=f1ylOXkszg_AP0lHTUabtbob; login_sid_t=24c75056b75b94ec66e86887484de8cd; cross_origin_proto=SSL; PPA_CI=8b3b7cf8cd9fcc8c6f3b6ef4b3aacdcb; _s_tentry=passport.weibo.com; Apache=3357902004956.5967.1678331617664; SINAGLOBAL=3357902004956.5967.1678331617664; ULV=1678331617668:1:1:1:3357902004956.5967.1678331617664:; wb_view_log=2560*14401; SCF=Auboes_7CrdRZ4K6_J3TjCIKrFIZ0txQqXfRo_LZO0FTNcYX7yMRl_iZvcDcM7Ee48SGdZ6HURx1Ri1xsy7OsYo.; SUB=_2A25JDYgxDeRhGeFG61cY8ynPzzuIHXVqev75rDV8PUNbmtAfLWSkkW9Nfns5JRkb5dfOeGQUMOkgmx0lU-dnfT6n; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh2cqyzWB5Y4.VnBuB4ySmB5JpX5KzhUgL.FoMReh-4e0M0ShM2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMN1h5f1KeNe0BN; ALF=1709911009; SSOLoginState=1678375009; PC_TOKEN=a9180fd2b0; WBStorage=4d96c54e|undefined; WBPSESS=RG7REZfowQtB4h7VOHh181o8rYucmnnCQpbrRryYKBrUXXf6XXjjxswMFrC4EAjVMtwAk0JEfTTARDTrPSROI3LIb4PgHTNN7jJ8IRJEnt1F94H3FnGeIEDDAIRUOHXOmg6gRJop0t8LGcUCiH8q1A==",
    ]
    count = 0

    def __init__(self, *args, **kwargs):
        super(UserInfoSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        uids = ['6239620007'] * 1000  # 生成1000条
        start_urls = [f'{self.base_url}?uid={uid}' for uid in uids]
        for url in start_urls:
            time.sleep(0.2)  # 提交延迟
            self.count += 1
            idx = self.count % len(self.cookies)
            self.headers["cookie"] = self.cookies[idx]
            # yield Request(url, callback=self.parse, headers=self.headers, meta={'cookiejar': idx}, dont_filter=True)
            yield Request(url, callback=self.parse, headers=self.headers, dont_filter=True)

    def parse(self, response):
        data = json.loads(response.text)
        ok = bool(data['ok'])
        if ok:
            print(data['data'])
            # bloc = data['data']
            # item = UserInfoItem()
            # item['user_id'] = str(bloc['user']['id'])  # 源微博id
            # item['friends_count'] = str(bloc['user']['friends_count'])  # 关注数
            # item['followers_count'] = str(bloc['user']['followers_count'])  # 粉丝数
            # item['statuses_count'] = str(bloc['user']['statuses_count'])  # 微博数
            # yield item
        else:
            print(data)
            pass
