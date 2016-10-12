import requests
import redis
import re

DigDeep = 2
RedisClient = redis.StrictRedis(port=6381, charset="utf-8", decode_responses=True)


def main():
    url = "http://www.sina.com"
    key = "Site:" + url
    # print(RedisClient.get(key))
    DigSite(url, 1)


def DigSite(url, deep):
    global DigDeep, RedisClient
    if deep > DigDeep:
        return

    key = "Site:" + url
    try:
        headers = {'User-agent': 'Mozilla/5.0'}
        rq = requests.get(url, headers=headers, timeout=8)
    except Exception as e:
        RedisClient.set(key, "访问失败")
    else:
        charset = re.search(r"charset=\"?\S*\w\"?", rq.text)
        if charset is not None:
            charset = charset.group().replace('"', '')
            rq.encoding = charset[8:]

        value = "{"
        title = re.search(r"<title>.*</title>", rq.text)
        value += '"title":"' + title.group()[7:-8] if title else "" + '",'
        for meta in re.findall(r"<meta.*/*\s*>", rq.text):
            metastr = meta.lower()
            if "keywords" in metastr:
                keywords = re.search(r"content=\"\S*\"", meta)
                value += '"keywords":"' + keywords.group()[9:-1] if keywords else "" + '",'
            if "description" in metastr:
                description = re.search(r"content=\"\S*\"", meta)
                value += '"description":"' + description.group()[9:-1] if description else "" + '",'
        value = value[:-1] + "\"}"

        RedisClient.set(key, value)
        print(value)
    # print(re.findall(r"href=\"http\S+(?:\.com)|(?:\.cn)|(?:\.gov)", rq.text))


if __name__ == "__main__":
    main()
