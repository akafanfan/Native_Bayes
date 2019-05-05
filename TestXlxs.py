#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  : TestXlxs.py
@Author: Yang Fan
@Date  : 2019/5/5 16:37
@Desc  : 利用pandas处理Excel数据的Demo

'''
import pandas #利用pandas处理Excel数据
import os
import codecs
import jieba

# jieba分词，过滤停止词，空字符串，标点
def segmentWords(emailFrame):
    texts = []
    for text in emailFrame["text"]:
        words = []
        seg_list = jieba.cut(text)
        for seg in seg_list:
            if(seg.isalpha())&(seg not in stopword):
                words.append(seg)
        sentance = " ".join(words)
        texts.append(sentance)
    emailFrame["text"] = texts
    return


FILE_PATH = "D:\\Documents\\PyCharm\\Native_Bayes\\data"
emailFrame = pandas.read_excel(os.path.join(FILE_PATH,'EmailDataSet.xlsx'),0)
# 检查数据
txt_head_5= emailFrame.head(5)
# print(txt_head_5)
'''
  type                                               text
0  ham  1506讲的是孔子后人的故事。一个老领导回到家乡，跟儿子感情不和，跟贪财的孙子孔为本和睦。老...
1  ham  那他为什么不愿意起诉，既然这样了！起诉后也有充分的理由！MM莫不是还生活在电影中，个人认为这...
2  ham  我觉得，负债不要紧，最重要的是能负得起这个责任来，\n欠了那么多钱，至少对当初拿出爱心来的网...
3  ham  公司现在有内部推荐机会,2-3人主要从事视频编解码器在pc/dsp/arm上的优化工作.(h...
4  ham  鼓励一下！\n还是让姐姐们给你解答更好吧。\n     赫赫，很少有女生追男生的例子。不过还...
'''
# print("data shape:", emailFrame.shape)
# print("spams in rows:", emailFrame.loc[emailFrame['type'] == "spam"].shape[0])
# print("ham in rows:", emailFrame.loc[emailFrame['type'] == "ham"].shape[0])
'''
data shape: (150, 2)
spams in rows: 50
ham in rows: 100
'''

# 载入停用词
stopword = codecs.open(os.path.join(FILE_PATH,'stopwords_cn.txt'),'r','UTF-8').read().split('\r\n')

# print(stopword)

segmentWords(emailFrame)
ntxt_head_5= emailFrame.head(10)
# print(ntxt_head_5)
'''
  type                                               text
0  ham  讲 孔子 后人 故事 一个 老 领导 回到 家乡 儿子 感情 贪财 孙子 孔为 本 和睦 老...
1  ham  愿意 起诉 起诉 充分 理由 MM 莫不是 生活 电影 中 认为 快 就 结婚 恰恰 对 感...
2  ham  觉得 负债 不要紧 重要 能 负得起 责任 欠 多钱 至少 对 当初 拿出 爱心 网友 交待...
3  ham  公司 现在 内部 推荐 机会 主要 从事 视频 编解码器 pc dsp arm 优化 工作 ...
4  ham  鼓励 一下 姐姐 解答 更好 赫赫 很少 女生 追 男生 例子 想 请 帮帮忙 闹 分手 一...
5  ham  这番话 说明 有心 赞 一下 今天 晚上 gg 我家 回家 时候 开门 外面 闷热 雷声 隆...
6  ham  理解 知道 说 挑是 意思 挑 带 框框 死 条件 传统 社会性 条件 会 条件 不利 改变...
7  ham  成熟 感情 可能 考虑 将来 勇敢 面过 过 逃避 感情 知道 做 每件事 都 选择 应该 ...
8  ham  kill bill 比较 侮辱 武侠片 徐克 片子 青蛇 东方不败 新龙门 蜀山 都 现如今...
9  ham  就 闹 明白 不介意 爸爸妈妈 何干 为啥 要说 呢 谢谢 安慰 确实 难受 苦衷 不敢 妈...

'''

wordList = emailFrame['text'].values.tostring()
print(wordList)
