# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import re
import time
# import MySQLdb
# import MySQLdb.cursors
import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class GlobaltimesPipeline:
    def __init__(self):
        print(f"{time.asctime()} start to refresh")
        self.conn = pymysql.connect(
            host='localhost',  #settings['Mysql_HOST'],
            port=settings['Mysql_PORT'],
            db='english_news',
            user='root',
            password='632632632',
            charset='utf8'
        )

        self.cursor = self.conn.cursor()
        print('Mysql 连接成功')

    def process_item(self, item, spider):
        news = {}

        news['news_id'] = self.get_id("".join(item['url']))
        # news['module'] = "".join(item['module']).strip()
        # news['type'] = "".join(item['type']).strip()
        news['url'] = "".join(item['url'])
        news['article_level_one'] = "".join(item['article_level_one'])
        news['article_level_two'] = "".join(item['article_level_two'])
        # news['author'] = self.get_author("".join(item['info']))
        # news['source'] = self.get_source("".join(item['info']))
        news['title'] = "".join(item['title']).strip()
        news['content'] = "".join(item['content']).strip()
        news['abstract'] = "".join(item['abstract']).strip()
        news['pub_time'] = "".join(item['pub_time'])
        # news['published_time'] = self.get_published_time("".join(item['info']))
        # 执行sql
        self.insert_item(news)
        print(f"{time.asctime()} insert a data")
        # 错误时回调

        return item
        pass

    def on_error(self, failure, spider):
        spider.logger.error(failure)

    def insert_item(self,item):
        sql = "insert into english_news.news_globaltimes "    #数据库 与 表名
        sql += "(news_id,url,article_level_one,article_level_two,title,abstract,content,pub_time)"
        sql += " values (%s,%s,%s,%s,%s,%s,%s,%s)"
        params = (item['news_id'],  item['url'],
                  item['article_level_one'], item['article_level_two'], item['title'],item['abstract'],
                  item['content'], item['pub_time'])
        self.cursor.execute(sql, params)
        self.conn.commit()
        print('插入数据库成功:' + item['url'])

    def get_id(self, url):
        pat = '\d{7}'
        return re.findall(pat,url)
        #return re.findall("(\w*[0-9]+)\w*", url)[0]

    def get_author(self, info):
        author_p = r"(?<=By).+?(?=Source:)"

        author_pattern = re.compile(author_p)
        author_match = re.search(author_pattern, info)
        if author_match:
            return author_match.group(0).strip()
        else:
            return ''

    def get_source(self, info):
        source_p = r"(?<=Source:).+?(?=Published)"

        source_pattern = re.compile(source_p)
        source_match = re.search(source_pattern, info)
        if source_match:
            return source_match.group(0).strip()
        else:
            return ''

    def get_published_time(seld, info):
        published_p = r"(?<=Published:).+?(.*)"

        published_pattern = re.compile(published_p)
        published_match = re.search(published_pattern, info)
        if published_match:
            return published_match.group(0).strip().replace('/', '-')
        else:
            return ''