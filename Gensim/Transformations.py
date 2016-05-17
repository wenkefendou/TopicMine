import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities

dictionary = corpora.Dictionary.load('./data/test.dict')
corpus = corpora.MmCorpus('./data/test.mm')
# print(corpus)

# 从一种向量表示转换为另外一种
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]  # 对所有语料进行tfidf转换，更常用语新的语料的转换
# for doc in corpus_tfidf:
#     print(doc)

# LSI模型的转换
# lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
# corpus_lsi = lsi[corpus_tfidf]  # 语料转换词序：bow->tfidf->fold-in-lsi
# for doc in corpus_lsi:
#     print(doc)
# lsi.save('./data/modeltest.lsi')    # 保存训练的模型

# LDA模型的转换
# lda = models.LdaModel(corpus, num_topics=2, id2word=dictionary)
# lda.save('./data/model.lda')

# HDP模型的转换
# hdp = models.HdpModel(corpus, id2word=dictionary)
# hdp.save('./data/model.hdp')




