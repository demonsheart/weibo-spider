import os

if __name__ == '__main__':

    rounds = 5
    cur_round = 0
    crawl_name = 'user_info'
    while rounds > cur_round:
        cur_round += 1
        print(f"第{cur_round}轮爬虫启动................")
        os.system(f"scrapy crawl {crawl_name} ")
        print(f"第{cur_round}轮爬虫结束................")
