#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: ake
@software: PyCharm Community Edition
@time: 2016/4/22 9:38
"""
from GetData.preprocess import getdata, handledata


def get_depart_list(sql, name):
    departs = getdata(sql)
    list1 = []
    for depart in departs:
        if depart[0] not in list1:
            list1.append(depart[0])
    # 保留最详细的机构信息，如“成都理工大学信息管理学院”与“成都理工大学”，保留后者
    for a in range(len(list1) - 1):
        if list1[a] is not None:
            for b in range(a + 1, len(list1)):
                if list1[b] is not None:
                    if list1[a].startswith(list1[b]):
                        list1[b] = None
                        continue
                    elif list1[b].startswith(list1[a]):
                        list1[a] = None
                        break
    list2 = [a for a in list1 if a is not None]
    if len(list2) != len(list1):
        temp = "select id,author_unique from topics.{0} where author_unique is not NUll;".format(name)
        update_departs(temp, list2, name)
    return list2


def update_departs(sql, lis, name):
    data = getdata(sql)
    for a in data:
        dd = a[0]
        depart = a[1]
        if depart not in lis:
            temp = "update %s set author_unique=NULL where id =%d" % (name, dd)
            handledata(temp)


if __name__ == '__main__':
    name1 = "夏斌"
    sql0 = "select author_unique from {0} where author_unique is not NUll;".format(name1)
    depart_list = get_depart_list(sql0, name1)
    print("无歧义机构信息共有%d个" % len(depart_list))
