import re
import jieba
from EmailFiltering import textParse
#切分文本
'''
docList = []
classList = []
fullText = []
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



# 中文测试
def textParseZh(bigString):
    str = jieba.lcut(bigString)
    newStr = [re.sub(r'\W*','',s) for s in str]
    return [tok.lower() for tok in newStr if len(tok) >0]

# mySent = '你好，欢迎来到西安邮电大学。Hello,Welcome to XUPT'
# str = textParseZh(mySent)
# print(str)


docList = []
classList = []
fullText = []
'''
单一文本测试
'''
'''
wordlist = textParseZh(open('email_zh/spam/1.txt' ,encoding='UTF-8').read())
docList.append(wordlist)

print(docList)
'''
for i in range(1,26):
    wordlist = textParse(open('email/ham/%d.txt' % i).read())

    # wordlist = textParseZh(open('email_zh/ham/%d.txt' % i,encoding='UTF-8').read())
    '''
    append() 用于在列表末尾添加新的对象。
    extend() 用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表
    '''
    docList.append(wordlist)
    fullText.extend(wordlist)
    classList.append(1)
    wordlist = textParse(open('email/spam/%d.txt' % i).read())
    # wordlist = textParseZh(open('email_zh/spam/%d.txt' % i,encoding='UTF-8').read())
    docList.append(wordlist)
    fullText.extend(wordlist)
    classList.append(0)

print(docList)
print('---------------------------------------------')
print(fullText)


