import requests
import redis
import re
import threading

DigDeep = 3
ForceGet = False
RedisClient = redis.StrictRedis(port=6381, charset="utf-8", decode_responses=True)


def main():
    url = "http://www.360.com"
    DigSite(url)


def DigSite(url, deep=1):
    "递归挖掘站点"
    global DigDeep, RedisClient, ForceGet
    key = "Site:" + url
    try:
        headers = {'User-agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        RedisClient.set(key, "访问失败")
        print("访问失败")
    else:
        charset = re.search(r"charset=\"?\S*\w\"?", resp.text)
        if charset is not None:
            charset = charset.group().replace('"', '')
            resp.encoding = charset[8:]
        #解析解码后的html
        resphtml = resp.text
        value = "{"
        title = re.search(r"<title>.*</title>", resphtml)
        if title:
            value += '"title":"' + title.group()[7:-8] + '",'
        for meta in re.findall(r"<meta.*/*\s*>", resphtml):
            metastr = meta.lower()
            if "keywords" in metastr:
                keywords = re.search(r"content=\"\S*\"", meta)
                if keywords:
                    value += '"keywords":"' + keywords.group()[9:-1] + '",'
            if "description" in metastr:
                description = re.search(r"content=\"\S*\"", meta)
                if description:
                    value += '"description":"' + description.group()[9:-1] + '",'
        if value[-1] == ',':
            value = value[:-1]
        value += "}"
        #存入Redis
        RedisClient.set(key, value)
        print(key + " = " + value)
        #多线程访问页内链接
        deep += 1
        if deep > DigDeep:
            return
        urlset = set()
        for url in re.findall(r"https?://www\.[_\w\-\.]+(?:(?:\.com)|(?:\.cn)|(?:\.net)|(?:\.org)|(?:\.edu)|(?:\.info)|(?:\.cc)|(?:\.gov))", resphtml):
            urlset.add(url)
        threadList = list()
        for url in urlset:
            if ForceGet == False and RedisClient.get("Site:" + url) is not None:
                continue
            t = threading.Thread(target=DigSite(url, deep))
            threadList.append(t)
        for t in threadList:
            t.start()


if __name__ == "__main__":
    main()
