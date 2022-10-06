# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import openpyxl
import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CommentsPipeline:

    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306,
                                    user='root', password='quan9672697611',
                                    database='commentsdb', charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        name = item.get('name', '')
        time = item.get('time', '')
        content = item.get('content', '')
        self.cursor.execute(
            'insert into comments (name, time, content) value (%s, %s, %s)',
            (name, time, content)
        )
        return item
