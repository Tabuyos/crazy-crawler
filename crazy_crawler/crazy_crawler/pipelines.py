# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


class CrazyCrawlerPipeline:

    def __init__(self):
        self.file = None

    def open_spider(self, spider):
        self.file = open('dataset/area.json', 'w')

    def process_item(self, item, spider):
        print("==============================", "Tabuyos-process_item", "==============================")
        return item

    def close_spider(self, spider):
        self.file.close()
