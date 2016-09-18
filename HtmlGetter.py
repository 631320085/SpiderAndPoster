from urllib.request import urlopen

import threading

class WebHtml():
    "网站html获取类"

    #访问的Url列表
    UrlList = list()
    #GetHtml单个url的结果
    Html = ""
    #多个url的结果字典
    HtmlDic = dict()
    #访问超时值
    TimeOut = 0

    def __init__(self, urlList):
        "构造必须初始化访问的url列表"
        self.UrlList = urlList
    
    def SetTimeOut(self, timeOut):
        "设置访问超时值"
        self.TimeOut = timeOut

    def GetHtml(self, url = None):
        "获取单个网站数据"
        #没有穿参时使用url列表第一个
        if(url == None):
            url = self.UrlList[0] if isinstance(self.UrlList, list) else self.UrlList
        #获取网站返回值
        try:
            if(self.TimeOut == 0):
                self.Response = urlopen(url).read()
            else:
                self.Response = urlopen(url, timeout = self.TimeOut).read()
        except Exception as e:
            return "访问失败：" + str(e)
        #解码返回结果为string
        try:
            self.Html = self.Response.decode("utf-8")
            return self.Html
        except:
            self.Html = self.Response.decode("gbk", "ignore")
            return self.Html
    
    def GetHtmlDic(self):
        "获取网站数据字典"
        for url in self.UrlList:
            self.HtmlDic[url] = self.GetHtml(url)
        return self.HtmlDic

    def ThreadGetHtml(self, url):
        "线程调用方法"
        self.HtmlDic[url] = self.GetHtml(url)

    def GetHtmlDicByThread(self):
        "多线程获取网站数据字典"
        #生成线程列表
        threads = list()
        for url in self.UrlList:
            t = threading.Thread(target=self.ThreadGetHtml(url))
            threads.append(t)
        #启动线程列表
        for t in threads:
            t.start()
        #等待线程全部完成返回结果
        t.join()
        return self.HtmlDic

