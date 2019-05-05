import re
from Native_Bayes_Email import textParse
#切分文本
'''
mySent = 'This book is the best book on Python or M.L. I have ever laid eyes upon.'
#利用正则表达式来切分句子，其中分隔符是除数字单词外的任意字符串
reg = re.compile('\\W')
str = reg.split(mySent)
print(str)
new_str = [tok for tok in str if len(tok)>0]
print(new_str)
new_str = [tok.lower() for tok in str if len(tok)>0]
print(new_str)

'''
docList = []
classList = []
fullText = []

for i in range(1, 26):  # 遍历25个txt文件
    wordList = textParse(open('email/spam/%d.txt' % i).read())  # 读取每个垃圾邮件，并字符串转换成字符串列表
    docList.append(wordList)
    fullText.extend(wordList)
    classList.append(1)  # 标记垃圾邮件，1表示垃圾文件
    wordList = textParse(open('email/ham/%d.txt' % i).read())  # 读取每个非垃圾邮件，并字符串转换成字符串列表
    docList.append(wordList)
    fullText.extend(wordList)
    classList.append(0)  # 标记正常邮件，0表示正常文件

print(docList)
print('-----------------------------')
print(fullText)
