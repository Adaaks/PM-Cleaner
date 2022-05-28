# No rate limit, very fast!
# imports required modules

import requests
import configparser
import os
import time

# gets infos in config file into variables
config = configparser.ConfigParser()
config.read_file(open(r"Config.ini"))
cookie = str(config.get("auth","cookie"))
config.read_file(open(r"Config.ini"))

# authenticates cookie into program
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

# if cookie is invalid then
if not check.status_code ==200:
    print("[ERROR] Your cookie is invalid")
    time.sleep(3)
    quit()
else:
    print("[AUTHENTICATION] Successfully logged in!")
# gets the amount of pms
request = session.get("https://privatemessages.roblox.com/v1/messages?pageNumber=1&pageSize=20&messageTab=Inbox")
request2 = request.json()
pmcount3 = request2['totalCollectionSize']
# if pms is 0 that means all pms removed so program has no need to run
if pmcount3 == 0:
    print("[ERROR] Your private messages have already been cleaned!")
    time.sleep(5)
    quit()

progress = 0
# continous loop of removing pm messages
while True:
    def program():
        global progress
        global messageids
        global archive
        global pmcount5
        # gets pms
        response = session.get(f'https://privatemessages.roblox.com/v1/messages?pageNumber=1&pageSize=20&messageTab=Inbox')
        ids_and_item_types = response.json()["collection"]
        messageids = [datum["id"] for datum in ids_and_item_types]  
        
        # archives pms in bulks of 20 (since that is robloxs limit
        archivelink = "https://privatemessages.roblox.com/v1/messages/archive"
        data = {
            "messageIds": [
                messageids
                ]
            }
        length = len(messageids)
        # archives it 
        archive  = session.post(archivelink, data=data)
        progress += length
        # displays progress towards user
        print(f'Progress: {progress}/{pmcount3}')
        # lets user know program has finished its job
        if progress >= pmcount3:
            print("[SUCCESS] Cleared all private messages!")
            time.sleep(5)
            quit()
    program()
    
    
