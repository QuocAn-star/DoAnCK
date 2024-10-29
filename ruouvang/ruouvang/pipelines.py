# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class RuouvangPipeline:
    def __init__(self):

        self.connection = sqlite3.connect('products_wine.db')
        self.cursor = self.connection.cursor()

        #Tạo bảng
        self.cursor.execute('''
        Create table wines(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price TEXT,
        img TEXT,
        url TEXT,
        wine_type TEXT,
        grape_variety TEXT,
        alcohol_concentration TEXT,
        volume TEXT,
        vintage TEXT
        )'''
        )


