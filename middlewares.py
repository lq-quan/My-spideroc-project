# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from glob import glob
from requests import request
from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy.http import HtmlResponse, Response
from selenium.webdriver.common.by import By
#from comments.settings import Pages
import time

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

#from comments.spiders.spideroc import Pages


class CommentsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CommentsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumCommentsDownloaderMiddleware(object):

    def __init__(self):
        self.reses = []

    def collect_all(self, request, spider):
        if spider.Pages == 0:
            self.driver = webdriver.Firefox()
            if spider.name == 'spideroc':
                self.driver.get(request.url)
                for x in range(1, 11, 2):
                    height = float(x) / 10
                    js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * %f' % height
                    self.driver.execute_script(js)
                    time.sleep(0.2)

                time.sleep(1.0)
                
                for i in range(51):
                    origin_code = self.driver.page_source
                    res = scrapy.http.HtmlResponse(url=request.url, encoding='utf-8', body=origin_code, request=request)
                    self.reses.append(res)
                    time.sleep(1.0)
                    self.driver.find_element(By.CLASS_NAME, 'ui-pager-next').click()
                    time.sleep(1.0)
                self.driver.quit()
            return 
        else:
            return 


    def process_request(self, request, spider):
        self.collect_all(request, spider)
        return self.reses[spider.Pages]

    def process_response(self, response, request, spider):
        print(response.url, response.status)
        return response
