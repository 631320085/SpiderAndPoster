import requests
import os
import re
import time
import urllib.parse
import random
from bs4 import BeautifulSoup


def PostContent(s, postUrl, reply, postData):
    success = False
    while not success:
        for j in range(1, 4):
            time.sleep(1)
            insert = random.randint(1, len(reply))
            reply = reply[:insert] + "&" + reply[insert:]
        huaji = "[emotion pic_type=1 width=30 height=30]http://tb2.bdstatic.com/tb/editor/images/face/i_f25.png?t=20140803[/emotion]"
        postData["content"] = reply.replace("&", huaji)
        try:
            print("回帖:" + postData["tid"])
            resp = s.post(postUrl, postData)
            print(resp.text)
            success = True
            time.sleep(random.randint(10, 25))
        except Exception as e:
            print(e)


def PostReply():
    s = requests.Session()
    #header
    s.headers = {
        "Host": "tieba.baidu.com",
        "Connection": "keep-alive",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }
    #读取fiddler抓取的cookie
    cookies = dict()
    cookieTxt = open("Data/CapturedData/tiebacok.txt", "r").read().replace("\t", "")
    for cok in re.findall(r"\S+=\n\S+\n\n", cookieTxt):
        cookieTxt = cookieTxt.replace(cok, "")
        c = cok.replace("\n", "")
        i = c.index("=")
        cookies[c[0:i]] = c[i + 1:]
    for cok in cookieTxt.split("\n"):
        if cok != "":
            c = cok.split("=")
            cookies[c[0]] = c[1]
    s.cookies.update(cookies)
    #读取配置
    config = dict()
    for con in open("Data/tiebaconfig.txt", "r", encoding="utf-8").read().split("\n"):
        if con != "":
            i = con.index(":")
            config[con[0:i]] = con[i + 1:]
    t = config["TemplateNum"]
    postUrl = config["PostUrl"]
    #读取post值，request post时会自动编码，读取的值先解码
    #设置为配置值，第一次访问成功可以保存返回cookie，下次读取使用(目前直接读取字典)
    postData = dict()
    for dat in urllib.parse.unquote(open("Data/CapturedData/tiebadat.txt", "r", encoding="utf-8").read()).split("&"):
        d = dat.split("=")
        postData[d[0]] = d[1]
    postData["fid"] = config["fid" + t]
    postData["kw"] = config["kw" + t]
    if "tid" + t in config.keys():
        postData["tid"] = config["tid" + t]
    else:
        postData["tid"] = ""
    reply = config["content" + t]
    #开始回复
    # for i in range(1, 10):
    #     PostContent(s, postUrl, reply, postData)
    #     time.sleep(random.randint(20, 40))
    tieSet = set()
    first = 1
    while True:
        try:
            resp = s.get(config["listUrl" + t])
            print("第" + str(first) + "次刷新-------------")
            time.sleep(15)
            rt = 0
            for tid in re.findall(r"href=\"/p/\d+", resp.text):
                id = re.search(r"\d+", tid).group()
                if first == 1:
                    tieSet.add(id)
                elif rt > 6:
                    tieSet.add(id)
                elif id not in tieSet:
                    postData["tid"] = id
                    PostContent(s, postUrl, reply, postData)
                    tieSet.add(id)
                    rt += 1
            first += 1
        except Exception as e:
            print(e)
            time.sleep(10)


if __name__ == "__main__":
    PostReply()