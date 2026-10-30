import requests
import json
from datetime import datetime    

def getthhw():
    f = open("data.txt", "r")
    datas = f.readlines()
    f.close()
    for i in range(len(datas)):
        if datas[i].startswith("tophat token"):
            token = datas[i].split("=")[1].strip()
            thi=i


    headers = {
        "authorization": f"Bearer {token}"
    }

    r = requests.get("https://app.tophat.com/api/v3/course/1142300/firestore/token/",headers=headers)
    token = json.loads(r.text)['token']

    f = open("data.txt","w")
    for i in range(len(datas)):
        if i == thi:
            f.write(f"tophat token={token}\n")
        else:
            f.write(datas[i])
    f.close()
    
    r = requests.get("https://app.tophat.com/api/v3/course/1142300/student_available_due_dates",headers=headers)

    assignments = json.loads(r.text)
    homework = []
    for assignment in assignments:
        if assignment['due_date'] != None:
            homework.append(["pysch","pysch",datetime.fromisoformat(assignment['due_date']).timestamp()])

    return homework

print(getthhw())