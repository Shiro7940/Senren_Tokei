#V1.2.0 21/08/11
from pydub import AudioSegment
from pydub.playback import play
from PIL import Image
from os import startfile
import time
import random
import pystray
import threading
import json

RESPATH="resources/"

chara_dict = {
    1: "yos",
    2: "mak",
    3: "mur",
    4: "ren"
    }

index_dict = {
    "AM": "01",
    "PM": "02",
    "h1": "03",
    "h2": "04",
    "h3": "05",
    "h4": "06",
    "h5": "07",
    "h6": "08",
    "h7": "09",
    "h8": "10",
    "h9": "11",
    "h10": "12",
    "h11": "13",
    "h12": "14",
    "10" : "15",
    "20" : "16",
    "30" : "17",
    "40" : "18",
    "50" : "19",
    "m0" : "20",
    "m1" : "21",
    "m2" : "22",
    "m3" : "23",
    "m4" : "24",
    "m5" : "25",
    "m6" : "26",
    "m7" : "27",
    "m8" : "28",
    "m9" : "29",
    "m10" : "30",
    "m20" : "31",
    "m30" : "32",
    "m40" : "33",
    "m50" : "34",
    "END" : "35"
    }
    
def pharse_conf(conf):
    try:
        alarmlist = []
        with open(conf,"r") as file:
            config = json.load(file)
            character = config["character"]
            play_hours = bool(config["play_hours"])
            play_halfhr = bool(config["play_halfhr"])
            play_tens = bool(config["play_tens"])
            play_fives = bool(config["play_fives"])
            play_mins = bool(config["play_hours"])
            rand_chr = bool(config["rand_chr"])
            alarm_playtime = bool(config["alarm_playtime"])
            alarm_start_wav = config["alarm_start_wav"]
            sleeping_hours = list(config["sleeping_hours"])
            for item in config["alarmlist"]:
                alarmlist += item.values()
    except Exception as error:
        print("Error: "+str(error)+", Loading default settings")
        return ("mur",True,True,True,True,False,True,True,"",[],[])
    return (character,play_hours,play_halfhr,play_tens,play_fives,play_mins,rand_chr,alarm_playtime,alarm_start_wav,sleeping_hours,alarmlist)

character,play_hours,play_halfhr,play_tens,play_fives,play_mins,rand_chr,alarm_playtime,alarm_start_wav,sleeping_hours,alarmlist =\
pharse_conf(RESPATH+"config.json")

def format_cur_time(localtime,indexdict=index_dict,includemins=True):
    tlist = []
    index_list = []
    hr = localtime.tm_hour
    if hr >= 12:
        tlist += ["PM"]
        if hr == 12:
            pass
        else:
            hr -= 12
        hr = "h"+str(hr)
        tlist += [hr]
    else:
        if hr == 0:
            hr = 12
        tlist += ["AM","h"+str(hr)]
    if includemins:
        minutes = localtime.tm_min
        tens = minutes//10
        ones = minutes%10
        if (tens != 0) and (ones == 0):
            tlist += ["m"+str(tens*10)]
        elif (tens != 0) and (ones != 0):
            tlist += [str(tens*10)]
            tlist += ["m"+str(ones)]
        else:
            tlist += ["m"+str(ones)]
    tlist += ["END"]
    for item in tlist:
        index_list += [indexdict.get(item)]
    return [tlist,index_list]

def play_cur_time(timelist,chara="mur",middle="_watch_"):
    audlist = []
    print(str(chara)+str(timelist[0]))
    for item in timelist[1]:
        audlist += [AudioSegment.from_wav(RESPATH+chara+middle+item+".wav")]
    for aud in audlist:
        play(aud)

