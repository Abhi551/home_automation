## alarm setting for home assistant 

import pyttsx
import speech_recognition as sr
import nltk
import re
import sys
import dateutil

from dateutil import parser
from gtts import gTTS

engine =  pyttsx.init()
voices = engine.getProperty("voices")
engine.setProperty('voice' , voices[1].id)
engine.setProperty('rate' , 150)

url = "http://codeglobal.in/home_automation1/alarms.php?mode=set&time=bsdh&hours="

## check is user says today , tomorrow , or day after tommorow
## check if the date given is not in past 
## check if the command have 24 hours setting in it , am/pm or , o'clock

    def alarms():
        
        ## first parser is used but it doesn't give result always and it doesn't recognize the days of wee
        try:
            alarm = 'set the alarm to monday  9 p.m.'
            date_time = parser.parse(alarm , fuzzy = True)
            #print (type(x))
            date_time = str(date_time)
            date_time = date_time.split(" ")
            ## user customized regex for recognition of day and time of alarm
            list_week = ['monday' , 'tuesday' , 'wednesday' , 'thursday' , 'friday' , 'saturday' , 'sunday']
            for days in list_week:
                if re.findall(r'monday' , alarm):
                    day = re.findall(days , alarm)
                    break
                elif re.findall(r'tuesday' , alarm):
                    day = re.findall(days , alarm)
                    break
                elif re.findall(r'wednesday' , alarm):
                    day = re.findall(days , alarm)
                    break
                elif re.findall(r'thursday' , alarm):
                    day = re.findall(days , alarm)
                    break
                elif re.findall(r'friday' , alarm):
                    day = re.findall(days , alarm)
                    break
                elif re.findall(r'saturday' , alarm):
                    day = re.findall(days , alarm)
                    break
                elif re.findall(r'sunday' , alarm):
                    day = re.findall(days , alarm)
                    break

            alarm = "set alarm to 9:01 p.m."
            #if (re.findall(r'[0-1]?[0-9].?p\.m\.|[0-1]?[0-9]?.?a\.m\.' , alarm ))

            time = (re.findall(r' [0-1]?[0-9]:?.?[0-5][0-9].?p\.m\.| [0-1]?[0-9]:?.?[0-5][0-9].?p\.m\.|[0-1]?[0-9].?p\.m\ | [0-1]?[0-9].?a\.m\.', alarm ))
            print (time)
            print (day)
            print date_time
            return (date_time , day , time)
        except Exception as e:
            print (e)
            print ("alarm set in wrong format")






