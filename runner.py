from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from jobparser import settings
from jobparser.spiders.hhru import HhruSpider

if __name__ == "__main__":
    crawler_settings = Settings()  # настройки
    crawler_settings.setmodule(settings)  # словарь
    process = CrawlerProcess(settings=crawler_settings)  # процесс
    process.crawl(HhruSpider)  # работник
    process.start()  # запуск