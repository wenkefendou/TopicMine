import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim import corpora, models, similarities
# 缺省形式显示语料，[]表示一篇文档；()表示一个词项，其中第一个数字表示词语，其后的数字表示词语在这篇文档中出现的次数
corpus = [[(0, 1.0), (1, 1.0), (2, 1.0)],
          [(2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (8, 1.0)],
          [(1, 1.0), (3, 1.0), (4, 1.0), (7, 1.0)],
          [(0, 1.0), (4, 2.0), (7, 1.0)],
          [(3, 1.0), (5, 1.0), (6, 1.0)],
          [(9, 1.0)],
          [(9, 1.0), (10, 1.0)],
          [(9, 1.0), (10, 1.0), (11, 1.0)],
          [(8, 1.0), (10, 1.0), (11, 1.0)]]
tfidf = models.TfidfModel(corpus)  # 将语料准换为tfidf模型
vec = [(0, 1), (4, 1)]  # 新的查询语句向量
print(tfidf[vec])  # 对新语句计算tfidf
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=12)  # 构建tfidf计算余弦相似度
sims = index[tfidf[vec]]    # 计算新语句与语料中九个语句的相似度
print(list(enumerate(sims)))

