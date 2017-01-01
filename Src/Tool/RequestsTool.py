"Requests工具"
import re
import os
import time
from http.cookiejar import LWPCookieJar


class RqsTool():
    "Requests工具类"

    def __init__(self):
        self.cookies = dict()

    def set_headers(self, rqs, host=""):
        "设置request的header"
        rqs.headers = {
            "Host": host,
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        return rqs

    def set_fiddler_cookie(self, rqs, path):
        "session设置fiddler抓取的cookie"
        cookietxt = open(path, "r").read().replace("\t", "")
        #读取换行的cookie
        for cok in re.findall(r"\S+=\n\S+\n\n", cookietxt):
            cookietxt = cookietxt.replace(cok, "")
            ncok = cok.replace("\n", "")
            i = ncok.index("=")
            self.cookies[ncok[0:i]] = ncok[i + 1:]
        #读取普通cookie
        for cok in cookietxt.split("\n"):
            if cok != "":
                ncok = cok.split("=")
                self.cookies[ncok[0]] = ncok[1]
        rqs.cookies.update(self.cookies)
        return rqs

    def lwp_logined_session(self, rqs, path, lgurl=None, lgdata=None):
        "通过LWPCookieJar获得已登录的seesion"
        rqs.cookies = LWPCookieJar(path)
        if not os.path.exists(path):
            rqs.post(lgurl, lgdata)
            rqs.cookies.save(ignore_discard=True)
        else:
            rqs.cookies.load(ignore_discard=True)
        return rqs

    def tryget(self, rqs, url, timeout=10, trytimes=2):
        "带异常处理的多次请求url"
        gtimes = 0
        while True:
            try:
                resp = rqs.get(url, timeout=timeout)
                return resp
            except Exception:
                gtimes += 1
                if gtimes > trytimes:
                    print(url + "无法访问，跳过。")
                    return None
                print(url + "访问失败，重试。")
                time.sleep(5)

    def trypost(self, rqs, url, postdata, trytimes=2):
        "带异常处理的多次post"
        gtimes = 0
        while True:
            try:
                resp = rqs.post(url, postdata)
                return resp
            except Exception:
                gtimes += 1
                if gtimes > trytimes:
                    print(url + "无法post，跳过。")
                    return None
                print(url + "post失败，重试。")
                time.sleep(5)
