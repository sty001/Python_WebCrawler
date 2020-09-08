#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spider.py
@Time    :   2020/09/08 21:30:40
@Author  :   STY_lcmg
@Version :   1.0
@Contact :   lcmg.sty@gmail.com
@Desc    :   None
'''

# here put the import lib

from .spider_utils import UrlManger
from .spider_utils import HTMLDownloader
from .spider_utils import HTMLParser
from .spider_utils import DataOutput


class SpiderMan(object):
    def __init__(self, root_url):
        self.root_url = root_url
        self.url_manager = UrlManger()
        self.html_downloader = HTMLDownloader()
        self.data_output = DataOutput()

    def crawl(self):
        # 将根入口添加到url管理器的待爬取集合中
        self.url_manager.add_new_url(self.root_url)

        while self.url_manager.old_urls_size != 100:
            # 判断是否有待爬取的url
            if self.url_manager.has_new_url():
                # 获取一个未爬取的url链接
                new_url = self.url_manager.get_new_url()
                # 交给 HTML 下载器取访问这个链接， 拿到下载好的html字符串文本
                html_text = self.html_downloader.download(new_url)
                # 将 html_text 交给HTML解析器取提取数据，和包含的新链接
                data, new_urls = HTMLParser.parser(new_url, html_text)
                # 把数据交给数据存储器
                self.data_output.store_data(data)
                # 把链接添加到url管理器中的待爬取链接集合
                self.url_manager.add_new_urls(new_urls)
        self.data_output.output_json()


def main():
    root_url = "https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB"
    spider = SpiderMan(root_url)
    spider.crawl()


if __name__ == "__main__":
    main()
