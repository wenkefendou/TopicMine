#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/24 16:51
"""
from GetData.geology.evaluate import getlist
from GetData.preprocess import getdata


if __name__ == '__main__':
    departlist = getlist('data/departs.txt')
    name1 = '李勇'
    sql0 = "select id,authors from {0} where author_unique is NUll;".format(name1)
    data = getdata(sql0)
    for line in data:
        id1 = line[0]
        departs = []
        doc = line[1].strip().split(';')
        for author in doc:
            aa = author.split('^c')
            if aa[0] != name1 and len(aa) > 1 and aa[1] in departlist:
                departs.append(aa[1])
        if len(departs) == 1:
            print('%d:%s' % (id1, departs[0]))
            with open('data/合著者机构匹配.txt', 'a', encoding='utf-8') as f:
                f.write('%d:%s' % (id1, departs[0]) + '\n')