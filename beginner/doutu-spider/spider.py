#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   spider.py
@Time    :   2020/09/08 21:29:26
@Author  :   STY_lcmg
@Version :   1.0
@Contact :   lcmg.sty@gmail.com
@Desc    :   None
'''

# here put the import lib

import chardet

import os
import sys
import urllib.request

from bs4 import BeautifulSoup

import tools


class DoutuSpider:
    user_agent = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36")

    def __init__(self):
        self.PICS_DIR = "data/images"
        self.ROOT_URL = "https://www.doutula.com/photo/list/"
        self.LOGGER = tools.get_logger("doutu")

    def _prepare(self):
        """
        准备工作，建立保存数据的目录
        :return:
        """
        if not os.path.exists(self.PICS_DIR):
            os.makedirs(self.PICS_DIR)

    def _download_html(self, url):
        """下载首页的 html 内容

        :return: bytes of html
        """
        req = urllib.request.Request(url)
        # 添加 UA, 否则网站响应403
        req.add_header('User-Agent', self.user_agent)
        resp = urllib.request.urlopen(req)
        return resp.read()

    def _parse_html(self, b_html):
        """解析图片地址

        :param b_html: 网页的字节内容
        :return: 解析好的图片地址列表
        """

        # 检测网页的正确编码格式
        right_encoding = chardet.detect(b_html)['encoding']

        soup = BeautifulSoup(b_html, "html.parser",
                             from_encoding=right_encoding)

        # 提取所有的图片节点
        images = soup.select(".page-content .image_dta")
        # 生成图片链接
        img_urls = [i["data-original"] for i in images]

        return img_urls

    def _save_img(self, img_urls):
        """将图片保存到本地硬盘"""
        imgs = img_urls.copy()
        imgs.append("fjlkdsfjlkdsf")  # 无效链接，测试日志输出
        for i in imgs:
            file_name = os.path.join(self.PICS_DIR, i.split('/')[-1])
            try:
                urllib.request.urlretrieve(i, file_name)
            except Exception as e:
                self.LOGGER.warning("Url: {} download failed".format(i))
            else:
                self.LOGGER.info("Url: {} download success".format(i))

    def run(self):
        """斗图啦爬取流程
        1. 下载首页内容
        2. 获取图片链接
        3. 将图片保存到本地
        """
        self._prepare()
        # Step 1
        b_html = self._download_html(self.ROOT_URL)
        # Step 2
        img_urls = self._parse_html(b_html)
        # Step 3
        self._save_img(img_urls)


if __name__ == "__main__":
    DoutuSpider().run()