def alarm(localtime,alarmlist,indexdict=index_dict,playtime=True,alarm_start_wav=""):
    try:
        for item in alarmlist:
            wkday = []
            temp = item.get("wkday")
            alarm_min = item.get("min")
            alarm_hour = item.get("hour")
            for num in temp:
                wkday += [num-1]
            if localtime.tm_min == alarm_min and\
            localtime.tm_hour == alarm_hour and\
            localtime.tm_wday in wkday:
                if len(str(alarm_min)) == 1:
                    alarm_min = "0"+str(alarm_min)
                icon.notify("Alarm at "+str(alarm_hour)+":"+str(alarm_min))
                if playtime:
                    play_cur_time(format_cur_time(localtime,indexdict=index_dict,includemins=True),chara=item.get("chara"))
                if alarm_start_wav != "":
                    play(AudioSegment.from_wav(RESPATH+alarm_start_wav))
                for i in range(1,int(item.get("loop"))+1):
                    play(AudioSegment.from_wav(RESPATH+item.get("chara")+"_alm_"+item.get("vindex")+".wav"))
                    time.sleep(3)
                return True
    except Exception as error:
        print("Alarm Error: "+str(error))
        return False
    return False
    
def main(character,play_hours,play_halfhr,play_tens,play_fives,play_mins,rand_chr,alarm_playtime,alarm_start_wav,sleeping_hours,alarmlist):
    t = time.localtime()
    play_cur_time(format_cur_time(t,index_dict,includemins=True),chara=character)
    t = time.localtime()
    print("Started, Sleep "+str(60-t.tm_sec)+"s")
    time.sleep(60-t.tm_sec)
    global stop_threads 
    while True:
        if stop_threads:
            break
        try:
            if rand_chr:
                character = chara_dict.get(random.randint(1,len(chara_dict)))
            t = time.localtime()
            if (alarm(t,alarmlist,playtime=alarm_playtime,alarm_start_wav=alarm_start_wav) == False)\
               and (t.tm_hour not in sleeping_hours) == True:
                if play_hours and t.tm_min == 0:
                    play_cur_time(format_cur_time(t,index_dict,includemins=False),chara=character)
                    print("hr")
                elif play_halfhr and (t.tm_min//30 != 0) and (t.tm_min%10 == 0):
                    play_cur_time(format_cur_time(t,index_dict,includemins=True),chara=character)
                    print("30")        
                elif play_tens and (t.tm_min//10 != 0) and (t.tm_min%10 == 0):
                    play_cur_time(format_cur_time(t,index_dict,includemins=True),chara=character)
                    print("10")
                elif play_fives and (t.tm_min%5 == 0):
                    play_cur_time(format_cur_time(t,index_dict,includemins=True),chara=character)
                    print("5")
                elif play_mins:
                    play_cur_time(format_cur_time(t,index_dict,includemins=True),chara=character)
                    print("min")
                else:
                    print("Skipped")
            if (t.tm_hour in sleeping_hours) == True:
                print("Sleep mode, skipped")
            t = time.localtime()
            if not stop_threads:
                print("Sleep "+str(60-t.tm_sec)+"s")
                time.sleep(60-t.tm_sec)
            
        except KeyboardInterrupt:
            print("Stopped")
            break   
        except Exception as error:
            print("Error: "+str(error))
            break
        
def run_main():
    main(character,play_hours,play_halfhr,play_tens,play_fives,play_mins,rand_chr,alarm_playtime,alarm_start_wav,sleeping_hours,alarmlist)

def quit():
    icon.stop()

def open_conf():
    icon.notify('Changes will be applied after restart\nPlease save the config file first')
    startfile("resources\\config.json")    

icon_img =  Image.open(RESPATH+"icon.png","r")
menu = (pystray.MenuItem('Senren Tokei',lambda icon, item: icon.notify('Python Adaptation made by Shiro7940')),\
        pystray.MenuItem('Config',open_conf),pystray.MenuItem('Quit',quit))
icon = pystray.Icon('Senren Tokei')
icon.menu = menu
icon.icon = icon_img

stop_threads = False
thread_time = threading.Thread(target=run_main) 
thread_time.start()
icon.run()

if rand_chr:
    character = chara_dict.get(random.randint(1,len(chara_dict)))
stop_threads = True
play(AudioSegment.from_wav(RESPATH+character+"_end.wav"))
thread_time.join() 
