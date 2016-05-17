# coding=utf-8
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import re
import xml.etree.ElementTree as Et
import pymysql
from nltk.corpus import WordListCorpusReader
# 添加停用词
STOP_PATH = r'D:\MyProject\pythonProjects\TopicMine\LDA_T\data\\'
stopwords = set(WordListCorpusReader(STOP_PATH, "stopwords.txt").words())


# 文件处理，分句，去除标点字符
def segment_graph(text):
    result = []
    rowsen = [sen for sen in re.split(r',|，|:|：|;|；|。|？|\?|！|!|、', text) if len(sen) > 1]
    for sen in rowsen:
        # 删除句子中的标点符号
        # string = re.sub("[A-Za-z0-9\s\.\!\:/_,$%^*()\[\]\-+\"\']+|[+——‘’，“”、~@#￥%……&*（）【】：《》·-・―％|～]+","", sen)
        # str1 = re.sub("[^\u4e00-\u9fa5A-Za-z0-9]+", "", sen)
        # if str1 not in ['None', 'SUB', 'SUP', 'sub', 'sup', 'em']:

        if sen is not None:
            result.append(sen.strip())
    # 返回处理结果
    return '\n'.join(result)


# linux环境调用LTP服务,s为文本
def ltp_server(s):
    uri_base = 'http://127.0.0.1:12345/ltp'
    data = {
        's': s,
        'x': 'n',
        't': 'dp',
    }
    r = Request(uri_base)
    params = urlencode(data)
    res = urlopen(r, params.encode())
    return res.read().strip().decode()


def ltp_pos(inp, oup):
    ltp_path = r"D:\ltp3.3.1"
    cmdline = "pos_cmdline"  # ltp_test; cws_cmdline;  pos_cmdline; par_cmdline; ner_cmdline
    threads = 5
    input_data = inp
    output_path = oup
    command = ("cd " + ltp_path + "&" + cmdline + " --threads " + str(threads) +
               " --input " + input_data + ">" + output_path)
    os.system(command)


def ltp_cws(inp, oup):
    ltp_path = r"D:\ltp3.3.1"
    cmdline = "cws_cmdline"  # ltp_test; cws_cmdline;  pos_cmdline; par_cmdline; ner_cmdline
    threads = 5
    input_data = inp
    userdict = r"D:\MyProject\pythonProjects\TopicMine\LDA_T\data\userdict.txt"
    output_path = oup
    command = ("cd " + ltp_path + "&" + cmdline + " --threads " + str(threads) +
               " --segmentor-lexicon " + userdict + " --input " + input_data + ">" + output_path)
    os.system(command)


def ltp_par(inp, oup):
    ltp_path = r"D:\ltp3.3.1"
    cmdline = "par_cmdline"  # ltp_test; cws_cmdline;  pos_cmdline; par_cmdline; ner_cmdline
    threads = 5
    input_data = inp
    userdict = r"D:\MyProject\pythonProjects\TopicMine\LDA_T\data\userdict.txt"
    output_path = oup
    command = ("cd " + ltp_path + "&" + cmdline + " --threads " + str(threads) +
               " --input " + input_data + ">" + output_path)
    os.system(command)


# windows环境调用ltp_test分词
def ltp(inp, oup):
    ltp_path = r"D:\ltp3.3.1"
    cmdline = "ltp_test"  # ltp_test; cws_cmdline;  pos_cmdline; par_cmdline; ner_cmdline
    threads = 5
    last_stage = "dp"  # ws, pos, ner, dp, srl, all
    input_data = inp
    userdict = r"D:\MyProject\pythonProjects\TopicMine\LDA_T\data\userdict.txt"
    output_path = oup

    command = ("cd " + ltp_path + "&" + cmdline + " --threads " + str(threads) + " --last-stage " + last_stage +
               " --segmentor-lexicon " + userdict + " --input " + input_data + ">" + output_path)
    os.system(command)


# 解析xml, 去除停用词、全英文或全数字、长度为1、词性为动词的词语
def parse_xml(path):
    with open(path, 'r', encoding="utf-8") as f:
        xml_raw = f.read().strip().split("\n\n")  # xml文本，可能包含多个xml，用双换行进行切分
    f.close()
    docs = []  # 存储结果
    for doc in xml_raw:
        xml = Et.fromstring(doc)
        doc_words = []
        for sentance in xml.findall('./doc/para/sent'):  # 循环读取句子
            word_list = [words for words in sentance]  # 循环读取word列表
            wordsall = []  # 存储句子的匹配结果
            for word in word_list:  # 循环解析每个word要素
                pattern = re.compile(u"([\u4e00-\u9fa5]+)")
                content = word.attrib['cont']
                pos = word.attrib['pos']
                if pattern.search(content) and len(content) > 1 and content not in stopwords and pos != "v":
                    wordsall.append(content)
            doc_words.append(' '.join(wordsall))
        docs.append(' '.join(doc_words))
    return docs  # 返回整个处理后的文本


# 从mysql获取数据，返回列表结果
def getdata(sql):
    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user='root', passwd='mf1414056', db='topics', charset='utf8mb4', )
    # 存储作者编号和其对应的主页url
    result = []
    # 获取操作游标
    cursor = conn.cursor()
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


# 插入数据到mysql数据库
def handledata(sql):
    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user='root', passwd='mf1414056', db='topics', charset='utf8mb4', )
    cursor = conn.cursor()
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

