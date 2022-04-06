import requests
import configparser
import os
import time
config = configparser.ConfigParser()
config.read_file(open(r"Config.ini"))
cookie = str(config.get("auth","cookie"))
config.read_file(open(r"Config.ini"))

session = requests.Session()
session.cookies[".ROBLOSECURITY"] = cookie
req = session.post(
    url="https://auth.roblox.com/"
)
if "X-CSRF-Token" in req.headers:  
    session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]  
req2 = session.post(
    url="https://auth.roblox.com/"
)
check = session.get('https://api.roblox.com/currency/balance')

if not check.status_code ==200:
    print("[ERROR] Your cookie is invalid")
    time.sleep(3)
    quit()
else:
    print("[AUTHENTICATION] Successfully logged in!")

request = session.get("https://privatemessages.roblox.com/v1/messages?pageNumber=1&pageSize=20&messageTab=Inbox")
request2 = request.json()
pmcount3 = request2['totalCollectionSize']

if pmcount3 == 0:
    print("[ERROR] Your private messages have already been cleaned!")
    time.sleep(5)
    quit()

progress = 0
while True:
    def program():
        global progress
        global messageids
        global archive
        global pmcount5
        response = session.get(f'https://privatemessages.roblox.com/v1/messages?pageNumber=1&pageSize=20&messageTab=Inbox')
        ids_and_item_types = response.json()["collection"]
        messageids = [datum["id"] for datum in ids_and_item_types]  
        archivelink = "https://privatemessages.roblox.com/v1/messages/archive"
        data = {
            "messageIds": [
                messageids
                ]
            }
        length = len(messageids)
        archive  = session.post(archivelink, data=data)
        progress += length
        print(f'Progress: {progress}/{pmcount3}')
        if progress >= pmcount3:
            print("[SUCCESS] Cleared all private messages!")
            time.sleep(5)
            quit()
    program()
