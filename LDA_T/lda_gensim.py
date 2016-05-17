# coding=utf-8
import logging, bz2

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
from gensim import corpora, models, similarities


def cos_dist(a, b):
    if len(a) != len(b):
        return None
    part_up = 0.0
    a_sq = 0.0
    b_sq = 0.0
    for a1, b1 in zip(a,b):
        part_up += a1*b1    # 分子为向量的点乘积的和
        a_sq += a1**2
        b_sq += b1**2
    part_down = sqrt(a_sq*b_sq)    # 分母为向量的模的积
    if part_down == 0.0:
        return None
    else:
        return part_up / part_down


def lda_test(numbers):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    dict1 = corpora.Dictionary.load('./data/dys.dict')
    corpus1 = corpora.MmCorpus('./data/dys.mm')
    # lda模型训练
    tfidf = models.TfidfModel(corpus1)  # 生成tf-idf模型
    corpus_tfidf = tfidf[corpus1]
    lda = models.LdaModel(corpus_tfidf, num_topics=numbers, id2word=dict1)
    topics = lda.show_topics(numbers, len(dict1), formatted=False)
    return topics


def average_sim(numbers):
    lists = lda_test(numbers)
    if numbers == 2:
        li1 = [num[0] for num in sorted(lists[0], key=lambda li: li[1])]
        li2 = [num[0] for num in sorted(lists[1], key=lambda li: li[1])]
        cos_sim = cos_dist(li1, li2)
        return cos_sim
    else:
        all_sim = 0
        for j in range(numbers-1):
            for m in range(j+1, numbers):
                li1 = [num[0] for num in sorted(lists[j], key=lambda li: li[1])]
                li2 = [num[0] for num in sorted(lists[m], key=lambda li: li[1])]
                cos_sim = cos_dist(li1, li2)
                all_sim += cos_sim
        return all_sim / (numbers*(numbers-1)/2)

if __name__ == "__main__":
    # lda测试
    # for tt in lda_test(4):
    #     print(sorted(tt, key=lambda li: li[1]))

    # 计算不同主题个数下各主题间的平均余弦相似度
    list_sim = []
    for i in range(2, 15):
        num_topics = i
        sim = average_sim(num_topics)
        list_sim.append(sim)
    for tu in list_sim:
        print(tu)

    # 绘出趋势图
    x1 = [i for i in range(2, 15)]
    y1 = list_sim
    plt.plot(x1, y1, 'r.-')
    plt.xlabel('number of topics')
    plt.ylabel('average sim')
    plt.ylim(0.4, 1.0)
    plt.show()