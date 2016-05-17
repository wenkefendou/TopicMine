# coding=utf-8
from urllib.parse import quote

import time
from bs4 import BeautifulSoup
from urllib import request
import re
import copy
import urllib


# 根据初始地址和正则项，返回相应的URL地址列表
def geturl(url, text):
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

    ass = soup.find_all('a', href=re.compile(text))
    result = []
    for a in ass:
        result.append("http://c-dblp.cn{0}".format(a['href']))
        # result.append(a['href'].replace("../../", "http://c-dblp.cn/"))
    return result


def getDisam(lists):
    newlist = []
    i = 0
    num = len(lists)
    print(num)
    for temp in lists:
        # time.sleep(2)
        namedis = geturl(temp, "../../namedisambiguation")
        if namedis == 'yemianbucunzai':
            continue
        print(lists.index(temp))
        if len(namedis) > 0:
            newlist.extend(copy.deepcopy(namedis[:]))
        else:
            newlist.append(temp.strip('\n'))
        # if len(newlist) > 50:
        #     time.sleep(2)
    print(len(newlist))
    result = '\n'.join(newlist)
    save2text(result, 'D:\MyProject\pythonProjects\data-topicmine\\authors2-2.txt')


def save2text(texts, save_path):
    with open(save_path, "w", encoding='utf-8') as f:
        f.write(texts)
    f.close()
    print("save to : %s " % save_path)


if __name__ == '__main__':
    # journals = geturl("http://c-dblp.cn/index.php", "/journal")
    # authorpages = []
    # print(len(journals))
    # num = 0
    # for journal in journals:
    #     anthors = geturl(journal, "/author")
    #     print(len(anthors))
    #     for author in anthors:
    #         if author not in authorpages:
    #             authorpages.append(author)
    #         else:
    #             print(author)
    #             num += 1
    # print("重复的主页有：%d" % num)
    # print(authorpages)
    # print(len(authorpages))
    # result = '\n'.join(authorpages)
    # f = open('D:\MyProject\pythonProjects\data-topicmine\\authors1.txt', 'w', encoding='utf-8')
    # f.write(result)
    # f.close()

    # f2 = open('D:\MyProject\pythonProjects\data-topicmine\\temp.txt', 'r', encoding='utf-8')
    # f3 = open('D:\MyProject\pythonProjects\data-topicmine\\authors1.txt', 'r', encoding='utf-8')
    # tems = f2.readlines()
    # ahhs = f3.readlines()
    # f2.close()
    # f3.close()
    # others = []
    # # zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
    # for tem in tems:
        # otherauthor = geturl(tem, "/author/%")
        # others.extend(copy.deepcopy(otherauthor[:]))
    #     for temp in otherauthor:
    #         other = temp+'\n'
    #         if other not in tems and other not in ahhs:
    #             others.append(temp)
    #         # if len(others) > 20:
    #         #     time.sleep(5)
    # result = '\n'.join(others)
    # f = open('D:\MyProject\pythonProjects\data-topicmine\\temp2.txt', 'w', encoding='utf-8')
    # f.write(result)
    # f.close()

    # enable_proxy = False
    # proxy_handler = request.ProxyHandler({"http": '119.188.94.145:80'})
    # null_proxy_handler = request.ProxyHandler({})
    # if enable_proxy:
    #     opener = request.build_opener(proxy_handler)
    # else:
    #     opener = request.build_opener(null_proxy_handler)
    # request.install_opener(opener)

    f = open('D:\MyProject\pythonProjects\data-topicmine\\authors2-1.txt', 'r', encoding='utf-8')
    getDisam(f.readlines())
    f.close()

