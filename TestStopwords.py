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
STOPWORDS = codecs.open(os.path.join(FILE_PATH,'stopwords_cn.txt'),'r','UTF-8').read().split('\r\n')

# 中文测试
def textParseZh(bigString):
    str = jieba.lcut(bigString)
    newStr = [re.sub(r'\W*', '', s) for s in str]
    return [tok.lower() for tok in newStr if len(tok) > 0]

def segmentWords(emailFrame):
    texts = []
    for text in emailFrame:
        words = []
        seg_list = jieba.cut(text)
        for seg in seg_list:
            if(seg.isalpha())&(seg not in STOPWORDS):
                words.append(seg)
        sentance = " ".join(words)
        texts.append(sentance)
    return texts


docList = []
classList = []
fullText = []

wordlist = textParseZh(open('email_zh/spam/1.txt', encoding='UTF-8').read())
docList.append(wordlist)
print(docList)


