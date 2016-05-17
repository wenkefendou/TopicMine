#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/21 14:20
从有类别的文章的标题、关键词、摘要数据中抽取出名词词语
          2.利用tf-idf，从每个类别取出若干个关键字（比如前10个），组成词袋
          3.计算每个类别对于词袋中的词的词频（为了避免文章长度的差异，使用相对词频）
          4.生成各个类别的词频向量语料
          5.生成相似度模型
"""
from operator import itemgetter
from gensim import corpora, models, similarities
from GetData.preprocess import getdata, parse_xml, ltp


def get_noun(sql, name, dep_lis):
    all_docs = []
    for dep in dep_lis:
        data = getdata(sql.format(name, dep))
        ss = ""
        for DOC in data:
            title = DOC[0]
            keywords = DOC[1]
            abstract = DOC[2]
            temp = "{};{};{}".format(title, keywords, abstract)
            ss += temp + "\n"
        with open("./data/temp1.txt", "w", encoding='utf-8') as f:
            f.write(ss.rstrip("\n"))
        ltp(r"D:\MyProject\pythonProjects\TopicMine\GetData\geology\data\temp1.txt",
            r"D:\MyProject\pythonProjects\TopicMine\GetData\geology\data\temp2.txt")
        documents = parse_xml("./data/temp2.txt")
        all_docs.append(' '.join(documents))
    return all_docs


def get_corpus(sql, name, dep_lis):
    all_docs = get_noun(sql, name, dep_lis)

    texts = [[word for word in t.split()] for t in all_docs]
    dictionary = corpora.Dictionary(texts)  # 词袋
    corpus_temp = [dictionary.doc2bow(text) for text in texts]  # 向量表示的语料

    # 生成tf-idf模型
    tf_idf = models.TfidfModel(corpus_temp)
    corpus_tf_idf = tf_idf[corpus_temp]
    # 选择最短类别的单词个数
    num = []
    for vec in corpus_tf_idf:
        num.append(len(vec))
    num_min = min(num)

    # 每个类别中抽取前num_min个元素
    new_dict = []
    for vec in corpus_tf_idf:
        aa = []
        bb = list(reversed(sorted(vec, key=itemgetter(1))))
        for num in range(num_min):
            aa.append(dictionary[bb[num][0]])
        new_dict.append(aa)
    dictionary1 = corpora.Dictionary(new_dict)
    dictionary1.save('./data/type.dict')  # 保存为本地词典

    new_corpus = [dictionary1.doc2bow(text) for text in texts]
    # 相对词频 = 某词在文章中出现的次数/文章的总词数
    for v in range(len(new_corpus)):
        for a in range(len(new_corpus[v])):
            temp1 = new_corpus[v][a][1]
            temp2 = new_corpus[v][a][0]
            new_corpus[v][a] = (temp2, temp1 / len(new_corpus[v]))
    corpora.MmCorpus.serialize('./data/type.mm', new_corpus)

    # 生成并保存相似矩阵
    index = similarities.Similarity('./data', new_corpus, num_features=len(dictionary1), num_best=5)
    index.save('./data/sim.index')

if __name__ == '__main__':
    name1 = "李勇"
    # 统计已有的机构类别信息
    depart_list = []
    sql1 = "select author_unique from {0} where author_unique is not NUll;".format(name1)
    for depart in getdata(sql1):
        if depart[0] not in depart_list:
            depart_list.append(depart[0])
    with open("./data/departs.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(depart_list))

    # 生成并本地化保存词典和按词典表示的类别语料
    sql2 = "select title,keywords,abstract from topics.{0} where author_unique = '{1}';"
    get_corpus(sql2, name1, depart_list)