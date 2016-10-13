import requests
from http.cookiejar import LWPCookieJar
import os


def main():
    loginData = {"Telephone": "18699967527", "Password": "123456", "ValidateCode": "wmsd"}
    s = requests.Session()
    s.cookies = LWPCookieJar('cookiejar')
    if not os.path.exists('cookiejar'):
        s.cookies.save()
        resp = s.post("http://www.3demoo.com/UserManagement/Login", loginData)
    else:
        s.cookies.load(ignore_discard=True)
        resp = s.get("http://www.3demoo.com/Partner/UserCenter/PartnerProfile")

    print(resp.text)
    s.cookies.save(ignore_discard=True)


if __name__ == "__main__":
    main()
