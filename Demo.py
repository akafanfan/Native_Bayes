#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : Demo.py
@Author: Yang Fan
@Date  : 2019/5/5 19:04
@Desc  : 
'''
import os
import jieba
import codecs

# 创建停用词列表
FILE_PATH = "D:\\Documents\\PyCharm\\Native_Bayes\\data"
STOPWORDS = codecs.open(os.path.join(FILE_PATH,'stopwords_cn.txt'),'r','UTF-8').read().split('\r\n')
