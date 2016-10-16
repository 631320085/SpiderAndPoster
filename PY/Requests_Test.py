import requests
from http.cookiejar import LWPCookieJar
import os
import json
import re
from bs4 import BeautifulSoup
import threading


def GetLoginSession(cookieFile, loginUrl=None, loginData=None):
    "cookie文件保存读取方法"
    filePath = "Data/LWPCookieJar/" + cookieFile + ".txt"
    s = requests.Session()
    s.headers = {"User-agent": "Mozilla/5.0"}
    s.cookies = LWPCookieJar(filePath)
    if not os.path.exists(filePath):
        if not os.path.exists("Data/LWPCookieJar"):
            os.mkdir("Data/LWPCookieJar")
        resp = s.post(loginUrl, loginData)
        s.cookies.save(ignore_discard=True)
    else:
        s.cookies.load(ignore_discard=True)
    return s


def SetResponseEncode(resp):
    "设置response的编码"
    charset = re.search(r"charset=\"?\S*\w\"?", resp.text)
    if charset is not None:
        charset = charset.group().replace('"', '')
        resp.encoding = charset[8:]
    return resp


def SessionPost():
    s = requests.Session()
    loginData = {"Telephone": "18699967527", "Password": "123456", "ValidateCode": "lvsi"}
    resp = s.post("http://www.Domain1.com/UserManagement/Login", loginData)
    resp = s.get("http://www.Domain1.com/Partner/UserCenter/PartnerProfile")
    print(resp.text)


def CookieFromFile():
    s = GetLoginSession("Domain1", "http://www.Domain1.com/UserManagement/Login", {"Telephone": "18699967527", "Password": "123456", "ValidateCode": "lvsi"})
    resp = s.get("http://www.Domain1.com/Partner/UserCenter/PartnerProfile")
    print(resp.text)


def PostFile():
    s = GetLoginSession("Domain1")
    #获取提交表单
    editUrl = "http://www.Domain1.com/Partner/UserCenter/PartnerProfile"
    resp = SetResponseEncode(s.get(editUrl))
    #根据表单生成post数据
    postData = dict()
    soup = BeautifulSoup(resp.text, "html.parser")
    form = soup.find_all("form", id="PartnerProfileForm")[0]
    for input in form.find_all("input"):  #此处查找不全面
        if input.has_attr("name"):
            postData[input["name"]] = input["value"]
    #上传图片
    postUrl = "http://file.Domain1.com/FileManagement/UploadAvatar"
    img = open(u"E:/图片/壁纸/333.jpg", "rb")
    files = {"Filedata": ("333.jpg", img, "application/octet-stream")}
    resp = s.post(postUrl, files=files)
    img.close()
    #修改表单数据
    result = json.loads(resp.text)
    postData["PhotoPath"] = result["originalImage"]["fileID"]
    #提交表单完成修改
    resp = s.post(editUrl, data=postData)
    print(resp.text)


def SaveImage(url, name):
    "保存图片"
    if not os.path.exists("Data/Image"):
        os.mkdir("Data/Image")
    if os.path.exists("Data/Image/" + name):
        return
    s = requests.Session()
    s.headers = {"User-agent": "Mozilla/5.0"}
    try:
        resp = s.get(url, timeout=10)
        if resp.status_code == 200:
            open("Data/Image/" + name, "wb").write(resp.content)
    except Exception as e:
        print("访问失败:" + url)
        print(e)


def ThreadGetPage(s, page):
    nextUrl = page[page.rfind("/") + 1:]
    while nextUrl != None:
        try:
            print(page[:page.rfind("/") + 1] + nextUrl)
            respPage = s.get(page[:page.rfind("/") + 1] + nextUrl, timeout=10)
            respPage.encoding = "gb2312"
            soupPage = BeautifulSoup(respPage.text, "html.parser")
            for image in soupPage.find_all("div", id="efpBigPic")[0].find_all("img"):
                name = "img" + image["src"].split("/")[-1]
                SaveImage(image["src"], name)
            nexta = soupPage.find("a", string="下一页")
            nextUrl = None
            if nexta["href"] != "#":
                nextUrl = nexta["href"]
        except Exception as e:
            print(e)


def GetImg():
    s = requests.Session()
    s.headers = {"User-agent": "Mozilla/5.0"}
    respIndex = s.get("http://Domain2.com/tag/aiss/")
    soupIndex = BeautifulSoup(respIndex.text, "html.parser")
    pages = set()
    for a in soupIndex.find("div", class_="lbtcimg1").find_all("a"):
        pages.add("http://Domain2.com" + a["href"])
    print(pages)
    #多线程抓取
    threads = list()
    for page in pages:
        t = threading.Thread(target=ThreadGetPage(s, page))
        threads.append(t)
    for t in threads:
        t.start()


if __name__ == "__main__":
    # SessionPost()
    # CookieFromFile()
    # PostFile()
    GetImg()
