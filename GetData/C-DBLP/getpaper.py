# coding=utf-8
import re
from urllib import request
from bs4 import BeautifulSoup
import pymysql
import time
import urllib


# 从数据库author表中选取发文量大于100的作者编号和主页，或者从paperout表中读取数据
def getdata(sql):
    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user='root', passwd='mf1414056', db='topics', charset='utf8mb4', )
    # 存储作者编号和其对应的主页url
    result = []
    # 获取操作游标
    cursor = conn.cursor()
    # sql = 'select * from topics.author where numberofpapers>=50 order by numberofpapers DESC'
    try:
        cursor.execute(sql)
        # 获取所有记录
        results = cursor.fetchall()
        for row in results:
            result.append(row)
    except Exception as e:
        print(e)
        print("Error:unable to fetch data")
    cursor.close()
    conn.close()
    return result


# 向数据库的paperout表中插入数据,或者更改其paperget属性
def insertdata(sql):
    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user='root', passwd='mf1414056', db='topics', charset='utf8mb4', )
    cursor = conn.cursor()
    # sql = 'insert into paperout value({0},{1},\'{2}\',\'{3}\',{4});'.format(id, authorid, title, url, get)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交数据
        conn.commit()
    except Exception as e:
        print(e)
        print("Error:unable to fetch data")
    # 关闭数据库连接
    cursor.close()
    conn.close()


# 获取文章url,由于c-dblp中只保存有期刊文章，会议论文的链接没有，因此先把所有文章的题目下载保存
def geturl(url, text1, text2):
    # 获取主页
    try:
        page = request.urlopen(url)
    except request.HTTPError as e:
        if e.code == "404":
            print(e)
            return 'yemianbucunzai'
        else:
            print(e)
            time.sleep(5)
            page = request.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html, 'lxml')

    ass1 = soup.find_all('a', href=re.compile(text1))
    ass2 = soup.find_all('a', href=re.compile(text2))
    result1 = {}
    result2 = []
    for a in ass1:
        paperurl = "http://c-dblp.cn{0}".format(a['href'])
        title = a.string
        if title not in result1:
            result1[title] = paperurl
    for a in ass2:
        title = a.string
        if title not in result2:
            result2.append(title)
    return result1, result2


# 获取paper信息
def getpaper(url):
    try:
        page = request.urlopen(url)
    except request.HTTPError as e:
        print(e)
        time.sleep(5)
        page = request.urlopen(url)
    html = page.read()
    soup = BeautifulSoup(html, 'lxml')
    if soup.prettify() == '':
        return 'yemianbucunzai'
    else:
        try:
            parent = soup.find('div', class_='p_detail_box')
            # 提取title
            # title = parent.contents[1].contents[1].contents[1].contents[0].strip()
            # 提取关键字
            tem = parent.contents[1].contents[7].contents[3].contents
            keywords = ''.join(tem).replace('\n', '')
            # 提取文章来源期刊
            tem = parent.contents[1].contents[9].contents[3].contents[0].contents[0]
            source = tem.strip().replace(' ', '-').replace(' ', '')
            # 提取项目基金
            tem = parent.contents[1].contents[11].contents[3].contents
            fund = ''.join(tem).replace('\n', '')
            # 提取摘要
            abstract = parent.contents[1].contents[17].contents[1].contents[0]
            # print(fund)
        except Exception as e:
            print(e)
            return 'yemianbucunzai'
        return keywords, source, fund, abstract


if __name__ == '__main__':
    # 读取c-dblp统计文章数大于等于50的作者
    # author = getauthorid()
    # id = 0
    # 对每一个作者主页读取其文章title和对应的c-dblp提供的内容信息网址
    # for item in author:
    #     # print(author[item])
    #     if geturl(author[item], '/paper/', '../bibtex') == 'yemianbucunzai':
    #         continue
    #     paperurls, titles = geturl(author[item], '/paper/', '../bibtex')
    #     print(item, len(paperurls)+len(titles))
    #     for ii in paperurls:
    #         # print(id, item, ii, paperurls[ii])
    #         inserttoPaperout(id, item, ii, paperurls[ii], 0)
    #         print(id)
    #         id += 1
    #     for ee in titles:
    #         inserttoPaperout(id, item, ee, '', 0)
    #         # print(id, item, ee, '', 0)
    #         id += 1
    #         print(id)
    # print('Done!!!')

    # 从数据库paperout表中读取有url的记录，判断其url是否有效，
    # 有效则爬取其摘要等内容存入paper表，并更改paperout表中的getpaper为1
    sql = 'SELECT * FROM paperout where url<>"" ;'
    paperout = getdata(sql)
    id = 0
    for row in paperout:
        paperoutid = row[0]
        authorid = row[1]
        title = row[2]
        url = row[3]
        if re.search(r'[\u4e00-\u9fa5]', urllib.request.unquote(url)) is None:
            print('英文文章')
            continue
        if getpaper(url) == 'yemianbucunzai':
            print('yemianbucunzai')
            continue
        else:
            keywords, source, fund, abstract = getpaper(url)
            insertsql = 'insert into paper value({0},{1},\'{2}\',\'{3}\',\'{4}\',\'{5}\',\'{6}\');'.format(id, authorid, title, keywords,source, fund, abstract)
            insertdata(insertsql)
            print(id, authorid, '插入成功')
            # print(id, authorid, title, keywords, source, fund, abstract)
            id += 1
            updatesql = 'update topics.paperout set getpaper={0} where id={1}'.format(1, paperoutid)
            insertdata(updatesql)
            print(paperoutid, '已获取内容')
    print('well done!!!')


    # url = 'http://c-dblp.cn/paper/XCluster%3A%E5%9F%BA%E4%BA%8E%E8%81%9A%E7%B1%BB%E6%94%AF%E6%8C%81%E6%9F%A5%E8%AF%A2%E7%9A%84XML%E5%A4%9A%E6%96%87%E6%A1%A3%E5%8E%8B%E7%BC%A9%E6%96%B9%E6%B3%95/80303.html'
    # if getpaper(url) == 'yemianbucunzai':
    #     print('yemianbucunzai')
    # else:
    #     title, keywords, source, fund, abstract = getpaper(url)
    #     print(title, keywords, source, fund, abstract)


