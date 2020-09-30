#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @Author Tabuyos
 @Time 2020/9/27 10:17
 @Site www.tabuyos.com
 @Email tabuyos@outlook.com
 @Description
"""
import os
from os.path import abspath

from scrapy import cmdline

from crazy_crawler.crazy_crawler.spiders.blog_spider import BlogSpider


def change_dir(path):
    """
    切换当前工作目录

    :param path: 相对根目录的子目录
    :return: None
    """
    project_name = "crazy-crawler"
    root_path = os.path.join(abspath(__file__).split(project_name)[0], project_name)
    os.chdir(os.path.join(root_path, path))


def start_scrapy(path, name):
    """
    在相应的目录下执行相应的爬虫

    :param path: scrapy项目所在的目录
    :param name: scrapy项目中爬虫的名称
    :return: None
    """
    # 切换到对应的 Scrapy 工作空间
    change_dir(path)
    # 执行指定的爬虫
    # cmdline.execute("scrapy crawl {name} -s LOG_FILE=logs/spider-{name}.log".format(name=name).split())
    cmdline.execute("scrapy crawl {name}".format(name=name).split())


if __name__ == '__main__':
    start_scrapy("crazy_crawler", BlogSpider.name)
