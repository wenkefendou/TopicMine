# coding=utf-8
"""
重名消歧算法:
1.获取已有单位类别的作者的合作者列表
2.对与没有单位类别的文章，统计其合著者已有类别中出现的次数
3.根据统计结果，如果一篇文章只匹配到一个类别，且其合著者至少两个出现在这个类别中，则将这个类别赋予这篇文章。
"""

from GetData.preprocess import getdata, handledata, parse_xml


# 获取作者类别-合著者字典
def get_coauthor_dict(sql, name):
    dicts = {}  # 存储合作者字典
    data = getdata(sql)
    for line in data:
        if line[0] in dicts:  # 唯一作者标识已经存在字典中
            new_coauthor = dicts[line[0]]
            coauthors = line[1].split(";")
            for coauthor in coauthors:
                author = coauthor.split("^c")
                if author[0] != name and author[0] not in new_coauthor:
                    new_coauthor.append(author[0])
        else:
            new_coauthor = []
            coauthors = line[1].split(";")
            for coauthor in coauthors:
                author = coauthor.split("^c")
                if author[0] != name:
                    new_coauthor.append(author[0])
            dicts[line[0]] = new_coauthor
    return dicts


# 根据合作者信息匹配作者
def coauthor_dict_match(sql, dictionary, name):
    data = getdata(sql)  # 没有机构信息的文章数据
    paper_get_type = 0
    only_one_type = 0
    get_more_type = 0

    for line in data:
        departs = {}
        paper_id = line[1]
        for coauthor in line[0].split(";"):  # 合著者列表
            author = coauthor.split("^c")
            if author[0] != name:  # 合著者不等于重名者
                for item in dictionary.items():
                    if author[0] in item[1]:  # 合著者的姓名在合著者列表中
                        if item[0] not in departs:
                            departs[item[0]] = 1
                        else:
                            temp = departs[item[0]] + 1
                            departs[item[0]] = temp

        # 输出匹配到合著者匹配结果
        # if len(departs) > 0:
        #     paper_get_type += 1
        #     print("第%d篇文章的可能机构信息：" % paper_id)
        #     aa = reversed(sorted(departs.items(), key=lambda value: value[1]))
        #     for a in aa:
        #         if a[1] > 1:    # 限制 匹配到合著者的个数
        #             print(a)
        #     print()

        if len(departs) == 1:
            for key in departs:
                if departs[key] > 1:    # 至少两个合著者
                    print("%d:%s\n" % (paper_id, key))
                    with open('./data/depart_coauthor_match.txt', 'a', encoding='utf-8') as f:
                        f.write("%d:%s\n" % (paper_id, key))
                    only_one_type += 1
                    aa = "update {0} set author_unique = '{1}' where id ={2};".format(name, key, int(paper_id))
                    handledata(aa)

    # print("可能匹配到机构信息的文章个数：" + str(paper_get_type))
    print("匹配到一个机构信息且至少两个合著者的文章个数：" + str(only_one_type))


if __name__ == '__main__':
    name1 = "李勇"

    sql3 = "select author_unique from topics.{0} where author_unique is NUll;".format(name1)
    num_no_depart = len(getdata(sql3))
    print("没有机构信息的文章有%d篇" % num_no_depart)

    # 获取已有单位信息的作者合著者字典
    sql1 = "select author_unique,authors from topics.{0} where author_unique is not NUll;".format(name1)
    coauthor_dict = get_coauthor_dict(sql1, name1)

    # 根据合作者信息字典匹配作者
    sql2 = "select authors,id from topics.{0} where author_unique is NUll;".format(name1)
    coauthor_dict_match(sql2, coauthor_dict, name1)