import requests
from http.cookiejar import LWPCookieJar
import os
import json
import re
from bs4 import BeautifulSoup


def GetLoginSession(cookieFile, loginUrl=None, loginData=None):
    "cookie文件保存读取方法"
    filePath = "LWPCookieJar/" + cookieFile + ".txt"
    s = requests.Session()
    s.headers = {"User-agent": "Mozilla/5.0"}
    s.cookies = LWPCookieJar(filePath)
    if not os.path.exists(filePath):
        if not os.path.exists("LWPCookieJar"):
            os.mkdir("LWPCookieJar")
        resp = s.post(loginUrl, loginData)
        s.cookies.save(ignore_discard=True)
    else:
        s.cookies.load(ignore_discard=True)
    return s


def GetVideoLink():
    # 获取cookie不成功手动扒下来保存直接读取
    s = GetLoginSession("91vi")
    respInd = s.get("http://email.91dizhi.at.gmail.com.8h8.space/index.php")
    respInd.encoding = "utf-8"
    print(respInd.text)


if __name__ == "__main__":
    # GetValicode()
    GetVideoLink()