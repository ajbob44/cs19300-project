import requests
import json
from datetime import datetime    

def getthhw():
    f = open("data.txt", "r")
    datas = f.readlines()
    f.close()
    for i in range(len(datas)):
        if datas[i].startswith("tophat login"):
            login = datas[i].split("=")[1].strip()
        if datas[i].startswith("tophat password"):
            password = datas[i].split("=")[1].strip()
        if datas[i].startswith("tophat classids"):
            classids = datas[i].split("=")[1].strip()

    data = {
        "username":login,
        "password":password
    }
    

    r = requests.get(f"https://app.tophat.com/index_metadata/loginv2/{classids}")

    headers = {
        "referer":"https://app.tophat.com/login/195631",
        "x-csrftoken":r.headers["set-cookie"].split(";")[0].replace("csrftoken=",""),
        "cookie":f"csrftoken={r.headers["set-cookie"].split(";")[0].replace("csrftoken=","")};"
    }

    r = requests.post(f"https://app.tophat.com/api/v3/authenticate/{classids}",data=data,headers=headers)

    token = r.headers['th_jwt']
        
    headers = {
        "authorization": f"Bearer {token}"
    }

    r = requests.get("https://app.tophat.com/api/v3/course/1142300/firestore/token/",headers=headers)
    token = json.loads(r.text)['token']
    
    r = requests.get("https://app.tophat.com/api/v3/course/1142300/student_available_due_dates",headers=headers)

    assignments = json.loads(r.text)
    homework = []
    for assignment in assignments:
        if assignment['due_date'] != None:
            try:
                r = requests.get(f"https://app.tophat.com/api/v2/pagesv2/{assignment['module_item_id']}",headers=headers)
                text = str(r.text)
                title = json.loads(text)['title']
            except Exception:
                try:
                    r = requests.get(f"https://app.tophat.com/questions/api/v1/question/{assignment['module_item_id']}",headers=headers)
                    text = str(r.text)
                    title = json.loads(text)['title']
                except Exception:
                    title = "no title found"
            homework.append(["pysch",title,datetime.fromisoformat(assignment['due_date']).timestamp()])

    return homework
