import os, os.path
import time 
import json
import mouse


name = None 
speed = None 
status = None


def loader():
    global name
    global speed 
    print("Loading name...")
    with open("config.json", "r") as con:
        data = json.loads(con.read())
        name = data["name"]
        speed = data["speed"]
        first_start = data["First_Start"]
        if first_start == False:
            print("\n\n\n                     WELKOM BIJ DE AUTO CLICKER VAN MEES                        ")
            print("VUL HIER ONDER JE GEGEVENS IN OM GEBRUIK TE MAKEN VAN DIT FANTASTISCHE PROGRAMMA\n")
            name = input("Wat is je Minecraft gebruikersnaam? \n ---> ")
            speed = input("Hoeveel seconden wil je tussen de slagen?     Standaard: 3 \n ---> ")
            if speed == "":
                speed = 3
            con.close()
            with open("config.json", "w") as file:
                configs = {"name" : name, "speed" : str(speed), "First_Start" : True}
                json.dump(configs, file)
                file.close()
        elif first_start == True:
            pass 
        print("{} is loaded! ".format(name))
        
   
        

def check():
    global name 
    global status
    print("waiting for chat...")
    with open(os.getenv("APPDATA")+"/.minecraft/logs/latest.log", "r") as file:
        file.seek(0, 2)
        while True:
            line = file.readline()
            if len(line) == (56 + len(name)):
                list_line = line.split(" ")
                if list_line[3] == name:
                    status_str = list_line[7]
                    if status_str == "online\n":
                        status = True
                        return True
                    elif status_str == "offline\n":
                        status = False
                        return False
            else: 
                time.sleep(0.1)
                continue
    
def last_line():
    global name
    global status

    with open(os.getenv("APPDATA")+"/.minecraft/logs/latest.log", "r") as file:
        for last_line in file:
            line = last_line
        name_line = line.split(" ")[3]
        status_line = line.split(" ")[7]
        if name_line == name:
            if status_line == "online\n":
                return True
            elif status_line == "offline\n":
                status = False
                return False
        else:
            return True       
                    
def click():
    global speed
    global status 
    print("clicking... ")
    while True:
        if status == True:
            while status == True:
                mouse.click()
                time.sleep(int(speed))
                get = last_line()
                if get == True:
                    pass 
                elif get == False:
                    status = False 
        elif status == False:
            check()

def check_for_file():
    try:
        with open("config.json", "r") as file:
            file.read()
    except IOError:
        with open("config.json", "w") as newfile:
            configs = {"name" : "", "speed" : 3, "First_Start" : False}
            json.dump(configs, newfile)
            newfile.close()
    finally:
        pass 
        
check_for_file()
loader()
print("Looping..")
while True:
    get = check()
    if get == True:
        click()

