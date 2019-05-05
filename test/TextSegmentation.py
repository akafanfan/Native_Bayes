import re
from Native_Bayes_Email import textParse
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

docList = []
classList = []
fullText = []

# for i in range(1,26):
#     wordlist = textParse(open('email/ham/%d.txt' % i).read())
#
#     '''
#     # append() 用于在列表末尾添加新的对象。
#     # extend() 用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表
#     '''
#     docList.append(wordlist)
#     fullText.extend(wordlist)
#     classList.append(1)
#     wordlist = textParse(open('email/spam/%d.txt' % i).read())
#     docList.append(wordlist)
#     fullText.extend(wordlist)
#     classList.append(0)
#
# print(docList)


'''
ham/6.txt 中
存在URL：http://www.google.com/support/sites/bin/answer.py?hl=en&answer=90563

'''
wordlist = textParse(open('email/ham/6.txt').read())
docList.append(wordlist)
print(docList)

