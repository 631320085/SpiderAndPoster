"GitHub用户信息抓取"
import requests
import MySQLdb
from bs4 import BeautifulSoup
from Tool.RequestsTool import RqsTool

DB = MySQLdb.connect(
    host="localhost", port=3306, user="root", passwd="123456", db="objnull", charset="utf8")
INSQL = "insert into githubzhuser values('UID','',NOW(),null, 0, 0)"


def executesql(sql):
    "执行sql"
    cur = DB.cursor()
    cur.execute(sql)
    DB.commit()


def craw_star_user():
    "抓取收藏用户"
    rqs = requests.Session()
    rqstool = RqsTool()
    rqs = rqstool.set_headers(rqs, "github.com")
    listurl = "https://github.com/Bilibili/flv.js/stargazers"
    #第一页
    resp = rqstool.tryget(rqs, listurl)
    if resp is None:
        return
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")
    for span in soup.find_all("span", class_="css-truncate css-truncate-target"):
        link = span.find("a")
        if link != None:
            uid = link["href"][1:]
            executesql(INSQL.replace("UID", uid))
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
            resp = rqstool.tryget(rqs, pageurl)
            if resp is None:
                continue
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, "html.parser")
            for span in soup.find_all("span", class_="css-truncate css-truncate-target"):
                link = span.find("a")
                if link != None:
                    uid = link["href"][1:]
                    executesql(INSQL.replace("UID", uid))
            print("插入" + str(i) + "页")


if __name__ == "__main__":
    craw_star_user()
