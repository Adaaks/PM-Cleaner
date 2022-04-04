import configparser
import os
import time
import configparser
def program():
    
    cookie = str(input("Enter your cookie: "))
    config = configparser.ConfigParser()
    config.read("Config.ini")
    
    if "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_" in cookie:
        config.set("auth", "cookie", cookie)
        with open("config.ini", 'w') as configfile:
            config.write(configfile)
            os.startfile("PM Cleaner.py")
            quit()
    else:
        print("[ERROR] Your cookie must start with:\n\n_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_")
        program()
program()   
