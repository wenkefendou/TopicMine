#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/24 16:33
"""


if __name__ == '__main__':
    types = []
    with open(u'./data/文章正确类别.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            type = line.strip('\n')
            if type not in types:
                types.append(type)
    print(len(types))
    for ii in types:
        print(ii)