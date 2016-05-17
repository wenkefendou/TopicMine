# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/5/17 11:19
"""
from collections import defaultdict
from gensim import corpora


# 统计词频
def term_frequency(obj):
    if not isinstance(obj, list):
        raise TypeError('bad operand type for term_frequency, it need two-dimensional array.')
    frequency = defaultdict(int)
    for text in obj:
        for token in text:
            frequency[token] += 1
    return frequency


# 从列表生成词典和语料
def dict_corpora_from_list(obj, dict_path='None', corpora_path='None'):
    if not isinstance(obj, list):
        raise TypeError('bad operand type for term_frequency, it need two-dimensional array.')
    dictionary = corpora.Dictionary(obj)
    if dict_path != 'None':
        dictionary.save(dict_path)

    corpus = [dictionary.doc2bow(text) for text in obj]
    if corpora_path != 'None':
        corpora.MmCorpus.serialize(corpora_path, corpus)
    return dictionary, corpus


# 从文件生成词典和语料
def dict_corpora_from_file(file_path, dict_path='None', corpora_path='None'):
    dictionary = corpora.Dictionary(line.split() for line in open(file_path, encoding='utf-8'))
    if dict_path != 'None':
        dictionary.save(dict_path)

    class MyCorpus(object):
        def __iter__(self):
            for line in open(file_path, encoding='utf-8'):
                yield dictionary.doc2bow(line.split())

    corpus_memory_friendly = MyCorpus()
    if corpora_path != 'None':
        corpora.MmCorpus.serialize(corpora_path, corpus_memory_friendly)
    return dictionary, corpus_memory_friendly


if __name__ == '__main__':
    pass
