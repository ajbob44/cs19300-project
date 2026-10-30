import requests
import json
from datetime import datetime


def getedhw():
    f = open("data.txt","r")
    tokens = f.readlines()
    f.close()
    for i in range(len(tokens)):
        if tokens[i].startswith("edstem token"):
            token = tokens[i].split("=")[1].strip()
            edi = i

    headers = {
        "X-Token":token
    }

    r = requests.get("https://us.edstem.org/api/user",headers=headers)

    userinfo = json.loads(r.text)

    courses = []

    for course in userinfo['courses']:
        courses.append([course['course']['id'],course['course']['code']])

    r = requests.post("https://us.edstem.org/api/renew_token",headers=headers)
    token = json.loads(r.text)['token']

    f = open("data.txt","w")
    for i in range(len(tokens)):
        if i == edi:
            f.write(f"edstem token:{token}\n")
        else:
            f.write(tokens[i])
    f.close()

    homework = []

    for course in courses:
        r = requests.get(f"https://us.edstem.org/api/courses/{course[0]}/lessons",headers=headers)
        lessons = json.loads(r.text)['lessons']
        for lesson in lessons:
            if lesson['status'] != "completed" and lesson['effective_due_at'] != None and lesson['status'] != "attempted":
                homework.append([course[1],lesson['title'],datetime.fromisoformat(lesson['effective_due_at']).timestamp()])

    return homework