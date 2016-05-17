#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/26 14:46
"""
import os
import re

from GetData.preprocess import ltp, segment_graph, ltp_cws, ltp_pos, ltp_par
import nltk
import xml.etree.ElementTree as Et


def get_words(path):
    with open(path, 'r', encoding="utf-8") as f:
        xml_raw = f.read().strip().split("\n\n")  # xml文本，可能包含多个xml，用双换行进行切分
    f.close()
    docs = []  # 存储结果
    for doc in xml_raw:
        xml = Et.fromstring(doc)
        doc_words = []
        for sentance in xml.findall('./doc/para/sent'):
            word_list = [words for words in sentance]
            wordsall = []  # 存储句子的匹配结果
            for word in word_list:
                pattern = re.compile(u"([\u4e00-\u9fa5]+)")
                content = word.attrib['cont']
                pos = word.attrib['pos']
                if pattern.search(content) and pos not in ['c', 'd', 'e', 'g', 'o', 'p', 'q', 'r', 'u', 'wp', 'x', 'nd']:
                # if pos != 'wp':
                    wordsall.append(content)
            doc_words.append(wordsall)
        docs.append(doc_words)
    return docs  # 返回整个处理后的文本


def chunk_ngram(file):
    dict1 = {}
    n_gram = 2
    docs = get_words(file)
    for doc in docs:
        for sen in doc:
            if len(sen) > n_gram - 1:
                temp = nltk.ngrams(sen, n_gram)
                for tt in temp:
                    aka = ''.join(tt)
                    if aka not in dict1:
                        dict1[aka] = 1
                    else:
                        num = dict1[aka] + 1
                        dict1[aka] = num
    list1 = list(reversed(sorted(dict1.items(), key=lambda x: x[1])))
    for yz in list1:
        if yz[1] > 1:
            print('%s:%s' % (yz[0], yz[1]))


def get_nounpos(file):
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


def chunk_pos(file):
    doc1 = []
    with open(file, 'r', encoding='utf-8') as f:
        for doc in f.readlines():
            sentence = []
            for words in re.split(' |	|	', doc):
                temp = words.split('_')
                sentence.append((temp[0], temp[1]))
            doc1.append(sentence)
    chunk = []
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
    cp = nltk.RegexpParser(grammar)
    for sent in doc1:
        tree = cp.parse(sent)
        for subtree in tree.subtrees():
            if subtree.label() == 'NP':
                t1 = ''.join([tup[0] for tup in list(subtree)])
                chunk.append(t1)
    newchunk = []
    for item in set(chunk):
        newchunk.append([item, chunk.count(item)])
    newchunk.sort(key=lambda num: num[1], reverse=True)
    nn = 0
    for item1 in newchunk:
        if item1[1] > 0:
            print(item1)
            nn += 1
    print('搭配出现频率大于4的语块个数：%d' % nn)


if __name__ == '__main__':
    # 将文本分句，ltp分词、词性标注
    # with open('data/temp3.txt', 'r', encoding='utf-8') as f:
    #     for doc in f.readlines():
    #         newdoc = segment_graph(doc)
    #         with open('data/new_train.txt', 'a', encoding='utf-8') as f1:
    #             f1.write('%s\n' % newdoc)
    #
    # ltp_par(r"D:\MyProject\pythonProjects\TopicMine\LDA_T\data\segment_jieba.txt",
    #         r"D:\MyProject\pythonProjects\TopicMine\LDA_T\data\parse.txt")

    # n-gram语块统计
    # chunk_ngram('data/temp4.txt')

    # 利用词性规则选取合适的语块,生成包含词性的词块，如“丹池/ns 盆地/n”
    chunk_pos('data/pos.txt')