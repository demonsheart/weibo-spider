from scrapy import signals
from .myextend import pro
import random


class ProxyDownloaderMiddleware:
    def process_request(self, request, spider):
        proxy = random.choice(pro.proxy_list)

        # 用户名密码认证(私密代理/独享代理)
        username = "t17838136409119"
        password = "h6vksi39"
        request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password,
                                                                        "proxy": proxy}

        # 白名单认证(私密代理/独享代理)
        # request.meta['proxy'] = "http://%(proxy)s/" % {"proxy": proxy}
        return None
