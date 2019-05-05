import re
import jieba
import os
import codecs

FILE_PATH = "D:\\Documents\\PyCharm\\Native_Bayes\\data"
STOPWORDS = codecs.open(os.path.join(FILE_PATH, 'stopwords_cn.txt'), 'r', 'UTF-8').read().split('\r\n')


# 中文测试
def textParseZh(bigString):
    str = jieba.lcut(bigString)
    newStr = [re.sub(r'\W*','',s) for s in str]
    return [tok.lower() for tok in newStr if len(tok) >0]

# mySent = '你好，欢迎来到西安邮电大学。Hello,Welcome to XUPT'
# str = textParseZh(mySent)
# print(str)

# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('data/stopwords_cn.txt', encoding='UTF-8').readlines()]
    return stopwords


def delStopwords(fullText):
    newList = []
    stopwords = stopwordslist()
    for word in fullText:
        if word not in stopwords:
            newList.append(word)
    return newList

docList = []
classList = []
fullText = []

'''
wordlist = textParseZh(open('data/email_zh/spam/demo.txt' ,encoding='UTF-8').read())
temp.extend(wordlist)
temp = delStopwords(temp)

docList.extend(temp)
print(docList)
'''
'''
demo.txt :我有很多论文

['我', '有', '很多', '论文']
['论文']

'''

'''
append() 用于在列表末尾添加新的对象。 
extend() 用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表
'''

#导入并解析文本文件
for i in range(1, 26): # 遍历25个txt文件
    temp1 = []
    # 读取每个垃圾邮件，并字符串转换成字符串列表
    wordlist1 = textParseZh(open('data/email_zh/ham/%d.txt' % i,encoding='UTF-8').read())
    temp1.extend(wordlist1)
    temp1 = delStopwords(temp1)
    print("temp1:\n", temp1)
    docList.append(temp1)

    temp2 = []
    wordlist2 = textParseZh(open('data/email_zh/spam/%d.txt' % i,encoding='UTF-8').read())
    temp2.extend(wordlist2)
    temp2 = delStopwords(temp2)
    print("temp2\n",temp2)
    docList.append(temp2)


print("docList:\n",docList)


