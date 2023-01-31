# weibo-spider

[教程](https://scrapy-cookbook.readthedocs.io/zh_CN/latest/scrapy-01.html)

python环境: python >= 3.7

填入cookie：
```bash
pip install -r requirements.txt
scrapy crawl origin_weibo 
scrapy crawl origin_weibo -a max_page=5 # 做了参数定义
```

爬取当前热搜榜 -- hot_band.py
> scrapy crawl hot_band -O hot_band.csv

爬取某个话题下面的推文和转发 -- weibo_hot_search.py
> scrapy crawl weibo_hot_search -a key=#阳性感染者只咳嗽发烧算无症状吗# -a reset_page=True