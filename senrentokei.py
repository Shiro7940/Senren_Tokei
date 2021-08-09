#V1.0.1 21/08/09
from pydub import AudioSegment
from pydub.playback import play
import time
import random
AUDPATH="resources/"

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
    "END" : "35",
    "h0" : "36"
    }
    
    
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
        #print(item)
        audlist += [AudioSegment.from_wav(AUDPATH+chara+middle+item+".wav")]
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
                print("Alarm at "+str(alarm_hour)+":"+str(alarm_min))
                if playtime:
                    play_cur_time(format_cur_time(localtime,indexdict=index_dict,includemins=True),chara=item.get("chara"))
                if alarm_start_wav != "":
                    play(AudioSegment.from_wav(AUDPATH+alarm_start_wav))
                for i in range(1,int(item.get("loop"))+1):
                    play(AudioSegment.from_wav(AUDPATH+item.get("chara")+"_alm_"+item.get("vindex")+".wav"))
                    time.sleep(3)
                return True
    except Exception as error:
        print("Alarm Error: "+str(error))
        return False
    return False
    

character = "mur"
play_hours = True
play_halfhr = True
play_tens = True
play_fives = True
play_mins = True
rand_chr = True
alarm_playtime = True
alarm_start_wav = "" #example: "alarm.wav" 
sleeping_hours = []  #[23,0,1,2,3,4,5,6,7]
alarm1 = {
    "chara" : "mur",
    "vindex" : "1",
    "wkday" : [1,2,3,4,5,6,7],
    "hour" : 0,
    "min"  : 12,
    "loop" : 2 
}
alarm2 = {
    "chara" : "yos",
    "vindex" : "1",
    "wkday" : [1,2,3,4,5,6,7],
    "hour" : 23,
    "min"  : 33,
    "loop" : 2 
}
alarm3 = {
    "chara" : "mak",
    "vindex" : "1",
    "wkday" : [1,2,3,4,5,6,7],
    "hour" : 12,
    "min"  : 34,
    "loop" : 2 
}
alarmlist = [alarm1,alarm2,alarm3]


t = time.localtime()
#print(t)
play_cur_time(format_cur_time(t,index_dict,includemins=True),chara=character)
t = time.localtime()
print("Started, Sleep "+str(60-t.tm_sec)+"s")
time.sleep(60-t.tm_sec)
try:
    while True:
        try:
            if rand_chr:
                character = chara_dict.get(random.randint(1,4))
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
            print("Sleep "+str(60-t.tm_sec)+"s")
            time.sleep(60-t.tm_sec)
        except KeyboardInterrupt:
            print("Stopped")
            break   
        except Exception as error:
            print("Error: "+str(error))
            break
finally:
    play(AudioSegment.from_wav(AUDPATH+character+"_end.wav"))