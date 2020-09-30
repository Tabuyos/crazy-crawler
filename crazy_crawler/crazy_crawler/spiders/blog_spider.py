#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @Author Tabuyos
 @Time 2020/9/27 10:07
 @Site www.tabuyos.com
 @Email tabuyos@outlook.com
 @Description
"""
import os
from os.path import abspath

from scrapy import Spider, Request

from op_json.op_json import OperateJson


class BlogSpider(Spider):
    name = 'woodenrobot'
    start_urls = ['http://woodenrobot.me']

    def parse(self, response, **kwargs):
        project_name = "crazy-crawler"
        root_path = os.path.join(abspath(__file__).split(project_name)[0], project_name)
        dataset = OperateJson(os.path.join(root_path, "config/WebSiteListing.json")).load_json()
        site_list = dataset.get("Listing")
        # for site_code in site_list:
        #     site_info = OperateJson(os.path.join(root_path, "config/{name}_Config.json".format(name=site_code))).load_json()
        #     for el in site_info.get("CrawlerInfo").get("Article").get("ContentElements"):
        #         titles = response.xpath(el.get("XPath")).extract()
        #         print(len(response.xpath("//*[@id=\"posts\"]/article")))
        #         for title in titles:
        #             print(title.strip())
        url = response.selector.xpath("//a[contains(@class, 'extend') and contains(@class, 'next')]/@href").extract()

        print(url)
        for i in response.selector.xpath("//*[@id=\"posts\"]/article"):
            result1 = i.xpath("./header/h2/a/text()").extract()
            result2 = i.xpath("./header/div/span[2]/span[4]/a/span/text()").extract()
            result3 = i.xpath("./header/div/span[1]/time/text()").extract()
            print("".join(result1).strip(), "".join(result2).strip(), "".join(result3).strip())

        response.selector.xpath("//*[@id=\"posts\"]/article")
        if len(url) == 0:
            pass
        else:
            yield Request(url="https://woodenrobot.me" + url[0], callback=self.parse)

        # titles = response.xpath('//a[@class="post-title-link"]/text()').extract()
        # for title in titles:
        #     print(title.strip())

    # def start_requests(self):
    #     print("==============================", "Tabuyos-start_requests", "==============================")
    #     yield Request(url=self.start_urls[0], callback=self.parse, meta={'page': 1}, dont_filter=True)
