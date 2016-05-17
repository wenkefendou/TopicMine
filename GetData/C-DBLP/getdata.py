# coding=utf-8
import time
from bs4 import BeautifulSoup
from urllib import request
import re
import pymysql


def getoutinformation(url):
    # 获取作者个人信息
    try:
        page = request.urlopen(url)
    except request.HTTPError as e:
        if e.code == "500":
            print(e)
            return 'yemianbucunzai'
        else:
            print(e)
            time.sleep(5)
            page = request.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html, 'lxml')
    parent = soup.find('div', id='col3_content')
    try:
        name = parent.h2.span.string
        department = parent.h3.string
        # 获取研究领域
        temp1 = []
        for domain in soup.find_all(href=re.compile("../domain_detail")):
            temp1.append(domain.get_text())
        domains = ';'.join(temp1)
        # 获取研究兴趣
        temp2 = []
        for interest in soup.find_all(href=re.compile("/research_area")):
            temp2.append(interest.get_text())
        interests = ';'.join(temp2)
        # 获取发文总数
        numberofpapers = re.findall(r'\d+', parent.td.string)
        numberofpaper = int(numberofpapers[0])
    except Exception as ex:
        print(ex)
        return 'yemianbucunzai'
    return name, department, domains, interests, numberofpaper


# 链接数据库并写入数据
def mysqlprocess(conn, i, name, department, domain, interest, numofpapers, url):
    # 使用cursor()方法获取操作游标
    cursor = conn.cursor()
    # sql插入语句
    sql = 'insert into author value({0},\'{1}\',\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\');'.format(i, name, department,
                                                                                                   domain, interest,
                                                                                                   numofpapers, url)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交数据
        conn.commit()
    except Exception as  e:
        print(e)
        print("Error:unable to fetch data")
    # 关闭数据库连接
    cursor.close()
    # conn.close()


if __name__ == '__main__':
    f = open('D:\MyProject\pythonProjects\data-topicmine\\authors2-2.txt', 'r', encoding='utf-8')
    pages = f.readlines()
    f.close()
    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user='root', passwd='mf1414056', db='topics', charset='utf8mb4', )
    nn = 60715
    while nn < len(pages):
        if getoutinformation(pages[nn].strip('\n')) == 'yemianbucunzai':
            print(pages.index(pages[nn]), ' yemianbucunzai')
            continue
        num1, num2, num3, num4, num5 = getoutinformation(pages[nn].strip('\n'))

        # 插入数据库
        mysqlprocess(conn, pages.index(pages[nn]), num1, num2, num3, num4, num5, pages[nn].strip('\n'))
        print(pages.index(pages[nn]))
        nn += 1
    print("get done!!!")
    conn.close()
