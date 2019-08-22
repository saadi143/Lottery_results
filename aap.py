from scrapy.crawler import CrawlerProcess
from Lottery.spiders import Lotto

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())

    process.crawl(Lotto)
    process.start() # the script will block here until the crawling is finished
