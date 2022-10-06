from optparse import Option
import scrapy
from scrapy import Request
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from comments.items import CommentsItem
#from comments.settings import Pages
import time


class SpiderocSpider(scrapy.Spider):
    name = 'spideroc'
    allowed_domains = ['item.jd.com']

    def __init__(self):
        self.Pages = 0

    def start_requests(self):

        for i in range(51):
            yield Request(url='https://item.jd.com/100019125569.html#comment', dont_filter=True)
            self.Pages = self.Pages + 1

            

    def parse(self, response):
        sel = scrapy.Selector(response)
        list_items = sel.css('#comment > div.mc > div.J-comments-list.comments-list.ETab > div.tab-con > #comment-0 > div.comment-item')
        for list_item in list_items:
            comment_item = CommentsItem()
            comment_item['name'] = list_item.css('div.user-column > div.user-info > img::attr(alt)').extract()
            comment_item['time'] = list_item.css('div.comment-column.J-comment-column > div.comment-message > div.order-info > span:last-child::text').extract()
            comment_item['content'] = '\n'.join(list_item.css('div.comment-column.J-comment-column > p::text').extract())
            yield comment_item
        

    