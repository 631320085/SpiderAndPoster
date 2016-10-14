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
    resp = s.post("http://www.3demoo.com/UserManagement/Login", loginData)
    resp = s.get("http://www.3demoo.com/Partner/UserCenter/PartnerProfile")
    print(resp.text)


def CookieFromFile():
    s = GetLoginSession("3demoo", "http://www.3demoo.com/UserManagement/Login", {"Telephone": "18699967527", "Password": "123456", "ValidateCode": "lvsi"})
    resp = s.get("http://www.3demoo.com/Partner/UserCenter/PartnerProfile")
    print(resp.text)


def PostFile():
    s = GetLoginSession("3demoo")
    #获取提交表单
    editUrl = "http://www.3demoo.com/Partner/UserCenter/PartnerProfile"
    resp = SetResponseEncode(s.get(editUrl))
    #根据表单生成post数据
    postData = dict()
    soup = BeautifulSoup(resp.text, "html.parser")
    form = soup.find_all("form", id="PartnerProfileForm")[0]
    for input in form.find_all("input"):  #此处查找不全面
        if input.has_attr("name"):
            postData[input["name"]] = input["value"]
    #上传图片
    postUrl = "http://file.3demoo.com/FileManagement/UploadAvatar"
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


if __name__ == "__main__":
    # SessionPost()
    # CookieFromFile()
    PostFile()