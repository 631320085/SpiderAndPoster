"贴吧发帖器"
import time
import random
import re
import urllib.parse
import requests
from Tool.RequestsTool import RqsTool

RQSTOOL = RqsTool()
RQS = RQSTOOL.set_headers(requests.Session(), "tieba.baidu.com")
RURL = "http://tieba.baidu.com/f/commit/post/add"


def post_reply(data, count, sleep):
    "回帖"
    pdsample = """ie=utf-8&kw=github&fid=2748553&tid=4913371495&vcode_md5=&floor_num=3&rich_text=1&tbs=cb6b34d0ed7bcb291483587140&content=%E5%9B%9E%E5%A4%8D%E6%B5%8B%E8%AF%95%5Bemotion+pic_type%3D1+width%3D30+height%3D30%5Dhttp%3A%2F%2Ftb2.bdstatic.com%2Ftb%2Feditor%2Fimages%2Fface%2Fi_f25.png%3Ft%3D20140803%5B%2Femotion%5D&files=%5B%5D&mouse_pwd=11%2C12%2C15%2C17%2C12%2C11%2C10%2C10%2C52%2C12%2C17%2C13%2C17%2C12%2C17%2C13%2C17%2C12%2C17%2C13%2C17%2C12%2C17%2C13%2C17%2C12%2C17%2C13%2C52%2C12%2C14%2C5%2C14%2C8%2C13%2C52%2C12%2C4%2C15%2C13%2C17%2C12%2C13%2C5%2C13%2C14835871387610&mouse_pwd_t=1483587138761&mouse_pwd_isclick=0&__type__=reply"""

    haha = "会收到回复"
    rqs = RQSTOOL.set_fiddler_cookie(RQS, "Data/Fiddler/coktieba.txt")
    postdata = dict()
    for dat in urllib.parse.unquote(pdsample).split("&"):
        dkv = dat.split("=")
        postdata[dkv[0]] = dkv[1]
    postdata["fid"] = data["fid"]
    postdata["kw"] = data["kw"]
    postdata["tid"] = data["tid"]
    for i in range(0, count):
        postdata["content"] = get_randstr(data["content"])
        resp = RQSTOOL.trypost(rqs, RURL, postdata)
        if resp != None:
            print("第" + str(i + 1) + "次回帖：")
            print(resp.text)
        i += 1
        time.sleep(sleep)


def get_randstr(reply):
    "添加随机字符串"
    for j in range(0, 3):
        insert = random.randint(1, len(reply))
        reply = reply[:insert] + "&" + reply[insert:]
        time.sleep(1)
        j += 1
    huaji = "[emotion pic_type=1 width=30 height=30]http://tb2.bdstatic.com/tb/editor/images/face/i_f25.png?t=20140803[/emotion]"
    reply = reply.replace("&", huaji)
    randstr = ""
    for k in range(0, 3):
        for i in range(0, random.randint(5, 20)):
            randstr += "_"
            i += 1
        randstr += "."
        time.sleep(1)
        k += 1
    return reply + randstr


def reply_newtie(url, data, count, sleep):
    "抢二楼"
    rqs = RQSTOOL.set_fiddler_cookie(RQS, "Data/Fiddler/coktieba.txt")
    tieset = set()
    refresh = 1
    for i in range(0, count):
        resp = RQSTOOL.tryget(rqs, url)
        print("第" + str(refresh) + "次刷新-------------")
        for tid in re.findall(r"href=\"/p/\d+", resp.text):
            idnum = re.search(r"\d+", tid).group()
            if refresh == 1:
                tieset.add(idnum)
            elif idnum not in tieset:
                data["tid"] = idnum
                post_reply(data, 1, 20)
                tieset.add(idnum)
        refresh += 1
        time.sleep(sleep)
        i += 1


if __name__ == "__main__":
    PDATA = dict()
    PDATA["kw"] = "github"
    PDATA["fid"] = "2748553"
    PDATA["tid"] = "4913371495"
    PDATA["content"] = "每隔十几秒，会有一个回复，并且很滑稽。"
    #post_reply(PDATA, 5, 10)

    QDATA = dict()
    QDATA["kw"] = "魔兽世界"
    QDATA["fid"] = "73787"
    QDATA["tid"] = ""
    QDATA["content"] = "我是不是二楼，是不是又怎样，不是已经有十五字了。"
    QURL = "http://tieba.baidu.com/f?kw=%E9%AD%94%E5%85%BD%E4%B8%96%E7%95%8C"
    #reply_newtie(QURL, QDATA, 10, 10)
    print("完成")
