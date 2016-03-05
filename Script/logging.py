#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-01-29 09:23:38
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import os
import logging
# 创建一个logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)
# 记录一条日志
logger.info('foorbar')

#logging.basicConfig(filename='log.txt',level=logging.INFO)
#formatter = logging.Formatter('%(levelname)s[%(asctime)s]:%(message)s',datefmt='%Y-%m-%d %H:%M:%S'))
#示例
def initlog():
    import logging
    mylog = logging.getLogger()
    mylog.setLevel(logging.DEBUG)
    fh = logging.FileHandler(os.path.join('C:\\Users\\Administrator\\Desktop','OutPut.log' ))
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)3s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    mylog.addHandler(fh)
    return mylog
logging = initlog()
logging.info('foorbar')