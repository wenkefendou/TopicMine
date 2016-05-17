import logging
from pprint import pprint
from collections import defaultdict

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities

# 简单的预料生成展示
documents = ["Human machine interface for lab abc computer applications",
             "A survey of user opinion of computer system response time",
             "The EPS user interface management system",
             "System and human system engineering testing of EPS",
             "Relation of user perceived response time to error measurement",
             "The generation of random binary unordered trees",
             "The intersection graph of paths in trees",
             "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

stoplist = set('for a of the and to in'.split())  # 简单的停用词表
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]  # 给文档中的文档去除停用词
# 删除词频为1的单词
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
texts = [[token for token in text if frequency[token] > 1]
         for text in texts]
pprint(texts)   # 打印texts
# # 将语料处理后的单词保存为词典
# dictionary = corpora.Dictionary(texts)
# dictionary.save('./data/test.dict')  # 保存为本地词典
# dictionary = corpora.Dictionary.load('./data/test.dict')
# print(dictionary)
# print(dictionary.token2id)  # 输出单词对应的编号
# # 将语料按照词典转换为向量
# corpus = [dictionary.doc2bow(text) for text in texts]
# # print(corpus)
# corpora.MmCorpus.serialize('./data/test.mm', corpus)  # 将训练语料本地化存储
# corpus = corpora.MmCorpus('./data/test.mm')  # 从本地读入语料
# print(list(corpus))
# for doc in corpus:
#     print(doc)


# 内存友好的语料生成方式
# 内存不受限的词典生成方式
stoplist = set('for a of the and to in'.split())  # 简单的停用词表
dictionary = corpora.Dictionary(line.lower().split() for line in open('./data/mycorpus.txt'))
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
            if stopword in dictionary.token2id]
once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.items() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids)  # 删除停用词和单个词
dictionary.compactify()  # 去除删除单词后留下的空白
#
#
# # 从文档中循环读入数据
# class MyCorpus(object):
#     def __iter__(self):
#         for line in open('./data/mycorpus.txt'):
#             # txt中一行代表一篇文章，单词有空格分隔
#             yield dictionary.doc2bow(line.lower().split())
#
#
# corpus_memory_friendly = MyCorpus()
# for vector in corpus_memory_friendly:
#     print(vector)
# 其他格式的语料存储
# corpora.LowCorpus.serialize('./data/test.low', corpus_memory_friendly)  # GibbsLDA++格式目前不能使用，显示MyCorpus没有len
# corpora.BleiCorpus.serialize('./data/test.lda-c', corpus_memory_friendly)  # Blei’s LDA_T-C格式可以使用
# corpus = corpora.BleiCorpus('./data/test.lda-c')
# print(list(corpus))
# for doc in corpus:
#     print(doc)
# corpora.SvmLightCorpus.serialize('./data/test.svmlight', corpus_memory_friendly)    # Joachim’s SVMlight格式可以使用
# corpus = corpora.SvmLightCorpus('./data/test.svmlight')
# print(list(corpus))
