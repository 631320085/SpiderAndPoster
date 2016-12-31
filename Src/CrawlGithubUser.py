"GitHub用户信息抓取"
import time
import requests
from bs4 import BeautifulSoup
from Tool.RequestsTool import RqsTool
from Tool.DBTool import MySQL

MYSQLTOOL = MySQL("localhost", 3306, "root", "123456", "objnull")
RQSTOOL = RqsTool()
RQS = RQSTOOL.set_headers(requests.Session(), "github.com")


def tryadd(uid):
    "添加GitHub用户"
    cksql = "select * from githubzhuser where UID='{0}'"
    if len(MYSQLTOOL.query(cksql.replace("{0}", uid))) == 0:
        insql = "insert into githubzhuser values('{0}','',NOW(),null, 0, 0, '')"
        MYSQLTOOL.execute(insql.replace("{0}", uid))
    else:
        print(uid + "已添加")


def craw_star_user(listurl):
    "抓取收藏用户"
    #第一页
    resp = RQSTOOL.tryget(RQS, listurl)
    if resp is None:
        return
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    for span in soup.find_all("span", class_="css-truncate css-truncate-target"):
        link = span.find("a")
        if link != None:
            tryadd(link["href"][1:])

    print("插入1页")

    #其他页
    usercount = int(soup.find("nav", class_="tabnav-tabs").find("span").text.replace(",", ""))
    pagecount = usercount / 51 if usercount % 51 == 0 else usercount / 51 + 1
    pagecount = int(pagecount)
    if pagecount > 2:
        if pagecount > 100:
            pagecount = 100

        for i in range(2, pagecount + 1):
            pageurl = listurl + "?page=" + str(i)
            resp = RQSTOOL.tryget(RQS, pageurl)
            if resp is None:
                continue
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, "html.parser")

            for span in soup.find_all("span", class_="css-truncate css-truncate-target"):
                link = span.find("a")
                if link != None:
                    tryadd(link["href"][1:])

            print("插入" + str(i) + "页")
            time.sleep(2)


def craw_user_info():
    "抓取用户信息"
    usql = "select UID from githubzhuser where checked = 0"
    upsql = "update githubzhuser set Email='{0}', FirstRepo='{1}', Checked=1 where UID='{2}'"
    for row in MYSQLTOOL.query(usql):
        email = ""
        frepo = ""
        uid = row[0]
        resp = RQSTOOL.tryget(RQS, "https://github.com/" + uid)
        if resp is None:
            print(uid + "信息获取失败")
            continue
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        liemail = soup.find("li", attrs={"aria-label": "Email"})
        if liemail != None:
            email = liemail.find("a").text
        spanfrepo = soup.find("span", class_="repo js-repo")
        if spanfrepo != None:
            frepo = spanfrepo.text
        MYSQLTOOL.execute(upsql.replace("{0}", email).replace("{1}", frepo).replace("{2}", uid))
        print(uid + "信息已获取")
        time.sleep(2)


if __name__ == "__main__":
    #craw_star_user("https://github.com/Show-Me-the-Code/python/stargazers")
    craw_user_info()
