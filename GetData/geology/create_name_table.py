# coding=utf-8
"""
可以按照geocount中的发文量排名，降序抽取出某个作者名的所有文章，
生成相应的“作者名”，其中新增一列author_unique，用来表示重名作
者的唯一标识。
"""
import re

from GetData.preprocess import handledata, getdata


# 按照作者名生成新的表
def create_name_table(name):
    create = '''CREATE TABLE `{0}` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` tinytext,
  `author_unique` varchar(200) DEFAULT NULL,
  `authors` mediumtext,
  `mname` tinytext,
  `index_terms` tinytext,
  `keywords` tinytext,
  `abstract` mediumtext,
  `pdate` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=372 DEFAULT CHARSET=utf8;'''.format(name)
    handledata(create)
    print("生成新表:" + name)


# 获取制定姓名的文章信息，插入新生成的表中
def fill_new_table(sql, name, ins1, ins2):
    data = getdata(sql)
    id = 0
    for row in data:
        title = row[1].strip().strip('\n').strip('\r')
        authors = row[2]
        mname = row[3]
        index_terms = row[4]
        if row[5] is not None:
            keywords = row[5].strip().strip('\n').strip('\r')
        else:
            keywords = row[5]
        abstract = row[6].strip().strip('\n').strip('\r')
        pdate = row[7]
        try:
            # 找到包含名字是name的记录
            authorlist = authors.split(";")
            for author in authorlist:
                new_author = re.split(r'\^c', author.strip())
                if new_author[0] == name:
                    if len(new_author) > 1:  # 标记已有机构信息的作者
                        temp = new_author[1]
                        id += 1
                        sql = ins1.format(id, title, temp, authors, mname, index_terms, keywords, abstract, pdate,
                                          name)
                        handledata(sql)
                    else:
                        id += 1
                        sql = ins2.format(id, title, authors, mname, index_terms, keywords, abstract, pdate,
                                          name)
                        handledata(sql)
        except Exception as e:
            print(e)
    print("填充新表" + "\"" + name + "\"" + "完成!")


if __name__ == "__main__":
    # 生成新的表
    name1 = "杜远生"
    create_name_table(name1)

    # 选择作者名相同的文章插入新的表中
    sql1 = "select * from topics.geopaper;"
    # 插入有单位信息的作者
    insert1 = ("insert into {9}(id,title,author_unique,authors,mname,index_terms,keywords,abstract,pdate) "
               "values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\',\'{8}\');")
    # 插入没有单位信息的作者
    insert2 = ("insert into {8}(id,title,authors,mname,index_terms,keywords,abstract,pdate) "
               "values(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\',\'{7}\');")
    fill_new_table(sql1, name1, insert1, insert2)
