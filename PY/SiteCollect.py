import requests
import redis
import re

def main():
    r = redis.StrictRedis(port=6381)

    url = "http://www.qq.com"
    rq = requests.get(url) 
    enclist = re.search(r"charset=\S+\w", rq.text).group()
    if len(enclist) > 0:
        rq.encoding = enclist[7:]
    title = re.search(r"<title>.*</title>", rq.text).group()[7:-8]
    key = "Site:" + url
    if r.get(key) is None:
        r.set(key, "{\"title\":\"" + title + "\"}")
    else :
        print(r.get(key).decode("utf-8"))
    print(re.findall(r"<meta.*/*\s*>", rq.text))
    # print(re.findall(r"href=\"http\S+(?:\.com)|(?:\.cn)|(?:\.gov)", rq.text))

if __name__ == "__main__":
    main()
