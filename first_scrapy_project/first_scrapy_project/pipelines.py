# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
import pymongo
import sqlite3
# class MongodbPipeline:
    
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient('localhost', 27017)
#         self.db = self.client['audible']
#         logging.warning('Spider opened -- pipeline')
        
#     def close_spider(self, spider):
#         self.client.close()
#         logging.warning('Spider closed -- pipeline')
    
#     def process_item(self, item, spider):
#         self.db['audible'].insert_one(item)
#         return item
    
class SQlitePipeline:
    
    def open_spider(self, spider):
        self.connection = sqlite3.connect('audible.db')
        self.cursor = self.connection.cursor()
        
        # query
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS audible(
                title TEXT,
                author TEXT,
                language TEXT,
            )
        ''')
        self.connection.commit()
        logging.warning('Spider opened -- pipeline')
        
    def close_spider(self, spider):
        self.connection.close()
        logging.warning('Spider closed -- pipeline')
    
    def process_item(self, item, spider):
        self.cursor.execute('''INSERT INTO audible(title, author, language) VALUES(?,?,?)''', (
            item.get('title'),
            item.get('author'),
            item.get('language'),
        ))
        self.connection.commit()
        return item