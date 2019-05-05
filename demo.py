#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : demo.py
@Author: Yang Fan
@Date  : 2019/5/5 21:03
@Desc  : 
'''
import numpy as n
import re
import random
import jieba

"""
函数说明:将切分的实验样本词条整理成不重复的词条列表，也就是词汇表
Parameters:
    dataSet - 整理的样本数据集
Returns:
    vocabSet - 返回不重复的词条列表，也就是词汇表
"""


def createVocabList(dataSet):
    vocabSet = set([])  # 利用set数据类型创建一个空集合
    for document in dataSet:  # 遍历数据集中的每篇文档,将每篇文档返回的新词添加到该集合中
        # | 用于求两个集合的并
        vocabSet = vocabSet | set(document)
    return list(vocabSet)  # 返回所有文档中出现不重复词的列表


"""
函数说明:根据vocabList词汇表，将inputSet向量化，向量的每个元素为1或0
Parameters:
    vocabList - createVocabList返回的列表
    inputSet - 切分的词条列表
Returns:
    returnVec - 文档向量,词集模型
"""


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)  # 创建一个和词汇表等长的向量，并将元素都设为0
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word:'%s' is not in my Vocabulary" % word)
    return returnVec


"""
函数说明:朴素贝叶斯分类器训练函数
Parameters:
    trainMatrix - 训练文档矩阵，即setOfWords2Vec返回的returnVec构成的矩阵
    trainCategory - 训练类别标签向量，即loadDataSet返回的classVec
Returns:
    p0Vect - 正常邮件类的条件概率数组
    p1Vect - 垃圾邮件类的条件概率数组
    pAbusive - 文档属于垃圾邮件类的概率
"""


def trainNB0(trainMatrix, trainlistClasses):
    numTrainDocs = len(trainMatrix)  # 获取文档数量
    numWords = len(trainMatrix[0])
    # pAbusive侮辱性文档的概率:侮辱性文档的标记为1,对标签向量求和,得到侮辱性文档的数量
    pAbusive = sum(trainlistClasses) / float(numTrainDocs)
    '''
        zeros:0数组  
        ones: 可以创建任意维度和元素个数的数组，其元素值均为1；  
    '''
    # 初始化概率
    p0Num = n.ones(numWords)  # 初始化单词列表中单词在正常文档中出现的次数
    p1Num = n.ones(numWords)  # 初始化单词列表中单词在侮辱性文档中出现的次数

    p0Denom = 2.0  # 正常文档中，词汇表中单词出现的总数
    p1Denom = 2.0  # 分母初始化为2 ,拉普拉斯平滑

    for i in range(numTrainDocs):  # 遍历每篇文档
        if trainlistClasses[i] == 1:  # 若此篇文档是侮辱性文档
            # 统计属于侮辱类的条件概率所需的数据，即P(w0|1),P(w1|1),P(w2|1)···
            p1Num += trainMatrix[i]  # 若词条在侮辱性文档中出现,则增加该词条的计数值
            p1Denom += sum(trainMatrix[i])  # 增加侮辱性文档中出现的词条总数
        else:  # 若此篇文档是非侮辱性文档
            # 统计属于非侮辱类的条件概率所需的数据，即P(w0|0),P(w1|0),P(w2|0)···
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    # 取对数，防止下溢出
    p1Vect = n.log(p1Num / p1Denom)  # 词汇表中每个单词在侮辱性文档中出现的概率
    p0Vect = n.log(p0Num / p0Denom)  # 词汇表中每个单词在正常文档中出现的概率

    # 返回属于正常邮件类的条件概率数组，属于侮辱垃圾邮件类的条件概率数组，文档属于垃圾邮件类的概率
    return p0Vect, p1Vect, pAbusive


"""
函数说明:朴素贝叶斯分类器分类函数
Parameters:
	vec2Classify - 待分类的词条数组
	p0Vec - 正常邮件类的条件概率数组
	p1Vec - 垃圾邮件类的条件概率数组
	pClass1 - 文档属于垃圾邮件的概率
Returns:
	0 - 属于正常邮件类
	1 - 属于垃圾邮件类
"""


def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + n.log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + n.log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0


"""
函数说明:接收一个大字符串并将其解析为字符串列表
"""


def textParse(String):  # 将字符串转换为字符列表
    listOfTokens = re.split(r'\W', String)  # 将特殊符号作为切分标志进行字符串切分，即非字母、非数字
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]  # 除了单个字母，例如大写的I，其它单词变成小写


'''
Python有个强大的中文处理模块 jieba，它不仅能对中文文本切词，如果碰到英文单词，也会以英文的默认形式切分。
'''


def textParseZh(bigString):
    str = jieba.lcut(bigString)
    newStr = [re.sub(r'\W*', '', s) for s in str]
    return [tok.lower() for tok in newStr if len(tok) > 0]


'''
创建停用词列表，过滤停用词
'''


def stopwordslist():
    stopwords = [line.strip() for line in open('data/stopwords_cn.txt', encoding='UTF-8').readlines()]
    return stopwords


def delStopwords(fullText):
    newList = []
    stopwords = stopwordslist()
    for i in fullText:
        if i not in stopwords:
            newList.append(i)
    return newList


"""
函数说明:测试朴素贝叶斯分类器，使用朴素贝叶斯进行交叉验证
"""


def spamTest():
    docList = []
    classList = []
    # 导入并解析文本文件
    for i in range(1, 26):  # 遍历25个txt文件
        temp1 = []
        # 读取每个垃圾邮件，并字符串转换成字符串列表
        wordlist1 = textParseZh(open('data/email_zh/ham/%d.txt' % i, encoding='UTF-8').read())
        temp1.extend(wordlist1)
        temp1 = delStopwords(temp1)
        docList.append(temp1)
        classList.append(0)  # 标记垃圾邮件，1表示垃圾文件

        temp2 = []
        wordlist2 = textParseZh(open('data/email_zh/spam/%d.txt' % i, encoding='UTF-8').read())
        temp2.extend(wordlist2)
        temp2 = delStopwords(temp2)
        docList.append(temp2)
        classList.append(1)  # 标记正常邮件，0表示正常文件

    vocabList = createVocabList(docList)  # 创建词汇表，不重复
    trainingSet = list(range(50))
    testSet = []  # 创建存储训练集的索引值的列表和测试集的索引值的列表
    for i in range(10):  # 从50个邮件中，随机挑选出40个作为训练集,10个做测试集
        randIndex = int(random.uniform(0, len(trainingSet)))  # 随机选取索索引值
        testSet.append(trainingSet[randIndex])  # 选出文档添加到测试集
        del (trainingSet[randIndex])  # 从训练集中剔除

    trainMat = []
    trainClasses = []  # 创建训练集矩阵和训练集类别标签系向量
    for j in trainingSet:  # 遍历训练集
        trainMat.append(setOfWords2Vec(vocabList, docList[j]))  # 将生成的词集模型添加到训练矩阵中
        trainClasses.append(classList[j])  # 将类别添加到训练集类别标签系向量中
    p0V, p1V, pSpam = trainNB0(trainMat, trainClasses)  # 训练朴素贝叶斯模型
    errorCount = 0  # 错误分类计数
    for i in testSet:  # 遍历测试集
        wordVector = setOfWords2Vec(vocabList, docList[i])  # 测试集的词集模型
        if classifyNB(wordVector, p0V, p1V, pSpam) != classList[i]:  # 如果分类错误
            errorCount += 1  # 错误计数加1
            print("分类错误的测试集：", docList[i])
    rate = float(errorCount) / len(testSet)
    # print("错误率:",float(errorCount)/len(testSet))

    return rate

'''
if __name__ == '__main__':
    spamTest()

'''

count = 0.0
for i in range(1,11):
    rate = spamTest()
    print('样本%d错误率:' %i, rate)
    count = count + rate
print("-----------------------------------------------------")
print('项目平均错误率：' ,round( count/10 , 4))

'''
问题：
    python3.x , 出现错误 'range' object doesn't support item deletion
原因：
    python3.x   range返回的是range对象，不返回数组对象
解决方法：
    把 trainingSet = range(50) 改为 trainingSet = list(range(50))


'''

