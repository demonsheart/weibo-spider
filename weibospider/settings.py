# Scrapy settings for weibospider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weibospider'

SPIDER_MODULES = ['weibospider.spiders']
NEWSPIDER_MODULE = 'weibospider.spiders'

# Retry
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 503, 504, 400, 408]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'weibospider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie': 'XSRF-TOKEN=g4wOcbWfU6QMUiwIDkWFNi32; PC_TOKEN=0404c1ae43; login_sid_t=bd1d874c47d5ce7c43d2523bedc32cac; cross_origin_proto=SSL; WBStorage=4d96c54e|undefined; _s_tentry=passport.weibo.com; Apache=3195839589278.7793.1678524226679; SINAGLOBAL=3195839589278.7793.1678524226679; ULV=1678524226680:1:1:1:3195839589278.7793.1678524226679:; wb_view_log=2560*14401; SUB=_2A25JCE8iDeRhGeNH4lEW9inNzziIHXVqfCfqrDV8PUNbmtANLXLZkW9NSnAePWauxCBbpWqOhCsY7QSyZLJ8okz9; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF.sG7_X0HX15pY5xDmTs5A5JpX5KzhUgL.Fo-41KeNSoMpShB2dJLoI0YLxKMLB.eL1KnLxKML1KBL1-qLxKMLB.eL1KnLxKML1h2LB-BLxKMLB.eL1KnLxK-LBo5LB.BLxKqL1K-LBKet; ALF=1710060273; SSOLoginState=1678524274; WBPSESS=kTzxXaFYfeELPFRjS_d8EHEAFHiaqY-3K1QrxDD54Yaq1jmuQ4auYnjWbn2d4uBI0F_kC7PNtN4-roHL5ORto691G76fUq1Btjo4JzicsjUISpii9qE07LnmAhEkhK-qM40deX90Mx17CXo-JC96Cw=='
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'weibospider.middlewares.WeibospiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 101,
    'weibospider.middlewares.ProxyDownloaderMiddleware': 100,  # 代理
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#  代理
# EXTENSIONS = {
#     'weibospider.myextend.MyExtend': 300,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'weibospider.pipelines.WeibospiderPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

ITEM_PIPELINES = {
    'weibospider.pipelines.WeibospiderPipeline': 300,
}
