# coding=utf-8
"""
按文章之间的合著者共现分类
"""

from GetData.preprocess import getdata


# 文章-作者按合著者分类
def get_author_paper(sql, num_coauthor):
    # 获取作者列表
    author_list = []
    data = getdata(sql)
    for line in data:
        author_list.append([])
        id = int(line[0]) - 1
        temp = line[1].split(';')
        for authors in temp:
            author = authors.split('^c')
            author_list[id].append(author[0].strip())
    # print(author_list)

    # 统计拥有相同合著者的文章
    related_list = []  # 相关列表
    for a in range(len(author_list) - 1):
        related_list.append([])  # 存储每篇文章的同一作者文章，根据合著者相同判断
        related_list[a].append(a + 1)  # 存储文章自身编号
        for b in range(a + 1, len(author_list)):  # 循环判断其后每篇文章是否有相同合著者
            same = 0
            for item in author_list[a]:
                if item in author_list[b]:
                    same += 1
            if same > num_coauthor:  # 参数可以调整，最低为1，即除了作者自身有一个共现作者
                related_list[a].append(b + 1)  # 存储有相同合作者的文章编号
    # print(related_list)

    # 去除重复项
    for a in range(len(author_list) - 1):
        for b in range(a + 1, len(author_list) - 1):
            tempa = related_list[a]
            tempb = related_list[b]
            if set(tempa) & set(tempb):  # 如果文章有交集
                related_list[b] = related_list[a] + related_list[b]
                related_list[a] = []
                break

    # 输出
    new_list = []
    id2 = 0
    id1 = 0
    num = 0
    for item in related_list:
        if len(item) > 1:
            id2 += 1
            num += len(set(item))
            print(sorted(list(set(item))))
            # new_list.append(sorted(list(set(item))))
        if len(item) == 1:
            id1 += 1
            # print(list(set(item)))
    print("拥有合著者共现的类别：" + str(id2) + "个；  包括文章：" + str(num) + "篇")
    print("没有合著者共现的文章：" + str(id1))
    print("总文章数：" + str(len(author_list)))
    # return new_list


# 统计每一组的作者的已有的机构信息
def depart_type(sql, type_list):
    type_depart = {}  # 每组对应的机构信息
    id_depart = getdata(sql)  # 已有机构信息的文章编号和作者机构信息
    for line in id_depart:
        type_depart[line[0]] = line[1].strip()

    for a in range(len(type_list)):
        # 统计每一组对应的机构信息
        a_types = {}
        ake = 0
        for b in type_list[a]:
            if b in type_depart:
                ake += 1
                # print(type_depart[b])  # 输出对应的机构信息
                # 统计每种机构信息出现的次数
                if type_depart[b] in a_types:
                    temp = a_types[type_depart[b]] + 1
                    a_types[type_depart[b]] = temp
                else:
                    a_types[type_depart[b]] = 1
        print("第" + str(a + 1) + "组：")
        print(str(len(type_list[a])) + "篇文章共中有" + str(ake) + "篇有机构信息")
        if len(a_types) > 0:
            aa = reversed(sorted(a_types.items(), key=lambda value: value[1]))
            for line in aa:
                print(line)
        print()


if __name__ == '__main__':
    name = "李勇1"
    num_of_coauthor = 2  # 合著者共现的最少个数
    sql1 = "select id,authors from topics.{0}  where author_unique is not NULL;".format(name)
    # author_paper = get_author_paper(sql1, num_of_coauthor)
    get_author_paper(sql1, num_of_coauthor)
    # for a in range(len(author_paper)):
    #     print("第" + str(a+1) + "组有" + str(len(author_paper[a])) + "篇文章：" + str(author_paper[a]))

    #  统计每组的机构信息
    sql2 = "select id,author_unique from topics.{0} where author_unique is not NULL;".format(name)
    # depart_type(sql2, author_paper)
