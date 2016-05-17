#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/26 14:46
"""
import re
from pprint import pprint

import nltk
import xml.etree.ElementTree as Et


# 解析ltp返回的xml文件,保留词语-词形组合
def get_noun_pos_from_xml(file):
    with open(file, 'r', encoding="utf-8") as f:
        xml_raw = f.read().strip().split("\n\n")  # xml文本，可能包含多个xml，用双换行进行切分
    f.close()
    sentences = []  # 存储结果
    for doc in xml_raw:
        xml = Et.fromstring(doc)
        for sentance in xml.findall('./doc/para/sent'):
            word_list = [words for words in sentance]
            sentence = []
            for word in word_list:
                content = word.attrib['cont']
                pos = word.attrib['pos']
                sentence.append((content, pos))
            sentences.append(sentence)
    return sentences  # 返回整个处理后的文本


# 解析ltp返回的txt文件
def get_noun_pos_from_txt(file):
    docs = []
    with open(file, 'r', encoding='utf-8') as f:
        for doc in f.readlines():
            sentence = []
            for words in re.split('\\t', doc):
                temp = words.split('_')
                sentence.append((temp[0], temp[1]))
            docs.append(sentence)
    return docs


# 抽取名词语块
def noun_chunk(file):
    doc1 = get_noun_pos_from_txt(file)
    grammar = r"""
        NP: {<a> <a> <n>}
            {<n.*> <a> <n>}
            {<a> <n.*> <n>}   # 形容词+形容词+名词
            {<n.*> <n.*> <n>}   # 名词所有形式+名词所有形式+名词
            {<n.*> <n>}     # 名词所有形式+名词
            {<b> <n>}       # 其他名词修饰词+名词
            {<a> <n>}       # 形容词+名词

            #{<v> <v> <n>}   # 动词+动词+名词
            # {<m> <a> <n>}   # 数字+形容词+名词
            #{<j> <ns> <n>}  # 缩略词+地名+名词
            # {<m> <n> <n>}   # 数字+名词+名词
            # {<n.*> <v> <n>} # 名词所有形式+动词+名词
    """
    chunk = []
    cp = nltk.RegexpParser(grammar)
    for sent in doc1:
        tree = cp.parse(sent)
        for subtree in tree.subtrees():
            if subtree.label() == 'NP':
                t1 = ''.join([tup[0] for tup in list(subtree)])
                chunk.append(t1)

    new_chunk = []
    for item in set(chunk):
        new_chunk.append([item, chunk.count(item)])
    new_chunk.sort(key=lambda num: num[1], reverse=True)
    nn = 0
    for item1 in new_chunk:
        if item1[1] > 4:
            print(item1)
            nn += 1
    print('搭配出现频率大于4的语块个数：%d' % nn)


if __name__ == '__main__':
    # 利用词性规则选取合适的语块,生成包含词性的词块，如“丹池/ns 盆地/n”
    noun_chunk('data/pos.txt')