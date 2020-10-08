#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
 @Author Tabuyos
 @Time 2020/10/8 23:38
 @Site www.tabuyos.com
 @Email tabuyos@outlook.com
 @Description
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait


def start():
    timeout = 20
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()
    browser.set_page_load_timeout(timeout)
    wait = WebDriverWait(browser, timeout)
    browser.get("https://www.woodenrobot.me")
    print(browser.page_source)
    print(browser.current_url)
    browser.find_elements_by_xpath("//*[@id=\"posts\"]/article[2]/header/h2/a")[0].click()
    print(browser.page_source)
    print(browser.current_url)


if __name__ == '__main__':
    start()
