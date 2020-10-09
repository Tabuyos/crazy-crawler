#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @Author Tabuyos
 @Time 2020/10/9 10:52
 @Site www.tabuyos.com
 @Email tabuyos@outlook.com
 @Description
"""
from logging import getLogger

from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumDownloaderMiddleware:

    def __init__(self, timeout=None, chrome_options=None):
        if chrome_options is None:
            chrome_options = Options()
        self.logger = getLogger(__name__)
        self.timeout = timeout
        self.browser = webdriver.Chrome(options=chrome_options)
        self.browser.maximize_window()
        self.browser.set_page_load_timeout(self.timeout * 2)
        self.browser.implicitly_wait(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout)

    @classmethod
    def from_crawler(cls, crawler):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        return cls(timeout=crawler.settings.get('SELENIUM_TIMEOUT'),
                   chrome_options=chrome_options)

    def __del__(self):
        print("======================================= start close =======================================")
        self.browser.close()

    def process_request(self, request, spider):
        """
        用 Chrome 抓取页面

        :param request: Request对象
        :param spider: Spider对象
        :return: HtmlResponse
        """
        self.logger.debug('Chrome is Starting')
        flag = False
        try:
            site_info = request.meta.get("site_info")
            if request.meta.get("first"):
                self.browser.get(request.url)
            else:
                try:
                    next_xpath = site_info.get("CrawlerInfo").get("Article").get("ChildPages").get("XPath")
                    self.wait.until(EC.presence_of_element_located((By.XPATH, next_xpath)))
                    next_page = self.wait.until(EC.element_to_be_clickable((By.XPATH, next_xpath)))
                    if next_page:
                        next_page.click()
                    else:
                        pass
                except TimeoutException:
                    flag = True

            if flag:
                return HtmlResponse(url=request.url, body="get_next_url", status=200, encoding='utf-8', request=request)

            try:
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, site_info.get("CrawlerInfo").get("Article").get("XPath"))))
            except TimeoutException:
                return HtmlResponse(url=request.url, status=500, request=request)

            page_source = self.browser.page_source
            url = self.browser.current_url

            return HtmlResponse(url=url, body=page_source, request=request, encoding='utf-8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url, status=500, request=request)
