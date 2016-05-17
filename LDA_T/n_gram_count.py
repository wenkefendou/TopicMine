# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/5/17 16:38
"""
import re
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
                    wordsall.append(content)
            doc_words.append(wordsall)
        docs.append(doc_words)
    return docs  # 返回整个处理后的文本


def chunk_n_gram(file):
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

if __name__ == '__main__':
    # n-gram语块统计
    chunk_n_gram('data/temp4.txt')