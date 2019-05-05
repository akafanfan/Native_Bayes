import re
import jieba

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
    wordlist = textParseZh(open('email_zh/spam/1.txt' ,encoding='UTF-8').read())
    docList.append(wordlist)
    
    print(docList)
'''
for i in range(1,26):
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

print(docList)
print('---------------------------------------------')
print(fullText)


