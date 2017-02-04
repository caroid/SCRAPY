# -*- coding: utf-8 -*-
import scrapy
from company.items import CompanyItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
# import time


class CompanyspiderSpider(scrapy.Spider):
    name = "comspider"
    allowed_domains = ["springfair.com"]
    start_urls = (
        'http://www.springfair.com/page.cfm/action=ExhibList/listid=1',
    )
    custom_settings = {
        "FEED_EXPORT_FIELDS": ["company_name", "category", "stand_id", "telephone", "address",
                               "website_url", "description"]
    }

    def __init__(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1920, 1080)

    def parse(self, response):
        for element in response.xpath('//div[contains(@class, "ez_list")]/ul/li'):
            item = CompanyItem()
            item['company_name'] = element.xpath('.//a/text()').extract_first()
            item['stand_id'] = element.xpath('.//div/text()').extract_first()
            item['category'] = element.xpath(
                './/span[contains(@class, "ez_merge15")]/text()').extract_first()

            url = element.xpath('.//a/@href').extract_first()
            request = scrapy.Request(url, callback=self.parse_company)
            request.meta['item'] = item
            yield request
            # Request for next page
            # url = response.xpath(
            #     '//span[contains(@class, "ezlist-page-next")]/a/@href').extract_first()
            # if url:
            #     yield scrapy.Request(url, callback=self.parse)

    def parse_company(self, response):
        item = response.meta['item']
        loader = ItemLoader(item=CompanyItem(), response=response)
        loader.default_output_processor = TakeFirst()
        self.driver.get(response.url)
        try:
            self.driver.find_element_by_xpath('//a[span[@class="view-website"]]').click()
            self.driver.switch_to.window(self.driver.window_handles[-1])
            url = self.driver.current_url
            loader.add_value('website_url', url)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except NoSuchElementException:
            with open("don't_have_url.txt", 'a+') as f:
                f.write(response.url + '\n')
            self.logger.info("This company don't have website!")
            pass
        loader.add_value('company_name', item['company_name'])
        loader.add_value('stand_id', item['stand_id'])
        loader.add_value('category', item['category'])
        loader.add_xpath('description', '//div[contains(@class, "profile__description")]//text()')
        loader.add_xpath('address', '//div[contains(@class, "entrydescitem")]//text()')
        loader.add_xpath('telephone', '//div[contains(@class, "contact__main__phone")]/li[1]/text()')
        yield loader.load_item()
