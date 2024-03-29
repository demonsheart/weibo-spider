# from .myextend import pro
# import random
from weibospider import private_setting


class ProxyDownloaderMiddleware:
    def process_request(self, request, spider):
        # proxy = random.choice(pro.proxy_list)

        # 隧道代理固定服务器 无需提取代理
        proxy = 'd393.kdltps.com: 15818'

        # 用户名密码认证(私密代理/独享代理)
        username = private_setting.PROXY_USERNAME
        password = private_setting.PROXY_PASSWORD
        request.meta['proxy'] = "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password,
                                                                        "proxy": proxy}

        # 白名单认证(私密代理/独享代理)
        # request.meta['proxy'] = "http://%(proxy)s/" % {"proxy": proxy}
        return None
