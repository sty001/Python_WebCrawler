#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tools.py
@Time    :   2020/09/08 21:30:13
@Author  :   STY_lcmg
@Version :   1.0
@Contact :   lcmg.sty@gmail.com
@Desc    :   None
'''

# here put the import lib

import logging

from colorama import Fore


def unverified_ssl():
    """取消全局 ssl 验证"""
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context


class SpiderLogger(logging.Logger):
    """自定义美化输出"""

    def info(self, msg, *args, **kwargs):
        """下载成功"""
        super().info(Fore.GREEN + msg + Fore.RESET, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """下载失败"""
        super().warning(Fore.RED + msg + Fore.RESET, *args, **kwargs)


def get_logger(logger_name):
    """控制台日志输出"""
    logger = SpiderLogger(logger_name)
    logger.setLevel(logging.INFO)
    fmt = "%(name)s - %(asctime)s - %(message)s"
    formatter = logging.Formatter(fmt=fmt, datefmt="%m/%d/%Y %I:%M:%S")
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger
