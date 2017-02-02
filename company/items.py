# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader.processors import MapCompose, Join


class CompanyItem(scrapy.Item):
    company_name = scrapy.Field()
    stand_id = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field(
        input_processor=MapCompose(lambda x: ' '.join(x.split())),
        output_processor=Join(),
    )
    address = scrapy.Field(
        input_processor=MapCompose(lambda x: ' '.join(x.split())),
        output_processor=Join(),
    )
    telephone = scrapy.Field(
        input_processor=MapCompose(lambda x: ' '.join(x.split())),
    )
    website_url = scrapy.Field()
