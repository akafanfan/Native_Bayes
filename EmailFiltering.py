import numpy as n
import re
import random
import jieba

def createVocabList(dataSet):
    vocabSet = set([]) #利用set数据类型创建一个空集合
    for document in dataSet:#遍历数据集中的每篇文档,将每篇文档返回的新词添加到该集合中
        # | 用于求两个集合的并
        vocabSet = vocabSet | set(document)
    return list(vocabSet) #返回所有文档中出现不重复词的列表

def setOfWords2Vec(vocabList ,inputSet):
    returnVec = [0]*len(vocabList) #创建一个和词汇表等长的向量，并将元素都设为0
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word:'%s' is not in my Vocabulary" %word)
    return returnVec

def trainNB0(trainMatrix , trainlistClasses):
    numTrainDocs = len(trainMatrix) #获取文档数量
    numWords = len(trainMatrix[0])
    #pAbusive侮辱性文档的概率:侮辱性文档的标记为1,对标签向量求和,得到侮辱性文档的数量
    pAbusive = sum(trainlistClasses) / float(numTrainDocs)
    '''
        zeros:0数组  
        ones: 可以创建任意维度和元素个数的数组，其元素值均为1；  
    '''
    #初始化概率
    p0Num = n.ones(numWords)# 初始化单词列表中单词在正常文档中出现的次数
    p1Num = n.ones(numWords) # 初始化单词列表中单词在侮辱性文档中出现的次数

    p0Denom = 2.0   # 正常文档中，词汇表中单词出现的总数
    p1Denom = 2.0

    for i in range(numTrainDocs):     #遍历每篇文档
        if trainlistClasses[i] == 1:#若此篇文档是侮辱性文档
            p1Num += trainMatrix[i]         #若词条在侮辱性文档中出现,则增加该词条的计数值
            p1Denom += sum(trainMatrix[i])  #增加侮辱性文档中出现的词条总数
        else:                       #若此篇文档是非侮辱性文档
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])


    p1Vect = n.log(p1Num/p1Denom)  #词汇表中每个单词在侮辱性文档中出现的概率
    p0Vect = n.log(p0Num/p0Denom)  #词汇表中每个单词在正常文档中出现的概率

    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Classify*p1Vec) + n.log(pClass1)
    p0 = sum(vec2Classify*p0Vec) + n.log(1.0-pClass1)
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
    newStr = [re.sub(r'\W*','',s) for s in str]
    return [tok.lower() for tok in newStr if len(tok) >0]


def spamTest():
    docList = []
    classList = []
    fullText = []

    #导入并解析文本文件
    for i in range(1, 26):
        # wordlist = textParse(open('email/ham/%d.txt' % i).read())
        wordlist = textParseZh(open('email_zh/ham/%d.txt' % i,encoding='UTF-8').read())

        '''
        append() 用于在列表末尾添加新的对象。 
        extend() 用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表
        '''
        docList.append(wordlist)
        fullText.extend(wordlist)
        classList.append(1)
        # wordlist = textParse(open('email/spam/%d.txt' % i).read())
        wordlist = textParseZh(open('email_zh/spam/%d.txt' % i,encoding='UTF-8').read())
        docList.append(wordlist)
        fullText.extend(wordlist)
        classList.append(0)

    vocabList = createVocabList(docList)
    trainingSet =  list(range(50))
    testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex]) #选出文档添加到测试集
        del(trainingSet[randIndex])      #从训练集中剔除
        '''
        python3.x , 出现错误 'range' object doesn't support item deletion
        原因：python3.x   range返回的是range对象，不返回数组对象
        解决方法：
        把 trainingSet = range(50) 改为 trainingSet = list(range(50))
        '''

    trainMat = []
    trainClasses = []
    for j in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[j]))
        trainClasses.append(classList[j])

    p0V,p1V,pSpam = trainNB0(trainMat,trainClasses)
    errorCount = 0
    for i in testSet:
        wordVector = setOfWords2Vec(vocabList,docList[i])
        if classifyNB(wordVector,p0V,p1V,pSpam) != classList[i]:
            errorCount += 1
            print("分类错误的测试集：", docList[i])
    rate = float(errorCount)/len(testSet)
    print("the error rate is:",float(errorCount)/len(testSet))

    return rate
'''
if __name__ == '__main__':
    spamTest()
'''
spamTest()

