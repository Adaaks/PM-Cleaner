import requests
import configparser
import os
import time
import threading 
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
    print("[ERROR] Your cookie is invalid")
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



def threads2():
    global num
    global progress
    global messageids
    global page
    
    while True:

        try:
            
        
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
                    screen_lock.acquire()
                    print(f'Progress: {progress}/{pmcount}')
                    screen_lock.release()
                    
                program()
                
            except IndexError:

                
                archivelink = "https://privatemessages.roblox.com/v1/messages/archive"
                data = {
                    "messageIds": [
                        messageids
                        ]
                    }
                archive  = session.post(archivelink, data=data)

                if archive.status_code != 200:
                    screen_lock.acquire()
                    print("[RATELIMIT] You're being ratelimited.")
                    screen_lock.release()
                messageids = []
                page+=1
                num = 0

                if progress == pmcount:
                    screen_lock.acquire()
                    print("[SUCCESS] Cleared all private messages!")
                    screen_lock.release()
                    time.sleep(5)
                    quit()
                    
                program()
        except:
            print("[SUCCESS] Cleared all private messages!")
            time.sleep(5)
            quit()
            

threads = int(input("[THREADS] Input amount of threads: "))

while True:
    try:
        if threading.active_count() <= threads:
            threading.Thread(target=threads2).start()
    except:
        screen_lock.acquire()
        print("[SUCCESS] Cleared all private messages!")
        time.sleep(5)
        screen_lock.release()
        quit()


        
