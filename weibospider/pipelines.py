# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from  weibospider import settings
import pymysql
import weibospider.items

class WeibospiderPipeline:
    connect = None
    cursor = None

    def open_spider(self, spider):
        self.connect = pymysql.connect(
            host = settings.MYSQL_HOST,
            db = settings.MYSQL_DATABASE,
            user = settings.MYSQL_USERNAME,
            passwd = settings.MYSQL_PASSWORD,
            charset = 'utf8'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        database= 'use weibo_datas;'
        if isinstance(item,weibospider.items.OriginWeiboItem):
            table = 'create table if not exists weibo(' \
                        'id int not null primary key auto_increment' \
                        ',origin_weibo_id varchar(1000)' \
                        ',origin_user_id varchar(1050)' \
                        ',origin_weibo_content varchar(1000)' \
                        ',publish_time varchar(1000)' \
                        ',repost_count varchar(1000)' \
                        ',like_count varchar(1000)' \
                        ');'
            sql = 'INSERT INTO weibo(origin_weibo_id, origin_user_id, origin_weibo_content,publish_time,repost_count,like_count)VALUES(%s,%s,%s,%s,%s,%s) '
            data = (item['origin_weibo_id'], item['origin_user_id'], item['origin_weibo_content'],item['publish_time'],item['repost_count'],item['like_count'])
        elif  isinstance(item,weibospider.items.RepostWeiboItem):          
            table = 'create table if not exists repost_weibo(' \
                        'id int not null primary key auto_increment' \
                        ',origin_weibo_id varchar(1000)' \
                        ',origin_user_id varchar(1050)' \
                        ',repost_weibo_id varchar(1000)' \
                        ',repost_user_id varchar(1000)' \
                        ',repost_weibo_content varchar(1000)' \
                        ',repost_publish_time varchar(1000)' \
                        ');'
            sql = 'INSERT INTO repost_weibo(origin_weibo_id, origin_user_id, repost_weibo_id,repost_user_id,repost_weibo_content,repost_publish_time)VALUES(%s,%s,%s,%s,%s,%s) '
            data = (item['origin_weibo_id'], item['origin_user_id'], item['repost_weibo_id'],item['repost_user_id'],item['repost_weibo_content'],item['repost_publish_time'])
        else:
            table = 'create table if not exists user_info(' \
                        'id int not null primary key auto_increment' \
                        ',user_id varchar(1000)' \
                        ',friends_count varchar(1050)' \
                        ',followers_count varchar(1000)' \
                        ',statuses_count varchar(1000)' \
                        ');'
            sql = 'INSERT INTO user_info(user_id, friends_count, followers_count,statuses_count)VALUES(%s,%s,%s,%s) '
            data = (item['user_id'], item['friends_count'], item['followers_count'],item['statuses_count'])            
        try:
            self.cursor.execute(database)
            self.cursor.execute(table)
            self.cursor.execute(sql, data)
            self.connect.commit()
        except   Exception as e:
            print('===============插入数据失败===============',e)
            self.connect.rollback()
        return item

    def close_spider(self, spider):
        self.connect.commit()
        self.connect.close()       