#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/21 21:11

"""
from GetData.geology.evaluate import getlist
from GetData.preprocess import getdata, ltp, parse_xml
from gensim import corpora, similarities


def get_test_corpus(name, dict1):
    sql = "select title,keywords,abstract from topics.{0} where author_unique is NULL;".format(name)
    test_docs = []
    data = getdata(sql)
    for DOC in data:
        title = DOC[0]
        keywords = DOC[1]
        abstract = DOC[2]
        temp = "{};{};{}".format(title, keywords, abstract)
        with open("./data/temp1.txt", "w", encoding='utf-8') as f:
            f.write(temp.rstrip("\n"))
        ltp(r"D:\MyProject\pythonProjects\TopicMine\GetData\geology\data\temp1.txt",
            r"D:\MyProject\pythonProjects\TopicMine\GetData\geology\data\temp2.txt")
        documents = parse_xml("./data/temp2.txt")
        test_docs.append(' '.join(documents))

    texts = [[word for word in t.split()] for t in test_docs]
    corpus_temp = [dict1.doc2bow(text) for text in texts]
    for v in range(len(corpus_temp)):
        for a in range(len(corpus_temp[v])):
            temp1 = corpus_temp[v][a][1]
            temp2 = corpus_temp[v][a][0]
            corpus_temp[v][a] = (temp2, temp1 / len(corpus_temp[v]))
    corpora.MmCorpus.serialize('./data/test_corpus.mm', corpus_temp)


if __name__ == '__main__':
    dictionary = corpora.Dictionary.load('./data/type.dict')
    corpus = corpora.MmCorpus('./data/type.mm')
    depart_list = getlist('./data/departs.txt')

    # 训练测试数据
    name1 = '李勇'
    get_test_corpus(name1, dictionary)

    test_corpus = corpora.MmCorpus('./data/test_corpus.mm')
    id_list = getlist('./data/no_type2.txt')

    # 预测
    index = similarities.Similarity.load('./data/sim.index')
    num_get = 0
    for nn in range(len(index[test_corpus])):
        test_id = id_list[nn]
        if len(index[test_corpus][nn]) == 0:
            print("第{0}篇文章的预测类为:{1}".format(test_id, "未知类别"))
        else:
            num_get += 1
            result = depart_list[index[test_corpus][nn][0][0]]
            # print("{0}:{1}".format(test_id, result))
            with open('./data/sim_match.txt', 'a', encoding='utf-8')as f:
                f.write("{0}:{1}\n".format(test_id, result))
    print('匹配到类别的文章有：%d篇' % num_get)