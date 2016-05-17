#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/28 9:32
"""
import re
from collections import defaultdict

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


def lda_parse_xml(path):
    with open(path, 'r', encoding='utf-8') as f:
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
                pos = word.attrib['pos']
                if pattern.search(content) and len(content) > 1 and content not in stopwords:
                    wordsall.append(content)
            doc_words.append(' '.join(wordsall))
        docs.append(' '.join(doc_words))
    return docs  # 返回整个处理后的文本


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
        # 将关键词单独去除，删选后可以加入用户词典
        keylist = []
        if keywords != 'None' and keywords != '':
            for key in re.split(r',|，|;|；|：|:|“|”|"', keywords):
                if len(key) > 1 and key not in keylist:
                    keylist.append(key)
        with open('data/keywords.txt', 'a', encoding='utf-8') as f:
            f.write('\n'.join(keylist))


def train_corpus():
    documents = []
    # jieba.load_userdict('data/userdict.txt')
    # with open('data/temp1.txt', 'r', encoding='utf-8') as f:
    #     for line in f.readlines():
    #         documents.append(list(jieba.cut(line.strip('\n'), cut_all=False, HMM=False)))
    #         with open('data/segment_jieba.txt', 'a', encoding='utf-8') as f:
    #             f.write(' '.join(jieba.cut(line, cut_all=False, HMM=False)))
    # # 选取名词
    # ltp_pos(r"D:\MyProject\pythonProjects\TopicMine\LDA_T\data\segment_jieba.txt",
    #         r"D:\MyProject\pythonProjects\TopicMine\LDA_T\data\pos.txt")
    with open('data/pos.txt', 'r', encoding='utf-8') as f:
        for doc in f.readlines():
            line1 = []
            for words in re.split(' |	|	', doc):
                temp = words.split('_')
                if temp[1].startswith('n') or temp[1] in ['i','j']:
                    line1.append(temp[0])
            documents.append(line1)
            # with open('data/noun2.txt', 'a', encoding='utf-8') as ff:
            #     ff.write(' '.join(line1) + '\n')

    texts = [[word for word in t if len(word) > 1 and word not in stopwords] for t in documents]
    # 删除词频为1的单词
    # frequency = defaultdict(int)
    # for text in texts:
    #     for token in text:
    #         frequency[token] += 1
    # texts = [[token for token in text if frequency[token] > 1]
    #          for text in texts]
    dictionary = corpora.Dictionary(texts)
    dictionary.save('data/dys.dict')
    corpus = [dictionary.doc2bow(text) for text in texts]  # 向量表示的语料
    corpora.MmCorpus.serialize('data/dys.mm', corpus)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    tfidf = models.TfidfModel(corpus)  # 生成tf-idf模型
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus_tfidf, num_topics=10, id2word=dictionary)
    topics = lda.show_topics(10, 10)
    for topic in topics:
        print(topic)

if __name__ == "__main__":
    name1 = '杜远生'
    # get_paper(name1)
    train_corpus()
