#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @Author Tabuyos
 @Time 2020/10/9 10:10
 @Site www.tabuyos.com
 @Email tabuyos@outlook.com
 @Description
"""
import os
from os.path import abspath

from scrapy import Spider, Request

from op_json.op_json import OperateJson


class CrazySpider(Spider):
    project_name = "crazy-crawler"

    # get spider config.
    root_path = os.path.join(abspath(__file__).split(project_name)[0], project_name)
    dataset = OperateJson(os.path.join(root_path, "config/WebSiteListing.json")).load_json()
    site_list = dataset.get("Listing")

    name = "crazy-crawler"

    def parse(self, response, **kwargs):
        current_url = response.url
        body = response.body
        site_info = response.request.meta.get("site_info")
        if body == b'get_next_url':
            ls = self.site_list
            pending_index = ls.index(site_info.get("BaseInfo").get("Name")) + 1
            if len(ls) != pending_index:
                name = ls[pending_index]
            else:
                return None
            config_path = os.path.join(self.root_path, "config/{name}_Config.json".format(name=name))
            site_info = OperateJson(config_path).load_json()
            pending_url = site_info.get("BaseInfo").get("Url")
            meta = {"first": True, "site_info": site_info}
            yield Request(url=pending_url, callback=self.parse, meta=meta, dont_filter=True)
        article = site_info.get("CrawlerInfo").get("Article")
        for art in response.selector.xpath(article.get("XPath")):
            result1 = art.xpath(article.get("ContentElements")[0].get("XPath")).extract()
            result2 = art.xpath(article.get("ContentElements")[1].get("XPath")).extract()
            result3 = art.xpath(article.get("ContentElements")[2].get("XPath")).extract()
            print("".join(result1).strip(), "|", "".join(result2).strip(), "|", "".join(result3).strip())
        if body != "end_url":
            yield Request(url=current_url, callback=self.parse, meta={"site_info": site_info}, dont_filter=True)
        else:
            pass

    def start_requests(self):
        print("==============================", "Tabuyos-start_requests", "==============================")
        config_path = os.path.join(self.root_path, "config/{name}_Config.json".format(name=self.site_list[0]))
        site_info = OperateJson(config_path).load_json()
        init_url = site_info.get("BaseInfo").get("Url")
        yield Request(url=init_url, callback=self.parse, meta={"first": True, "site_info": site_info}, dont_filter=True)
