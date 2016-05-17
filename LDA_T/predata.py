#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/28 9:32
"""
import re
from gensim import corpora, models, similarities
import xml.etree.ElementTree as Et
from GetData.preprocess import getdata, ltp, ltp_pos
from nltk.corpus import WordListCorpusReader
import jieba
import jieba.posseg as pseg
import logging

# 添加停用词
STOP_PATH = r'D:\MyProject\pythonProjects\TopicMine\LDA_T\data\\'
stopwords = set(WordListCorpusReader(STOP_PATH, 'stopwords.txt').words())


#
def parse_lda_xml(file):
    with open(file, 'r', encoding='utf-8') as f:
        xml_raw = f.read().strip().split('\n\n')  # xml文本，可能包含多个xml，用双换行进行切分
    f.close()
    docs = []  # 存储结果
    for doc in xml_raw:
        xml = Et.fromstring(doc)
        doc_words = []
        for sentence in xml.findall('./doc/para/sent'):  # 循环读取句子
            word_list = [words for words in sentence]  # 循环读取word列表
            wordsall = []  # 存储句子的匹配结果
            for word in word_list:  # 循环解析每个word要素
                pattern = re.compile(u'([\u4e00-\u9fa5A-Za-z]+)')
                content = word.attrib['cont']
                if pattern.search(content) and len(content) > 1 and content not in stopwords:
                    wordsall.append(content)
            doc_words.append(' '.join(wordsall))
        docs.append(' '.join(doc_words))
    return docs  # 返回整个处理后的文本


# 从mysql数据库抽取训练数据
def get_paper(name):
    sql = 'select title,keywords,abstract from topics.{0};'.format(name)
    data = getdata(sql)
    for DOC in data:
        title = DOC[0]
        keywords = DOC[1]
        abstract = DOC[2]
        # 获得训练数据
        temp = '{};{};{}'.format(title, keywords, abstract)
        with open('data/temp1.txt', 'a', encoding='utf-8') as f:
            f.write('%s\n' % temp.strip())


# 抽选关键词，删选后可以加入用户词典
def get_keywords(name):
    sql = 'select keywords from topics.{0};'.format(name)
    data = getdata(sql)
    keywords = []
    for doc in data:
        keyword = doc[0]
        if keyword != 'None' and keyword != '':
            for key in re.split(r',|，|;|；|：|:|“|”|"', keyword):
                if len(key) > 1 and key not in keywords:
                    keywords.append(key)
    with open('data/user_dict.txt', 'a', encoding='utf-8') as f:
        f.write('\n'.join(keywords))


# jieba分词、ltp词性分析
def seg_pos():
    jieba.load_userdict('data/user_dict.txt')
    with open('data/temp1.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            with open('data/segment_jieba.txt', 'a', encoding='utf-8') as f:
                f.write(' '.join(jieba.cut(line, cut_all=False, HMM=False)))
    # ltp词性标注
    ltp_pos(r"D:\MyProject\pythonProjects\TopicMine\LDA_T\data\segment_jieba.txt",
            r"D:\MyProject\pythonProjects\TopicMine\LDA_T\data\pos.txt")


# 训练语料
def train_corpus():
    seg_pos()
    # 选取名词词形的词语
    with open('data/pos.txt', 'r', encoding='utf-8') as f:
        for doc in f.readlines():
            line1 = []
            for words in re.split('\\t', doc):
                temp = words.split('_')
                if temp[1].startswith('n') or temp[1] in ['i', 'j']:
                    if temp[0] not in stopwords and len(temp[0]) > 1:
                        line1.append(temp[0])
            with open('data/noun2.txt', 'a', encoding='utf-8') as ff:
                ff.write(' '.join(line1) + '\n')


if __name__ == "__main__":
    name1 = '杜远生'
    # get_paper(name1)
    train_corpus()
