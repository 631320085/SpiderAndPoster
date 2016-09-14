import urllib.request

html = urllib.request.urlopen("http://www.3demoo.com").read().decode()

print(html)