# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from weibospider import private_setting
import pymysql
import weibospider.items


class WeibospiderPipeline:
    connect = None
    cursor = None

    def open_spider(self, spider):
        self.connect = pymysql.connect(
            host=private_setting.MYSQL_HOST,
            db=private_setting.MYSQL_DATABASE,
            user=private_setting.MYSQL_USERNAME,
            passwd=private_setting.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        database = 'use weibo_datas;'
        if isinstance(item, weibospider.items.OriginWeiboItem):
            sql2 = 'select * from weibo where origin_weibo_id = %s'
            data2 = item['origin_weibo_id']
            sql3 = 'update weibo set  origin_user_id=%s, origin_weibo_content=%s,publish_time=%s,repost_count=%s,like_count =%s where origin_user_id = %s'
            data3 = (item['origin_user_id'], item['origin_weibo_content'], item['publish_time'],
                     item['repost_count'], item['like_count'], item['origin_weibo_id'])
            sql = 'INSERT INTO weibo(origin_weibo_id, origin_user_id, origin_weibo_content,publish_time,repost_count,like_count)VALUES(%s,%s,%s,%s,%s,%s) '
            data = (item['origin_weibo_id'], item['origin_user_id'], item['origin_weibo_content'], item['publish_time'],
                    item['repost_count'], item['like_count'])
        elif isinstance(item, weibospider.items.RepostWeiboItem):
            sql2 = 'select * from repost_weibo where repost_weibo_id = %s'
            data2 = item['repost_weibo_id']
            sql3 = 'update repost_weibo set origin_weibo_id = %s,origin_user_id=%s, repost_user_id=%s,repost_weibo_content=%s,repost_publish_time=%s where repost_weibo_id = %s'
            data3 = (item['origin_weibo_id'], item['origin_user_id'], item['repost_user_id'],
                     item['repost_weibo_content'], item['repost_publish_time'], item['repost_weibo_id'])
            sql = 'INSERT INTO repost_weibo(origin_weibo_id, origin_user_id, repost_weibo_id,repost_user_id,repost_weibo_content,repost_publish_time)VALUES(%s,%s,%s,%s,%s,%s) '
            data = (item['origin_weibo_id'], item['origin_user_id'], item['repost_weibo_id'], item['repost_user_id'],
                    item['repost_weibo_content'], item['repost_publish_time'])
        elif isinstance(item, weibospider.items.UserInfoItem):
            sql2 = 'select * from user_info where user_id = %s'
            data2 = item['user_id']
            sql3 = 'update user_info set friends_count=%s, followers_count=%s,statuses_count =%s where user_id = %s'
            data3 = (item['friends_count'], item['followers_count'], item['statuses_count'], item['user_id'])
            sql = 'INSERT INTO user_info(user_id, friends_count, followers_count,statuses_count)VALUES(%s,%s,%s,%s) '
            data = (item['user_id'], item['friends_count'], item['followers_count'], item['statuses_count'])
        elif isinstance(item, weibospider.items.WeiboHotSearchItem):
            sql2 = 'select * from weibo_hotsearch where origin_weibo_id = %s'
            data2 = item['origin_weibo_id']
            sql3 = 'update weibo_hotsearch set  origin_user_id=%s, origin_weibo_content=%s,publish_time=%s,repost_count=%s,like_count =%s where origin_user_id = %s'
            data3 = (item['origin_user_id'], item['origin_weibo_content'], item['publish_time'],
                     item['repost_count'], item['like_count'], item['origin_weibo_id'])
            sql = 'INSERT INTO weibo_hotsearch(origin_weibo_id, origin_user_id, origin_weibo_content,publish_time,repost_count,like_count)VALUES(%s,%s,%s,%s,%s,%s) '
            data = (item['origin_weibo_id'], item['origin_user_id'], item['origin_weibo_content'], item['publish_time'],
                    item['repost_count'], item['like_count'])    
        elif isinstance(item, weibospider.items.HotSearchRepostWeiboItem):
            sql2 = 'select * from repost_weibo_hotsearch where repost_weibo_id = %s'
            data2 = item['repost_weibo_id']
            sql3 = 'update repost_weibo_hotsearch set origin_weibo_id = %s,origin_user_id=%s, repost_user_id=%s,repost_weibo_content=%s,repost_publish_time=%s where repost_weibo_id = %s'
            data3 = (item['origin_weibo_id'], item['origin_user_id'], item['repost_user_id'],
                     item['repost_weibo_content'], item['repost_publish_time'], item['repost_weibo_id'])
            sql = 'INSERT INTO repost_weibo_hotsearch(origin_weibo_id, origin_user_id, repost_weibo_id,repost_user_id,repost_weibo_content,repost_publish_time)VALUES(%s,%s,%s,%s,%s,%s) '
            data = (item['origin_weibo_id'], item['origin_user_id'], item['repost_weibo_id'], item['repost_user_id'],
                    item['repost_weibo_content'], item['repost_publish_time'])
        elif isinstance(item, weibospider.items.HotsearchUserInfoItem):
            sql2 = 'select * from user_info_hotsearch where user_id = %s'
            data2 = item['user_id']
            sql3 = 'update user_info_hotsearch set friends_count=%s, followers_count=%s,statuses_count =%s where user_id = %s'
            data3 = (item['friends_count'], item['followers_count'], item['statuses_count'], item['user_id'])
            sql = 'INSERT INTO user_info_hotsearch(user_id, friends_count, followers_count,statuses_count)VALUES(%s,%s,%s,%s) '
            data = (item['user_id'], item['friends_count'], item['followers_count'], item['statuses_count'])            
        try:
            self.cursor.execute(database)
            self.cursor.execute(sql2, data2)
            ret = self.cursor.fetchone()
            if ret:
                # 先取消update
                pass
                # self.cursor.execute(sql3, data3)
            else:
                self.cursor.execute(sql, data)
                self.connect.commit()
        except Exception as e:
            print('===============失败===============', e)
            self.connect.rollback()
        return item

    def close_spider(self, spider):
        self.connect.commit()
        self.connect.close()
