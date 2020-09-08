#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spider_utils.py
@Time    :   2020/09/08 21:30:48
@Author  :   STY_lcmg
@Version :   1.0
@Contact :   lcmg.sty@gmail.com
@Desc    :   None
'''

# here put the import lib

"""
预定义基础爬虫5大模块
"""




from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import chardet
import json
import os
import os.path
class UrlManger(object):
    def __init__(self):
        # 使用 set 类型， 可以直接提供链接去重复功能
        self.new_urls = set()  # 未爬取URL集合
        self.old_urls = set()  # 已爬取URL集合

    def has_new_url(self):
        """判断是否有待取的URL"""
        return self.new_urls_size != 0

    def add_new_url(self, url):
        """添加新的URL到未爬取集合中"""
        # 判断链接是否未None (HTML解析器可能解析不出链接，返回None)
        if url is None:
            return
        # 判断链接是否在已爬取URL集合中
        if url in self.old_urls:
            return
        self.new_urls.add(url)

    def add_new_urls(self, urls):
        """添加新的URL集合到未爬取集合中"""
        # 判断链接是否未None (HTML解析器可能解析不出链接，返回None)
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def get_new_url(self):
        """获取一个未爬取的URL"""
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    @property
    def new_urls_size(self):
        """获取未爬取URL集合的大小"""
        return len(self.new_urls)

    @property
    def old_urls_size(self):
        """获取已爬取URL集合的大小"""
        return len(self.old_urls)


class HTMLDownloader(object):
    headers = {
        'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.106 Safari/537.36')
    }

    def download(self, url):
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            resp.encoding = chardet.detect(resp.content)['encoding']
            return resp.text
        return None


class HTMLParser(object):

    @staticmethod
    def parser(page_url, html):
        """
        :param page_url: 对应的html内容的url地址
        :param html: 下载的html内容
        :return:
        """
        if page_url is None or html is None:
            return

        soup = BeautifulSoup(html, 'lxml')
        # 1. 提取数据
        data = HTMLParser._extract_data(page_url, soup)
        # 2. 提取新链接
        new_urls = HTMLParser._extract_new_urls(page_url, soup)
        return data, new_urls

    @staticmethod
    def _extract_data(page_url, soup):
        data = {}
        # 提取标题
        title = soup.h1.string

        div_paras = soup.find('div', {'class': 'lemma-summary'})
        # 提取摘要
        summary = "".join(div_paras.strings)
        data[page_url] = {'title': title, 'summary': summary}
        return data

    @staticmethod
    def _extract_new_urls(page_url, soup):
        # 提取待爬取的链接
        base = "https://baike.baidu.com/"
        div_paras = soup.find('div', {'class': 'lemma-summary'})
        a = div_paras.find_all('a')
        print(a)
        if a is None:
            return
        # 有的链接没有 href 属性， 要小心处理
        new_urls = {urljoin(base, i.get('href')) for i in a}
        return new_urls


class DataOutput(object):

    def __init__(self):
        # 将数据缓存在内存中
        self.datas = []
        self.DIRs = 'downloads'

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_json(self):
        if not os.path.exists(self.DIRs):
            os.mkdir(self.DIRs)
        file_name = os.path.join(self.DIRs, 'baike.json')

        with open(file_name, 'w') as f:
            json.dump(self.datas, f)

    # TODO other output type
