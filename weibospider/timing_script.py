import time
import sys
import os
import datetime
 
 
if __name__ == '__main__':
    
    while True:
         
        print("爬虫启动................")
        
        os.system("python3 -m scrapy crawl user_info ") 
        print("爬虫结束................")
        time.sleep(20)                # 每两分钟执行一次 
