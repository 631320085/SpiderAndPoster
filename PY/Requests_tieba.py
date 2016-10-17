import requests
import os
import re
import time
import urllib.parse


def PostReply():
    s = requests.Session()
    s.headers = {
        "Host": "tieba.baidu.com",
        "Connection": "keep-alive",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    }

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

    postUrl = "PostUrl"
    postData = dict()
    #request post时会自动编码，读取的值先解码
    for dat in urllib.parse.unquote(open("Data/CapturedData/tiebadat.txt", "r", encoding="utf-8").read()).split("&"):
        d = dat.split("=")
        postData[d[0]] = d[1]
    #第一次访问成功可以保存返回cookie，下次读取使用(目前直接读取字典)
    # postData["content"] = "开始"
    # resp = s.post(postUrl, postData)
    # print("第0次回复")
    # print(resp.text)

    reply1 = "半分钟又过去了，你还在浪费生命。"
    reply2 = "一分钟又过去了，你还在浪费生命。"
    for i in range(1, 101):
        time.sleep(30)
        if i % 2 == 0:
            postData["content"] = reply2
        else:
            postData["content"] = reply1
        success = False
        while not success:
            try:
                resp = s.post(postUrl, postData)
                print("第" + str(i) + "次回复")
                print(resp.text)
                i += 1
                success = True
            except Exception as e:
                print(e)


if __name__ == "__main__":
    PostReply()