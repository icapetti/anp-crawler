from spidermon.contrib.actions.slack.notifiers import SendSlackMessageSpiderFinished
from spidermon.core.suites import MonitorSuite
from spidermon.contrib.scrapy.monitors import (
    ItemCountMonitor            # SPIDERMON_MIN_ITEMS
    ,ErrorCountMonitor          # SPIDERMON_MAX_ERRORS
    ,FinishReasonMonitor        # SPIDERMON_EXPECTED_FINISH_REASONS
    ,UnwantedHTTPCodesMonitor   # SPIDERMON_UNWANTED_HTTP_CODES_MAX_COUNT, SPIDERMON_UNWANTED_HTTP_CODES
    ,ItemValidationMonitor      # SPIDERMON_MAX_ITEM_VALIDATION_ERRORS
)

from spidermon import Monitor, monitors
from spidermon.contrib.monitors.mixins.stats import StatsMonitorMixin
from anp_crawler.actions import CloseSpiderAction, SendStatsToS3Action

@monitors.name("History Validation")
class HistoryMonitor(Monitor):

    @monitors.name("Expected number of items extracted")
    def test_expected_number_of_items_extracted(self):
        spider = self.data["spider"]
        total_previous_jobs = len(spider.stats_history)
        if total_previous_jobs == 0:
            return

        previous_item_extracted_mean = (
            sum(
                previous_job["item_scraped_count"]
                for previous_job in spider.stats_history
            )
            / total_previous_jobs
        )
        items_extracted = self.data.stats["item_scraped_count"]

        # Minimum number of items we expect to be extracted
        #minimum_threshold = 0.9 * previous_item_extracted_mean
        minimum_threshold = 2 * previous_item_extracted_mean

        self.assertFalse(
            items_extracted <= minimum_threshold,
            msg=f"Expected at least {minimum_threshold} items extracted.",
        )

class SpiderCloseMonitorSuite(MonitorSuite):
    """
    To activate this suite add to settings.py:
    SPIDERMON_SPIDER_CLOSE_MONITORS = {
        'spidermon.contrib.scrapy.monitors.SpiderCloseMonitorSuite',
    }
    """
    
    monitors = [
        ItemCountMonitor
        ,ErrorCountMonitor
        ,FinishReasonMonitor
        ,UnwantedHTTPCodesMonitor
        ,ItemValidationMonitor
        ,HistoryMonitor
    ]

    monitors_finished_actions = [
        # actions to execute when suite finishes its execution
        SendStatsToS3Action
    ]

    monitors_failed_actions = [
        # actions to execute when suite finishes its execution with a failed monitor
        SendSlackMessageSpiderFinished
    ]

@monitors.name('Periodic job stats monitor')
class PeriodicJobStatsMonitor(Monitor, StatsMonitorMixin):

    @monitors.name('Should not have more unwanted http code than success')
    def test_number_of_unwanted_http_status(self):
        success_http_codes = self.data.stats.get('downloader/response_status_count/200', 0)
        unwanted_http_codes = self.data.stats.get('downloader/response_status_count/429', 0)

        msg = 'The job has more http unwated 429 code than success 200 code.'
        self.assertLessEqual(unwanted_http_codes, success_http_codes, msg=msg)

    @monitors.name('Number of items extracted should be greater than 1 after 15 minutes of running')
    def test_number_items_extracted(self):
        no_items_count = 1
        items_count = self.data.stats.get('item_scraped_count', 0)
        msg = 'The job has no items extracted after 15 minutes of execution.'
        self.assertLess(items_count, no_items_count, msg=msg)

class PeriodicMonitorSuite(MonitorSuite):
    """
    To activate this suite add to settings.py:
    SPIDERMON_PERIODIC_MONITORS = {
        'anp_crawler.monitors.PeriodicMonitorSuite': 900,  # time in seconds
    }
    """

    monitors = [
        PeriodicJobStatsMonitor
    ]
    monitors_failed_actions = [
        CloseSpiderAction
    ]
