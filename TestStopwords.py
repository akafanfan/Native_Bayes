#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : TestStopwords.py
@Author: Yang Fan
@Date  : 2019/5/5 18:44
@Desc  : 
'''
import os
import codecs
import jieba
import re

FILE_PATH = "D:\\Documents\\PyCharm\\Native_Bayes\\data"
STOPWORDS = codecs.open(os.path.join(FILE_PATH, 'stopwords_cn.txt'), 'r', 'UTF-8').read().split('\r\n')


# 中文测试
def textParseZh(bigString):
    str = jieba.lcut(bigString)
    newStr = [re.sub(r'\W*', '', s) for s in str]
    return [tok.lower() for tok in newStr if len(tok) > 0]


# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('data/stopwords_cn.txt', encoding='UTF-8').readlines()]
    return stopwords


def segmentWords(bigString):
    # 对文档中每一行进行中文分词
    print('正在分词...')
    sentence = jieba.cut(bigString.strip())  # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
    # 注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。
    # 创建一个停用词列表
    stopwords = stopwordslist()
    new_str = ''
    # 过滤停用词
    for word in sentence:
        if word not in stopwords:
            if word != '\t':
                new_str += word
                new_str += " "
    return new_str



docList = []
classList = []
fullText = []
wordlist = textParseZh(open('data/email_zh/spam/1.txt', encoding='UTF-8').read())
docList.append(wordlist)
print(docList)