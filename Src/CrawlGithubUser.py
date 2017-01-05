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
        insql = "insert into githubzhuser values('{0}', '', NOW(), null, 0, 0, '', 0)"
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


def craw_follow_user(listurl):
    "抓取follow用户"
    #第一页
    resp = RQSTOOL.tryget(RQS, listurl)
    if resp is None:
        return
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    for div in soup.find_all("div", class_="d-table-cell col-9 v-align-top pr-3"):
        link = div.find("a")
        if link is not None:
            tryadd(link["href"][1:])

    print(listurl + "抓取完成")

    #其他页
    while True:
        pagediv = soup.find("div", "pagination")
        nextp = pagediv.find("a", text="Next")
        if nextp is None:
            print("没有下一页了")
            break
        resp = RQSTOOL.tryget(RQS, nextp["href"])
        if resp is None:
            continue
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")

        for span in soup.find_all("div", class_="d-table-cell col-9 v-align-top pr-3"):
            link = span.find("a")
            if link is not None:
                tryadd(link["href"][1:])

        print(nextp["href"] + "抓取完成")
        time.sleep(2)


def craw_user_info():
    "抓取用户信息"
    usql = "select UID from githubzhuser where Checked=0"
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


def post_issue():
    "没有email的用户提交一个issue"
    usql = "select UID,FirstRepo from githubzhuser \
     where Checked=1 and Email='' and FirstRepo<>'' and Issued=0"

    upsql = "update githubzhuser set Issued=1 where UID='{0}'"
    upsql2 = "update githubzhuser set FirstRepo='' where UID='{0}'"

    rqs = RQSTOOL.set_fiddler_cookie(RQS, "Data/Fiddler/cokgithub.txt")
    postdata = dict()
    postdata["utf8"] = "✓"
    postdata["authenticity_token"] = ""
    postdata["issue[title]"] = "标题"
    postdata["saved_reply_id"] = ""
    postdata["issue[body]"] = "内容，发多了被封了，就没用了。"
    for row in MYSQLTOOL.query(usql):
        uid = row[0]
        frepo = row[1]
        resp = RQSTOOL.tryget(rqs, "https://github.com/" + uid + "/" + frepo + "/issues/new")
        if resp is None:
            continue
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        form = soup.find("form", id="new_issue")
        if form is None:
            MYSQLTOOL.execute(upsql2.replace("{0}", uid))
            continue
        token = form.find("input", attrs={"name": "authenticity_token"})

        postdata["authenticity_token"] = token["value"]
        presp = RQSTOOL.trypost(rqs, "https://github.com/" + uid + "/" + frepo + "/issues",
                                postdata)
        if presp is None:
            continue
        print(uid + "已添加issue")
        MYSQLTOOL.execute(upsql.replace("{0}", uid))
        time.sleep(2)


if __name__ == "__main__":
    #craw_star_user("https://github.com/Show-Me-the-Code/python/stargazers")
    #craw_follow_user("https://github.com/clowwindy?tab=followers")
    #craw_user_info()
    #post_issue()
    print("完成")
