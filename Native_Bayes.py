#从文本中构建词向量
import sys
from numpy import *



#创建了一些实验样本。
def loadDataSet():
    DemoList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],         #1 0
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],    #2 1
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],       #3 0
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],             #4 1
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'], #5 0
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]          #6 1
    classVec = [0,1,0,1,0,1] #1 代表侮辱性文字 0 代表正常言论
    # 返回的第一个变量是进行词条切分后的文档集合
    # 返回的第二个变量是一个文档类别标签的集合。
    return DemoList,classVec


#输入 数据集
#返回 词汇表(包含在所有文档中出现的不重复词的列表)
def createVocabList(dataSet):
    vocabSet = set([]) #利用set数据类型创建一个空集合
    for document in dataSet:#遍历数据集中的每篇文档,将每篇文档返回的新词添加到该集合中
        # | 用于求两个集合的并
        vocabSet = vocabSet | set(document)
    return list(vocabSet) #返回所有文档中出现不重复词的列表

#输入 词汇表，某个文档
#输出 文档向量，向量每一个元素为1或0 分别表示词汇中的单词在输入文档中是否出现过

def setOfWords2Vec(vocabList ,inputSet):
    returnVec = [0]*len(vocabList) #创建一个和词汇表等长的向量，并将元素都设为0
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word :%s is not in my Vocabulary" %word)
    return returnVec

#朴素贝叶斯分类器训练函数 即训练算法：从词向量计算概率
def trainNB0(trainMatrix , trainCategory):
    numTrainDocs = len(trainMatrix)
    print("获取文档数量：",numTrainDocs)
    numWords = len(trainMatrix[0])
    print("每篇文档的单词量，也是矩阵的列：",numWords)
    pAbusive = sum(trainCategory) / float(numTrainDocs)

    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0

    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])

    p1Vect = log(p1Num / p1Denom)
    p0Vect = log(p0Num / p0Denom)

    return p0Vect,p1Vect,pAbusive


#main
listOposts , listClasses = loadDataSet()
print("词条切分后的文档集合:\n",listOposts)
print("文档类别标签集合:\n",listClasses)
myVocabList=createVocabList(listOposts)
print("在数据集包含的所有文档中出现的不重复词的列表:\n",myVocabList)
print("列表长度:",len(myVocabList))
mywordsVec=setOfWords2Vec(myVocabList,listOposts[0])
print("文档1：",listOposts[0])
print("文档中是否出现了所给的单词列表中的元素\n",mywordsVec)
print("列表长度:",len(mywordsVec))

print("++++++++++++++++++++++++++++++++++++++++++++++++++")

#构建一个包含所有词的列表 myVocabList
'''获取文档矩阵：列数固定，等于单词列表的长度；行数表示数据集中包含文档的数量'''
trainMat=[]
for postinDoc in listOposts:
    trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
print("文档矩阵：每篇文档中是否出现了单词列表中的元素:\n", trainMat)
p0V, p1V, pAb=trainNB0(trainMat, listClasses)
print("任意文档属于侮辱性文档的概率pAB：\n",pAb)
print("在侮辱性文档中词汇表中单词的出现概率p1v：\n",p1V)
print("在正常文档中词汇表中单词的出现概率p0v：\n",p0V)