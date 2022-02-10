# Scrapy settings for anp_crawler project

import os
from random import choice

from dotenv import load_dotenv

# Loads variables on the .env file to the local environment variables
# Add your aws credentials on the .env file
user = os.environ.get("USER") if os.environ.get("USER") else os.environ.get("USERNAME")
load_dotenv(f'/home/{user}/.credentials/.env')

BOT_NAME = 'anp_crawler'

SPIDER_MODULES = ['anp_crawler.spiders']
NEWSPIDER_MODULE = 'anp_crawler.spiders'

# LOG Level
LOG_ENABLED = True
LOG_LEVEL = 'INFO'

# CREDENTIALS FOR S3
AWS_ACCESS_KEY_ID = os.getenv("aws_id")
AWS_SECRET_ACCESS_KEY = os.getenv("aws_secret")

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

DOWNLOAD_DELAY = 1.0

# Activate Spidermon
SPIDERMON_ENABLED = True

EXTENSIONS = {
    'spidermon.contrib.scrapy.extensions.Spidermon': 500,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'anp_crawler.pipelines.AnpCrawlerPipeline': 300,
    'spidermon.contrib.scrapy.pipelines.ItemValidationPipeline': 800,
}

# Configure Validations and Monitoring
SPIDERMON_VALIDATION_SCHEMAS = [
    './anp_crawler/schemas/anp_default_schema.json',
]

SPIDERMON_PERIODIC_MONITORS = {
    'anp_crawler.monitors.PeriodicMonitorSuite': 900,  # time in seconds
}

SPIDERMON_SPIDER_CLOSE_MONITORS = {
    'anp_crawler.monitors.SpiderCloseMonitorSuite',
}

SPIDERMON_MIN_ITEMS = 2100
SPIDERMON_MAX_ERRORS = 0
SPIDERMON_EXPECTED_FINISH_REASONS = ["finished"]
SPIDERMON_UNWANTED_HTTP_CODES_MAX_COUNT = 10
SPIDERMON_UNWANTED_HTTP_CODES = [400, 407, 429, 500, 502, 503, 504, 523, 540, 541]
SPIDERMON_MAX_ITEM_VALIDATION_ERRORS = 0

SPIDERMON_SLACK_SENDER_TOKEN = os.getenv("slack_alert_token")
SPIDERMON_SLACK_SENDER_NAME = 'Spidermon Monitoring'
SPIDERMON_SLACK_RECIPIENTS = ['C02U54LHZ61',]

# Store locally stats history
STATS_CLASS = (
    "spidermon.contrib.stats.statscollectors.LocalStorageStatsHistoryCollector"
)

# Stores the stats of the last 10 spider execution (default=100)
SPIDERMON_MAX_STORED_STATS = 10

# Configure exporters
# FEED compressed jsonlines
FEED_EXPORTERS = {
    'jl.gz': 'anp_crawler.exporters.JsonLinesGzipItemExporter',
}
FEED_EXPORT_ENCODING = 'utf-8'
FEED_EXPORT_BATCH_ITEM_COUNT = 10000

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = choice([
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0", 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2483.0 Safari/537.36",
    "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240", 
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
])
