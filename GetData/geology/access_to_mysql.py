# -*- coding: utf-8 -*-
import pyodbc
import re
from GetData.preprocess import handledata


# 链接access数据库
def link_access(sql):
    dbfile = r'D:\MyProject\pythonProjects\data\topicmine\文摘库.mdb'
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + dbfile + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    result = []
    for row in cursor.execute(sql):
        result.append(row)
    cursor.close()
    conn.close()
    return result


# 过滤作者信息，最多只保留作者名和机构信息
def filter(sources, insert):
    counter = {}  # 统计原始数据作者发文量
    for row in sources:
        title = row[0].strip()
        mname = row[2]
        index_terms = row[3]
        keywords = row[4]
        abstract = row[5]
        pdate = row[6]
        if abstract is None or abstract.strip() == "":
            continue
        try:
            authors = row[1]
            authors.replace("0800^a", "")  # 0800^a后跟集体投稿人的名称，不起分隔作用
            authors.replace("0070^a", "")  # 0070^a后跟部分作者名，不起分隔作用
            authorlist = re.split(r';|2300\^a', authors.strip())  # 2300^a后跟作者名，多出现与中外合著，有分隔作者的作用
            if len(authorlist) < 2:  # 文章只有一个作者
                sql = insert.format(title, authorlist[0].strip(), mname, index_terms, keywords, abstract, pdate)
                handledata(sql)
                # 统计作者出现频次
                if authorlist[0].strip() in counter:
                    counter[authorlist[0].strip()] += 1
                else:
                    counter[authorlist[0].strip()] = 1
            else:  # 文章有多个作者
                # 对每个作者只保留作者名和机构信息
                new_authors = []
                for author in authorlist:
                    author = re.split(r'\^c|\^d|\^e|\^f', author.strip())
                    if len(author) > 2:
                        temp = author[0].strip() + "^c" + author[1].strip()
                        new_authors.append(temp)
                        # 统计作者频次
                        if temp in counter:
                            counter[temp] += 1
                        else:
                            counter[temp] = 1
                    else:
                        new_authors.append(author[0].strip())
                        # 统计作者频次
                        if author[0].strip() in counter:
                            counter[author[0].strip()] += 1
                        else:
                            counter[author[0].strip()] = 1
                sql1 = insert.format(title, ";".join(new_authors), mname, index_terms, keywords, abstract, pdate)
                handledata(sql1)
        except Exception as e:
            print(e)
    return counter


if __name__ == '__main__':
    # 从文摘库中抽取出包含摘要的文章信息，并对作者信息过滤
    sql1 = 'select title,author,mname,keyword,NN_AKEYWORD_S,abstract,pdate from 查询;'
    sources = link_access(sql1)
    insert1 = "insert into geopaper(title,author,mname,index_terms,keywords,abstract,pdate) " \
              "values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\');"

    # 生成发文量统计表
    counter = filter(sources, insert1)
    for name in counter:
        number = counter[name]
        sql2 = 'insert into geocount(name,numofpapers) value(\'{0}\',{1})'.format(name, number)
        handledata(sql2)
    print('Well done!!!')
