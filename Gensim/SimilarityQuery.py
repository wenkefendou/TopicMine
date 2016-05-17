import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities

dictionary = corpora.Dictionary.load('./data/test.dict')
print(len(dictionary))
corpus = corpora.MmCorpus('./data/test.mm')
# lsi = models.LsiModel(corpus, num_topics=2, id2word=dictionary)

doc = "Human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())

hdp = models.HdpModel.load('./data/model.hdp')
vec_hdp = hdp[vec_bow]
index = similarities.Similarity('./data/hdp', hdp[corpus], num_features=12)
for sim in index:
    print(sim)