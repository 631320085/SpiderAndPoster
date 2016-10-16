import requests
from http.cookiejar import LWPCookieJar
import os
import json
import re
from bs4 import BeautifulSoup
import time
import random


def GetLoginSession(cookieFile, loginUrl=None, loginData=None):
    "cookie文件保存读取方法"
    filePath = "Data/LWPCookieJar/" + cookieFile + ".txt"
    s = requests.Session()
    #User-agent 有的网站可能会通过这个屏蔽请求，可以在值后面添加随机数
    s.headers = {"User-agent": "Mozilla/5.0;222"}
    s.cookies = LWPCookieJar(filePath)
    if not os.path.exists(filePath):
        if not os.path.exists("Data/LWPCookieJar"):
            os.mkdir("Data/LWPCookieJar")
        resp = s.post(loginUrl, loginData)
        s.cookies.save(ignore_discard=True)
    else:
        s.cookies.load(ignore_discard=True)
    return s


def GetResp(s, url):
    failtimes = 0
    while True:
        try:
            resp = s.get(url, timeout=10)
            return resp
        except Exception as e:
            failtimes += 1
            if failtimes > 3:
                print("跳过")
                break
            print("一级页面访问失败，重试。")
            time.sleep(3 * failtimes)


def GetVideoLink():
    # 获取cookie不成功手动扒下来保存直接读取
    s = GetLoginSession("91vi")

    for i in range(1, 2):
        respNew = GetResp(s, "http://Domain/v.php?next=watch&page=" + str(i))
        respNew.encoding = "utf-8"
        soupNew = BeautifulSoup(respNew.text, "html.parser")
        for div in soupNew.find_all("div", class_="listchannel"):
            video = dict()
            if div.find("a") != None:
                video["name"] = div.find("a").find("img")["title"]
            if re.search(r"\d+:\d+", div.get_text()) != None:
                video["runtime"] = re.search(r"\d+:\d+", div.get_text()).group()
            retry = True
            failtimes = 0
            while retry:
                try:
                    respV = s.get(div.find("a")["href"], timeout=10)
                    respV.encoding = "utf-8"
                    soupV = BeautifulSoup(respV.text, "html.parser")
                    #等级不足不显示链接，修改cookie中等级解决
                    video["link"] = soupV.find_all("textarea", id="fm-video_link")[1].string
                    open("Data/91link.txt", "a+").write(video["runtime"] + " " + video["link"] + " " + video["name"] + "\n")
                    print(video)
                    retry = False
                    time.sleep(random.randint(3, 10))
                except Exception as e:
                    print(e)
                    failtimes += 1
                    time.sleep(5 * failtimes)
                    print(div.find("a")["href"] + " 访问失败，重试。")
                    if failtimes > 3:
                        print("跳过")
                        break


if __name__ == "__main__":
    # GetValicode()
    GetVideoLink()