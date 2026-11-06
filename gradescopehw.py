import requests
from datetime import datetime


def getgradescopehw():
    f = open("data.txt","r")
    t = f.readlines()
    f.close()
    for l in t:
        if l.startswith("gradescope login"):
            login = l.split("=")[1].strip()
        if l.startswith("gradescope password"):
            password = l.split("=")[1].strip()

    r = requests.get("https://www.gradescope.com/")

    authtoken = r.text.split("authenticity_token")[1].split("<meta name=\"csrf-token\" content=\"")[1].split("\" />")[0]

    headers = {
        "cookie":r.headers["set-cookie"].split(";")[0]
    }

    data = {
        "utf8":"✓",
        "authenticity_token":authtoken,
        "session[email]" : login,
        "session[password]" : password,
        "session[remember_me]":0,
        "commit":"Log In",
        "session[remember_me_sso]":0
    }

    r = requests.post("https://www.gradescope.com/login",data=data,headers=headers, allow_redirects=False)

    cookie = r.headers['set-cookie']

    headers = {
        "cookie":cookie
    }

    r = requests.get("https://www.gradescope.com/account", headers=headers)

    courses = []
    for c in r.text.split("href=\"/courses/")[1:]:
        courseid = c.split("\">")[0]
        coursename = c.split("title=\"")[1].split("\">")[0]
        courses.append([courseid,coursename])

    hw = []

    for course in courses:
        r = requests.get(f"https://www.gradescope.com/courses/{course[0]}",headers=headers)

        for assignment in r.text.split("<th class=\"table--primaryLink\" role=\"rowheader\" scope=\"row\">"):
            if assignment.find("No Submission") == -1 or assignment.find("button") == -1:
                continue
            hwname = assignment.split("Submit ")[1].split("\"")[0]
            duedate = datetime.fromisoformat(assignment.split("dueDate\" datetime=\"")[1].split("\">")[0]).timestamp()

            hw.append([course[1],hwname,duedate])

    return hw