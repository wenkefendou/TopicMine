#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/24 10:31
"""


def getlist(textfile):
    result = []
    with open(textfile, 'r', encoding='utf-8')as f:
        for li in f.readlines():
            result.append(li.strip('\n'))
    return result


def t_t(a, b):
    pre = 0
    for line in a:
        line1 = line.split(':')
        id1 = line1[0]
        type1 = line1[1]
        if type1 == b[int(id1) - 1]:
            pre += 1
            # print(line)
    return pre


def should_right(r, a, b):
    result = 0
    for num in b:
        if r[int(num) - 1] in a:
            result += 1
    return result


def precision(a, b):
    return '%-5.4f' % (a / b)


def recall(a, b):
    return '%-5.4f' % (a / b)


def f1(p, r):
    return '%-5.4f' % (2 * p * r / (p + r))


if __name__ == '__main__':
    right = getlist('data/文章正确类别.txt')
    departs = getlist('data/departs.txt')

    coauthor = getlist('data/depart_coauthor_match.txt')
    prec = t_t(coauthor, right)
    print(precision(prec, len(coauthor)))
    weifen = getlist('data/no_type1.txt')
    shouldr = should_right(right, departs, weifen)
    print(recall(prec, shouldr))
    print(f1(float(precision(prec, len(coauthor))), float(recall(prec, shouldr))))
    print()

    sim = getlist('data/sim_match.txt')
    prec1 = t_t(sim, right)
    print(precision(prec1, len(sim)))
    type2 = getlist('data/no_type2.txt')
    sr = should_right(right, departs, type2)
    print(recall(prec1, sr))
    print(f1(float(precision(prec1, len(sim))), float(recall(prec1, sr))))
    print()

    ttt = getlist('data/合著者机构匹配.txt')
    prec2 = t_t(ttt, right)
    print(precision(prec2, len(ttt)))
    type2 = getlist('data/no_type2.txt')
    sr = should_right(right, departs, type2)
    print(recall(prec2, sr))
    print(f1(float(precision(prec2, len(sim))), float(recall(prec2, sr))))