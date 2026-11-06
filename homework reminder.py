import time
import requests
from edstemhw import getedhw
from tophathw import getthhw

f = open("data.txt","r")
for l in f.readlines():
    if l.startswith("discord webhook url"):
        webhook = l.split("=")[1].strip()
f.close()

while True:
    homeworks = getedhw()# + getthhw()

    duesoon = []
    for homework in homeworks:
        if homework[2] - time.time() > 0 and homework[2] - time.time() < 1440000:
            duesoon.append(homework)

    for duehw in duesoon:
        data = {
            "content":f"{duehw[1]} due in {(duehw[2] - time.time())//3600} hours {((duehw[2] - time.time())//60)%60} minutes",
            "username": duehw[0]
        }
        r = requests.post(webhook,json=data)

    time.sleep(3600)
