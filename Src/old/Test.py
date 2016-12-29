from HtmlGetter import WebHtml
import datetime
import redis
import requests

response = requests.get("http://www.6ants.com")
print(response.text)

# RedisClient = redis.StrictRedis(port=6381, charset="utf-8", decode_responses=True)
# count = 0
# for key in RedisClient.keys("Site:*"):
#     count += 1
#     print(str(count) + " " + key)

# GetHtml 测试
# wh = WebHtml("http://www.zhihu.com/")
# print(wh.GetHtml())

# TimeOut 测试
# wh = WebHtml("http://www.google.com/")
# wh.TimeOut = 5
# print(wh.GetHtml())

# GetHtmlDic 测试
# urls = ["http://www.zhihu.com", "http://www.douban.com", "http://www.cnblogs.com"]
# wh = WebHtml(urls)
# for k, v in wh.GetHtmlDic().items():
#     print(k,v)

# GetHtmlDicByThread 测试
# urls = ["http://www.zhihu.com", "http://www.douban.com", "http://www.cnblogs.com"]
# wh = WebHtml(urls)
# for k, v in wh.GetHtmlDicByThread().items():
#     print(k,v)

# 多线程对比测试
# urls = ["http://www.zhihu.com", "http://www.douban.com", "http://www.cnblogs.com", "http://www.moviejie.com", "http://www.3demoo.com"]
# wh = WebHtml(urls)
# print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# wh.GetHtmlDic()
# print("单线程结束")
# print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# wh.GetHtmlDicByThread()
# print("多线程结束")
# print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
