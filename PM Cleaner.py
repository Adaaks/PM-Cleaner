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

# send first request
req = session.post(
    url="https://auth.roblox.com/"
)

if "X-CSRF-Token" in req.headers:  # check if token is in response headers
    session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]  # store the response header in the session

# send second request
req2 = session.post(
    url="https://auth.roblox.com/"
)

check = session.get('https://api.roblox.com/currency/balance')
if not check.status_code ==200:
    print("Invalid cookie!")
    time.sleep(3)
    quit()
else:
    print("Successfully logged in!")


request = session.get("https://privatemessages.roblox.com/v1/messages?pageNumber=1&pageSize=20&messageTab=Inbox")
request2 = request.json()
pmcount = request2['totalCollectionSize']


progress = 0
page = 1
num = 0
messageids = []

if pmcount == 0:
    print("[ERROR] Your private messages have already been cleaned!")
    time.sleep(5)
    quit()
while True:
    
    try:
        def program():
            
            global num
            global progress
            global messageids
            messagereq = session.get(f'https://privatemessages.roblox.com/v1/messages?pageNumber={page}&pageSize=20&messageTab=Inbox')
            messages = messagereq.json()
            lets = messages['collection'][num]['id']
            progress+=1
            num+=1
            messageids += [lets]
            print(f'Progress: {progress}/{pmcount}')
            
        program()
        
    except IndexError:

        
        archivelink = "https://privatemessages.roblox.com/v1/messages/archive"
        data = {
            "messageIds": [
                messageids
                ]
            }
        archive  = session.post(archivelink, data=data)
        messageids = []
        page+=1
        num = 0

        if progress == pmcount:
            print("[SUCCESS] Cleared all private messages!")
            time.sleep(5)
            quit()
            
        program()
        



        
