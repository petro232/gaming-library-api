# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class BacklogedPipeline:
#     def process_item(self, item, spider):
#         return item
import sqlite3

class  SQLitePipeline:
    def open_spider(self,spider):
        self.conn=sqlite3.connect("backlooged.db")
        self.c=self.conn.cursor()
        self.c.execute("""
               CREATE TABLE IF NOT EXISTS game
                       (
                        title TEXT,
                         year TEXT,
                       rating TEXT,
                       played INTEGER,
                       playing INTEGER,
                       backlog INTEGER,
                       wishlist INTEGER,
                       likes INTEGER,
                       released TEXT,
                       url TEXT UNIQUE ,
                       post_image TEXT,
                       studio TEXT,
                       genres TEXT,
                       story TEXT
                    
                       )    
""")
        self.conn.commit()
    

    def close_spider(self,spider):
        self.conn.close()



    def process_item(self,item,spider):
        self.c.execute("""

                 INSERT OR IGNORE INTO game (title,year,rating,played,playing,backlog,wishlist,likes,released,url,post_image,studio,genres,story)
                       

                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                       
                                                """,
                ( 
                    item.get("title"),
                    item.get("year"),
                    item.get("rating"),
                    item.get("played"),
                    item.get("playing"),
                    item.get("backlog"),
                    item.get("wishlist"),
                    item.get("likes"),
                    ",".join(item.get("released",[])),
                           item.get("url"),
                              item.get("post_image"),
                                 ",".join(item.get("studio",[])) ,
                                   ",".join(item.get("genres",[])),
                                    item.get("story") ) )
        
        self.conn.commit()
        return item