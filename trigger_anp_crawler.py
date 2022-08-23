"""
TODO: docstring
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from anp_crawler.spiders.anp import AnpSpider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(AnpSpider)
process.start()
