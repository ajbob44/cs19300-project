import requests
import json

f = open("data.txt","r")
t = f.readlines()
f.close()
for l in t:
    if l.startswith("gradescope login"):
        login = l.split("=")[1].strip()
    if l.startswith("gradescope password"):
        password = l.split("=")[1].strip()

data = {
    "session[email]" : login,
    "session[password]" : password,
    "session[remember_me]":0,
    "commit":"Log In",
    "session[remember_me_sso]":0
}

r = requests.post("https://www.gradescope.com/login",data=data)

cookie = r.headers['set-cookie']


header = {
    "cookie":cookie
}

r = requests.get("https://www.gradescope.com/account", headers=header)

print(r.text)