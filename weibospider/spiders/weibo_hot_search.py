import scrapy
import json
import re
import urllib.parse
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

    def __init__(self, *args, **kwargs):
        super(WeiboHotSearchSpider, self).__init__(*args, **kwargs)

    # def start_requests(self):
    #     yield scrapy.Request(start_urls, callback=self.parse)

    # for key in self.key_words:
    #     hot_search_url = f'https://s.weibo.com/weibo?q={key}&page={self.key_words_pages[key]}'
    #     yield scrapy.Request(hot_search_url, callback=self.parse,
    #                          meta={'user_id': key, 'page_num': self.key_words_pages[key]})

    def parse(self, response):
        data = json.loads(response.text)
        band_list = data['data']['band_list']
        for band in band_list:
            if 'word_scheme' in band:
                key = urllib.parse.quote(band['word_scheme'])
                hot_search_url = f'https://s.weibo.com/weibo?q={key}&page={1}'
                yield scrapy.Request(hot_search_url, callback=self.parse_origin,
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
            yield Request(user_url, callback=self.parse_user)

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
            yield Request(url, callback=self.parse_origin, meta={'user_id': user_id, 'page_num': page_num})

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
            yield Request(user_url, callback=self.parse_user)
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
