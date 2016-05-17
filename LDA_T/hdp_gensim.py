#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/24 18:44
"""
from gensim import corpora, models
import logging

if __name__ == '__main__':
    dict1 = corpora.Dictionary.load(u'data/dys.dict')
    corpus1 = corpora.MmCorpus(u'data/dys.mm')

    # hdp模型训练
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    tfidf = models.TfidfModel(corpus1)
    corpus_tfidf = tfidf[corpus1]
    hdp = models.HdpModel(corpus_tfidf, id2word=dict1)
    hdp.print_topics(topics=-1)