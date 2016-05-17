#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/24 11:00
"""
from GetData.preprocess import getdata

if __name__ == '__main__':
    sql1 = 'select id from topics.{0}  where author_unique is NULL;'.format('李勇')
    data = getdata(sql1)
    for line in data:
        id1 = str(line[0])
        with open('geology/data/no_type2.txt', 'a', encoding='utf-8')as f:
            f.write(id1 + "\n")
