import logging
from datetime import date, datetime
from json import dumps
from gzip import compress

from boto3 import resource
from spidermon.core.actions import Action

class CloseSpiderAction(Action):

    def run_action(self):
        spider = self.data['spider']
        spider.logger.info("Closing spider")
        spider.crawler.engine.close_spider(spider, 'closed_by_spidermon')

class SendStatsToS3Action(Action):
    def run_action(self):
        # Include here the logic of your action
        run_date = date.today().strftime('%Y-%m-%d')
        run_datetime = datetime.now().strftime('%Y-%m-%d_%H-%m-%s')

        bucket_name = 'da-vinci-raw'
        filename = f'{self.data.spider.name}-stats-{run_datetime}.jl.gz'
        load_uri = f'logs/spidermon/{self.data.spider.name}/run={run_date}/{filename}'

        raw_stats = self.data.get('stats')
        stats = {}
        for key in raw_stats.keys():
            if isinstance(raw_stats[key], datetime):
                stats[key] = raw_stats[key].strftime("%Y-%m-%d %H:%m:%s")
            else:
                stats[key] = raw_stats[key]

        compressed_stats = compress(dumps(stats).encode())

        logging.info(f"Uploading stats to s3 \nBucket: {bucket_name}\nLoad URI: {load_uri}")
        s3 = resource('s3')
        object = s3.Object(bucket_name, load_uri)
        object.put(Body=compressed_stats)
        