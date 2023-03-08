# weibo-spider

[教程](https://scrapy-cookbook.readthedocs.io/zh_CN/latest/scrapy-01.html)

python环境: python >= 3.7

1. 填入微博的cookie到 /weibospider/cookie.txt
2. mysql上执行weibo_datas.sql 建立数据库用来存放相关的数据
3. /weibospider 目录下增加private_setting.py文件 格式如下
```python
# 数据库配置 pipelines文件中定义了数据流向的是数据库
MYSQL_HOST = 'xxx'
MYSQL_DATABASE = 'xxx'
MYSQL_USERNAME = 'xxx'
MYSQL_PASSWORD = 'xxx'
MYSQL_PORT = 'xxx'


# email 这个可以不用填 当初调用邮箱服务留下来的
MAIL_FROM = "xxx"
MAIL_HOST = 'xxx'
MAIL_PORT = 25
MAIL_USER = 'xxx'
MAIL_PASS = 'xxx'
MAIL_TLS = False
MAIL_SSL = False
```

4. run
```bash
pip install -r requirements.txt
scrapy crawl origin_weibo # 代码里是爬取深圳大学下的所有微博
```

爬取当前热搜榜 -- hot_band.py
> scrapy crawl hot_band -O hot_band.csv

爬取某个话题下面的推文和转发 -- weibo_hot_search.py
> scrapy crawl weibo_hot_search
