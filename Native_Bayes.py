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

'''
#输入 数据集
#返回 词汇表(包含在所有文档中出现的不重复词的列表)
#利用set结构的特点建立一个词汇库不包含重复元素 set存储的是无序集合
'''
def createVocabList(dataSet):
    vocabSet = set([]) #利用set数据类型创建一个空集合
    for document in dataSet:#遍历数据集中的每篇文档,将每篇文档返回的新词添加到该集合中
        # | 用于求两个集合的并
        vocabSet = vocabSet | set(document)
    return list(vocabSet) #返回所有文档中出现不重复词的列表

'''
输入 词汇表，某个文档
输出 文档向量，向量每一个元素为1或0 分别表示词汇中的单词在输入文档中是否出现过
     创建一个和词汇表等长的向量，并将元素都设置为0
     遍历文档中所有单词，如果出现了词汇表中的单词，则将输出的文档向量中对应值设置为1，表示词汇表中这个单词在文档中出现了
     否则检查某个词是否在 vocablist中。
'''
def setOfWords2Vec(vocabList ,inputSet):
    returnVec = [0]*len(vocabList) #创建一个和词汇表等长的向量，并将元素都设为0
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word:'%s' is not in my Vocabulary" %word)
    return returnVec


'''朴素贝叶斯分类器训练函数 即训练算法：从词向量计算概率
 上述代码展示了如何将一组单词转换为一组数字，接下来使用这些数字计算概率


'''
'''
输入：文档矩阵（由文档向量构成），每篇文档类别标签所构成的向量，
        即已经知道每篇文档是否属于侮辱性文档了。
输出：p(w|c_0)正常文档中词汇表中单词出现的概率、p(w|c_1)侮辱性文档中词汇表中单词出现的概率、
        任意文档属于侮辱性文档的概率p(c_1)。
'''
def trainNB0(trainMatrix , trainlistClasses):
    print(trainlistClasses)
    numTrainDocs = len(trainMatrix) #获取文档数量
    print("获取文档数量numTrainDocs：",numTrainDocs)
    numWords = len(trainMatrix[0])
    print("每篇文档的单词量（矩阵的列）numWords：",numWords)
    #pAbusive侮辱性文档的概率:侮辱性文档的标记为1,对标签向量求和,得到侮辱性文档的数量
    print("侮辱性文档的数量：",sum(trainlistClasses))
    pAbusive = sum(trainlistClasses) / float(numTrainDocs)
    print("pAbusive：",pAbusive)
    '''
        zeros:0数组  
        ones: 可以创建任意维度和元素个数的数组，其元素值均为1；  
    '''
    #初始化概率
    p0Num = ones(numWords) # 初始化单词列表中单词在正常文档中出现的次数
    p1Num = ones(numWords) # 初始化单词列表中单词在侮辱性文档中出现的次数

    p0Denom = 2.0   # 正常文档中，词汇表中单词出现的总数
    p1Denom = 2.0

    for i in range(numTrainDocs):     #遍历每篇文档
        if trainlistClasses[i] == 1:#若此篇文档是侮辱性文档
            p1Num += trainMatrix[i]         #若词条在侮辱性文档中出现,则增加该词条的计数值
            p1Denom += sum(trainMatrix[i])  #增加侮辱性文档中出现的词条总数
        else:                       #若此篇文档是非侮辱性文档
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    print("p1Num:", p1Num)
    print("p0Num:",p0Num)
    print("p1Denom:",p1Denom)
    print("p0Denom:",p0Denom)

    p1Vect = log(p1Num/p1Denom)  #词汇表中每个单词在侮辱性文档中出现的概率
    p0Vect = log(p0Num/p0Denom)  #词汇表中每个单词在正常文档中出现的概率

    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Classify*p1Vec)+log(pClass1)
    p0 = sum(vec2Classify*p0Vec)+log(1.0-pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

#main
listOposts , listClasses = loadDataSet()
#初始状态
print("词条切分后的文档集合:\n",listOposts)
print("文档类别标签集合:\n",listClasses)

myVocabList=createVocabList(listOposts)
print("在数据集包含的所有文档中出现的不重复词的列表（无序）myVocabList:\n",myVocabList)
print("列表长度:",len(myVocabList))
# demolistOposts = ['life','is','short','I','use','python'];
mywordsVec=setOfWords2Vec(myVocabList,listOposts[0])
# mywordsVec=setOfWords2Vec(myVocabList,demolistOposts)
print("文档中是否出现了所给的单词列表中的元素\n",mywordsVec)

print("------------------------------------------------------------------")

#构建一个包含所有词的列表 myVocabList
'''获取文档矩阵：列数固定，等于单词列表的长度；行数表示数据集中包含文档的数量'''
trainMat=[]
for i in listOposts:
    print("\n",i)
    trainMat.append(setOfWords2Vec(myVocabList,i))
print("文档矩阵：\n",trainMat)
p0V, p1V, pAb = trainNB0(trainMat,listClasses) #trainMat：文档矩阵，listClasses：标签列表
print("任意文档属于侮辱性文档的概率pAB：\n",pAb)
print("在侮辱性文档中词汇表中单词的出现概率p1v：\n",p1V)
print("在正常文档中词汇表中单词的出现概率p0v：\n",p0V)

# 样本1
print("样本1:")
testEntry = ['love','my','dalmation']
thisDoc = setOfWords2Vec(myVocabList,testEntry)
print(testEntry,'classified as:',classifyNB(thisDoc,p0V,p1V,pAb))
#样本2
print("样本2:")
testEntry = ['stupid','garbage']
thisDoc = setOfWords2Vec(myVocabList,testEntry)
print(testEntry,'classified as:',classifyNB(thisDoc,p0V,p1V,pAb))