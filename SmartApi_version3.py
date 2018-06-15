## for multiple devices 
## solve error after reconneting , see chat.py
import pyttsx
import wikipedia
import speech_recognition as sr
import os
import nltk
import re
import webbrowser
import smtplib
import requests
import ast 
import time 
import sys
import dateutil

from datetime import datetime
from dateutil import parser
from gtts import gTTS
#from weather import Weather

engine=pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)



## for speech to speech interaction
class SmartApi_try():
    ## takes the command from user through Microphone
    def valid_url(self,url):
        start_time = time.time()
        #print (url)
        try:
            r = requests.get(url)
            req_result = r
            return (r.text , req_result)
        except requests.exceptions.Timeout as e:
            print ("Timeout ! Try Again")
            engine.say("timeout try again")
            engine.runAndWait()
            time.sleep(5)
            self.valid_url(url)
        except requests.exceptions.TooManyRedirects:
            print ("Too Many Requests")
            engine.say("too Many requests")
            engine.runAndWait()
            time.sleep(5)
            self.valid_url(url)
        except requests.exceptions.RequestException as e:
            print ("lost connectivity")
            engine.say("lost connectivity")
            engine.runAndWait()
            time.sleep(5)
            self.valid_url(url)
        except RuntimeError as e:
            print ("Took too long to connect , Try Again!")
            engine.say("too Many requests")
            engine.runAndWait()            
            sys.exit()
        except Exception as e :
            print (e)
            engine.say("couldn't handle ")
            engine.runAndWait()
            self.valid_url(url)
            
    '''
    def myCommand(self):
        ## function to be executed till internet connectivity is available again
        r = sr.Recognizer()
        r.dynamic_energy_threshold = False
        try :
            with sr.Microphone() as source:
                print('Ready...')
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source, duration=1)
                print("Speak")
                audio = r.listen(source , timeout = 5.0)
                try:
                    command = r.recognize_google(audio).lower()
                    print('You said: ' + command + '\n')
                    return (str(command))
                except sr.UnknownValueError:
                    print("We couldn't understand your last command \nTry Again!")
                    engine.say("we couldn't understand your last command Try Again!")
                    engine.runAndWait()
                    command = self.myCommand();
                except sr.RequestError as e:
                    print ("Could not request your results due to lost connectivity")
                    engine.say("could not request your results due to lost connectivity")
                    engine.runAndWait()
                    self.myCommand()
                except Exception as e :
                    print ("Unknown Issues")
                    self.myCommand()
        except Exception as e:
            print ("Unknown Issues executed")
            print (e)
            self.myCommand()
    '''
class controls(SmartApi_try):
 
    def alarms(self , response ):
        while 1:
            ##http://codeglobal.in/home_automation1/fetchalarmdetails.php?api_key=x
            resp =  response
            fixed_fetch_url = "http://codeglobal.in/home_automation1/fetchalarmdetails.php?"
            fixed_alarm_url = "http://codeglobal.in/home_automation1/alarm.php?"
            
            print ("typical statement of form , set  alarm to 7:00 p.m. for Monday or remove alarm to 7:00 p.m. for Monday , to see existing alarms say see my previous alarms")
            engine.say("typical statement of form , set  alarm to 7:00 p.m. for monday or remove alarm to 7:00 p.m. for monday")
            engine.runAndWait()

            alarm_mode =  SmartApi_try.myCommand(self)
            #alarm_mode = raw_input("give alarm = ")
            
            if re.search(r'alarm|reminder' , alarm_mode) and (re.search(r'set' , alarm_mode) or re.search(r'remove' , alarm_mode)):
                date_time = str(parser.parse(alarm_mode , fuzzy = True))
                #print (date_time)
                date_time = date_time.split(" ")

                ## user customized regex for recognition of day and time of alarm_set
                if re.findall(r'monday' , alarm_mode):
                   alarm_day = re.findall(r'monday' , alarm_mode)[0]
                if re.findall(r'tuesday' , alarm_mode):
                   alarm_day = re.findall(r'tuesday' , alarm_mode)[0]
                if re.findall(r'wednesday' , alarm_mode):
                   alarm_day = re.findall(r'wednesday' , alarm_mode)[0]
                if re.findall(r'thursday' , alarm_mode):
                   alarm_day = re.findall(r'thursday' , alarm_mode)[0]
                if re.findall(r'friday' , alarm_mode):
                   alarm_day = re.findall(r'friday', alarm_mode)[0]
                if re.findall(r'saturday' , alarm_mode):
                   alarm_day = re.findall(r'saturday' , alarm_mode)[0]
                if re.findall(r'sunday' , alarm_mode):
                   alarm_day = re.findall(r'sunday' , alarm_mode)[0]

                ## use of regex to find exact time 
                '''
                time = (re.findall(r' [0-1]?[0-9]:?.?[0-5][0-9].?p\.m\.| [0-1]?[0-9]:?.?[0-5][0-9].?p\.m\.|[0-1]?[0-9].?p\.m\ | [0-1]?[0-9].?a\.m\.', alarm_mode ))
                '''

                week_days = {0 : 'monday' , 1 : 'tuesday' , 2 : 'wednesday' , 3 : 'thursday' , 4 : 'friday' , 5 : 'saturday' , 6 : 'sunday'}
                alarm_time , alarm_date = date_time[1] , date_time[0]

                
                if re.findall(r'remove' , alarm_mode):
                    mode = 'remove'
                elif re.findall(r'set' , alarm_mode) :
                    mode = 'set'
                else :
                    engine.say('unavailable option demanded')
                    engine.runAndWait()
                    self.alarms(resp)

                ## ask for text to be added 
                #reminder = raw_input("Enter the reminder")
                engine.say("enter the reminder")
                engine.runAndWait()

                ## thus 4 things are to be passed in the database 
                ## action , alarm_day , alarm_date , alarm_time
                #print ("time = %s" %(alarm_time))
                #print ("date = %s "%(alarm_date))
                try :
                    print ("alarm day is %s "%(alarm_day))
                    #print ('day = %s' %(alarm_day))
                except Exception as e:
                    print ('day is not specified so by default current day is used')
                    day = parser.parse(alarm_mode , fuzzy = True).weekday()
                    #print ('day = %s' %week_days[day])
                    alarm_day = week_days[day]

                ## conveting time to milliseconds 
                date_time = str(parser.parse(alarm_mode , fuzzy = True))
                dt = datetime.strptime(str(date_time) , "%Y-%m-%d %H:%M:%S")
                time_milli = time.mktime(dt.timetuple())*1000 + int(76)*10
                if time_milli < time.time()*1000:
                    print ("Time already passed")
                    engine.say("time already passed")
                    engine.runAndWait()
                    self.alarms(resp)
                else :
                    ## reminder text 
                    if re.search('set' , alarm_mode):
                        engine.say('enter the reminder')
                        engine.runAndWait()
                        #reminder = raw_input("Enter the reminder ")
                        reminder =  SmartApi_try.myCommand(self)  
                        alarm_url = fixed_alarm_url + 'api_key='+resp['api_key']+'&mode='+mode+'&alarm_date='+alarm_date+'&alarm_day='+alarm_day+'&alarm_time='+alarm_time+'&time='+str(time_milli)+'&text='+reminder
                    elif re.search('remove' , alarm_mode) :
                        print ("this works")
                        try :
                            fetch_url =  fixed_fetch_url + "api_key="+resp['api_key']
                            while  SmartApi_try.valid_url(self , fetch_url ):

                            r , json = SmartApi_try.valid_url(self , fetch_url)
                            alarm_status = str(r)
                            alarm_status = list(ast.literal_eval(alarm_status))
                            for status in alarm_status:
                                if float(status['Time_ms']) == float(time_milli):
                                    text = status['Text'] 
                                    alarm_url = fixed_alarm_url + 'api_key='+resp['api_key']+'&mode='+mode+'&alarm_date='+alarm_date+'&alarm_day='+alarm_day+'&alarm_time='+alarm_time+'&time='+str(time_milli)+'&text='+text
                                    print ("here 1")
                                    print (alarm_url)
                        except Exception as e:
                            #print (e)
                            self.alarms(resp) 
                r , json = SmartApi_try.valid_url(self , alarm_url)
                output = ast.literal_eval(r)
                if output['success'] == "1":
                    print ("alarm had been added")
                    engine.say("alarm had been added")
                    engine.runAndWait()
                elif output['success'] == '-1':
                    print ("alarm already exists ")
                    engine.say("alarm already exists")
                    engine.runAndWait()
                elif output['success'] == "0":
                    print ("alarm had been removed")
                    engine.say("alarm had been removed")
                    engine.runAndWait()
                elif output['success'] == "2":
                    print ("alarm doesn't exit " )
                    engine.say("alarm doesn't exist")
                    engine.runAndWait()
                else :
                    print ("unrecognizable operations")
                    engine.say("unrecognizable operations")
                    engine.runAndWait()
            elif re.search(r'previous' , str(alarm_mode)) and re.search(r'alarm' , str(alarm_mode)):
                fetch_url =  fixed_fetch_url + "api_key="+resp['api_key']
                #print (fetch_url)
                r , json = SmartApi_try.valid_url(self , fetch_url)
                #print (r)
                #print (r.text)
                if not(re.search(r'Date' , str(r))):
                    print ("no alarm has been set")
                else:
                    alarm_status = str(r)
                    #print (alarm_status[2:-1])
                    try :
                        alarm_status = list(ast.literal_eval(alarm_status))
                        #print (alarm_status)
                        for status in alarm_status:
                            text = status['Text']
                            Text = "you have set reminder  " + text
                            print (Text)
                            engine.say(Text)
                            engine.runAndWait()
                            result_status = "your alarm is on " +status['Date']+ " " +status['Day'] +  " at " + status['Time']
                            print (result_status) 
                            engine.say(result_status)
                            engine.runAndWait()
                    except Exception as e:
                        print ("2\n error occured in exceptions here")
                        #print (alarm_status)
            else :
                print ("Wrong command , Try Again !")
                engine.say("wrong command , try Again")
                engine.runAndWait()             
                self.alarms(resp)   
            while 1:
                ## call the SmartApi_try()
                ##user_input = raw_input("do you want to set another alarm , yes or no \n")
                engine.say("do you want to set another alarm yes or no")
                engine.runAndWait()
                user_input = SmartApi_try.myCommand(self)
                if re.search(r'no' , str(user_input)) or user_input == "no":
                    return 1
                elif re.search(r'yes' , str(user_input)) or  user_input == "yes":
                    break
                else :
                    print ("Wrong Input , Try Again !")
                    self.alarms(resp)
                    engine.say("wrong input , try again")
                    engine.runAndWait()
            
    ## lights function for accessing the lights 
    def lights(self , response):

        resp = response
        fixed_url = "http://codeglobal.in/home_automation1/update.php?"
        while 1 :
            ## which device to operate by user  
            print ("\n")
            print ("options for light controls are \n device 1 \n device 2 \n device 3 \n device 4 \n all devices\n")              
            #engine.say("options for light controls are device 1 device 2 device 3 device 4 and all devices ")              
            #engine.runAndWait()

            print ("\nchoose your light which you want to turn on or off , if you want to logout say logout , and for controling other devices say go back ")
            print ("in order to check the status of lights say check status of lights")
            #engine.say("choose your light which you want to turn on or off , if you want to logout say logout , and for controling other devices say go back ")
            #engine.runAndWait()

            ## checking the device input by user 

            device_operate = str(SmartApi_try.myCommand(self))
            ##>>>>> change this 
            #device_operate =  raw_input("device_operate = ")
            #print (str(device_operate))

            ## check the current status of all devices 
            #device_status = str(requests.get("http://codeglobal.in/home_automation1/read_all.php?api=a1ebc37f43ee497ca453f84a9e9e7d11").text)
            device_status , json = SmartApi_try.valid_url(self , "http://codeglobal.in/home_automation1/read_all.php?api=a1ebc37f43ee497ca453f84a9e9e7d11")
            #print (device_status ,json)
            device_status = ast.literal_eval(device_status)['hardware'][0]
            ## upgrade for all other devices 
            if re.search("device" , str(device_operate)) and re.search("off|of" , str(device_operate)):
                if re.search(r" 1 | one " , str(device_operate)):
                    if device_status['status1'] == 'off':
                        print ("device 1 is already off")
                        engine.say("device 1 is already off")
                        engine.runAndWait()
                    else :
                        url_parsed =  fixed_url+"api_key="+resp["api_key"]+"&"+"status1"+"="+"off"
                        #requests.get(url_parsed)
                        print ("OK")
                        SmartApi_try.valid_url(self , url_parsed)
                        time.sleep(4.0)
                elif re.search(r"2 | to | two " , str(device_operate)):
                    if device_status['status2'] == 'off':
                        print ("device 2 is already off")
                        engine.say("device 2 is already off")
                        engine.runAndWait()
                    else :
                        print ("OK")
                        url_parsed =  fixed_url+"api_key="+resp["api_key"]+"&"+"status2"+"="+"off"
                        #requests.get(url_parsed)
                        SmartApi_try.valid_url(self , url_parsed)
                        time.sleep(4.0)
                elif re.search(r" 3 | three | tree " , str(device_operate)):
                    if device_status['status3'] == 'off':
                        print ("device 3 is already off")
                        engine.say("device 3 is already off")
                        engine.runAndWait()
                    else :
                        print ("OK")
                        url_parsed =  fixed_url+"api_key="+resp["api_key"]+"&"+"status3"+"="+"off"
                        #requests.get(url_parsed)
                        SmartApi_try.valid_url(self , url_parsed)
                        time.sleep(4.0)                   
                elif re.search(r" 4 | four " , str(device_operate)):
                    if device_status['status4'] == 'off':
                        print ("device 4 is already off")
                        engine.say("device 4 is already off")
                        engine.runAndWait()
                    else :
                        print ("OK")
                        url_parsed =  fixed_url+"api_key="+resp["api_key"]+"&"+"status4"+"="+"off"
                        #requests.get(url_parsed)
                        SmartApi_try.valid_url(self , url_parsed)
                        time.sleep(4.0)
                elif re.search(r"all" , str(device_operate)):
                    if device_status['status1'] == 'off' and device_status['status2'] == 'off' and device_status['status3'] == 'off' and device_status['status4'] == 'off':
                        print ("all devices are  already off")
                        engine.say("all devices are already off")
                        engine.runAndWait()
                    else :
                        print ("OK")
                        url_parsed = fixed_url+"api_key="+resp["api_key"]+"&"+"status1"+"="+"off"
                        SmartApi_try.valid_url(self , url_parsed)
                        url_parsed = fixed_url+"api_key="+resp["api_key"]+"&"+"status2"+"="+"off"
                        SmartApi_try.valid_url(self , url_parsed)
                        url_parsed = fixed_url+"api_key="+resp["api_key"]+"&"+"status3"+"="+"off"
                        SmartApi_try.valid_url(self , url_parsed)
                        url_parsed = fixed_url+"api_key="+resp["api_key"]+"&"+"status4"+"="+"off"
                        SmartApi_try.valid_url(self , url_parsed)
                        time.sleep(6.0)                        
                        ## check the status of all other device 
                        #print (device_status)
                else :
                    engine.say("no such device registered")
                    engine.runAndWait()
                    print ("no such device registered")
                    self.lights(resp)
            elif re.search("device" , str(device_operate)) and re.search("on" , str(device_operate)):
                if re.search(r" 1 | one " , str(device_operate)):
                    if device_status['status1'] == 'on':
                        print ("device 1 is already on")
                        engine.say("device 1 is already on")
                        engine.runAndWait()
                    else :
                        print ("OK")
                        url_parsed =  fixed_url+"api_key="+resp["api_key"]+"&"+"status1"+"="+"on"
                        #requests.get(url_parsed)
                        SmartApi_try.valid_url(self , url_parsed)
                        time.sleep(4.0)
                elif re.search(r" 2 | to | two " , str(device_operate)):
                    if device_status['status2'] == 'on':
                        print ("device 2 is already on")
                        engine.say("device 2 is already on")
                        engine.runAndWait()
                    else :
                        print ("OK")
                        url_parsed =  fixed_url+"api_key="+resp["api_key"]+"&"+"status2"+"="+"on"
                        #requests.get(url_parsed)
                        SmartApi_try.valid_url(self , url_parsed)
                        time.sleep(4.0)
                elif re.search(r" 3 | three | tree " , str(device_operate)):
                    if device_status['status3'] == 'on':
                        print ("device 3 is already on")
                        engine.say("device 3 is already on")
                        engine.runAndWait()
                    else :
                        print ("OK")
                        url_parsed =  fixed_url+"api_key="+resp["api_key"]+"&"+"status3"+"="+"on"
                        #requests.get(url_parsed)
                        SmartApi_try.valid_url(self , url_parsed)
                        time.sleep(4.0)
                elif re.search(r" 4 | four " , str(device_operate)):
                    if device_status['status4'] == 'on':
                        print ("device 4 is already on")
                        engine.say("device 4 is already on")
                        engine.runAndWait()
                    else :
                        print ("OK")
                        url_parsed =  fixed_url+"api_key="+resp["api_key"]+"&"+"status4"+"="+"on"
                        #requests.get(url_parsed)
                        SmartApi_try.valid_url(self , url_parsed)
                        time.sleep(4.0)
                elif re.search(r"all" , str(device_operate)):
                    if device_status['status1'] == 'on' and device_status['status4'] == 'on' and device_status['status3'] == 'on' and device_status['status2'] == 'on':
                        print ("all devices are already on")
                        engine.say("all devices are already on")
                        engine.runAndWait()
                    else:
                        print ("OK")
                        url_parsed = fixed_url+"api_key="+resp["api_key"]+"&"+"status1"+"="+"on"
                        SmartApi_try.valid_url(self , url_parsed)
                        url_parsed = fixed_url+"api_key="+resp["api_key"]+"&"+"status2"+"="+"on"
                        SmartApi_try.valid_url(self , url_parsed)
                        url_parsed = fixed_url+"api_key="+resp["api_key"]+"&"+"status3"+"="+"on"
                        SmartApi_try.valid_url(self , url_parsed)
                        url_parsed = fixed_url+"api_key="+resp["api_key"]+"&"+"status4"+"="+"on"
                        SmartApi_try.valid_url(self , url_parsed)
                        time.sleep(6.0)                        
                else :
                    engine.say("no such device registered")
                    engine.runAndWait()
                    print ("no such device registered")
                    self.lights(resp)
            elif re.search(r"log.?out" , str(device_operate)):
                resp["api_key"] = None
                print ("Exiting the Smart Api")
                engine.say("Exiting the Smart Api")
                engine.runAndWait()
                sys.exit()
            elif re.search(r'go',device_operate) and re.search(r'back', device_operate):
                return 1
            elif re.search('check' , str(device_operate)) and re.search(r'lights|status' , str(device_operate)):
                for i , j in device_status.iteritems():
                    if j == 'on':
                        text = ""
                        text = i + " is on"
                        print (text)
                        engine.say(text)
                        engine.runAndWait()
                print ("\n")
            else :
                engine.say("no such device registered")
                engine.runAndWait()
                print ("no such device registered")
                self.lights(resp)





## for simple commands using speech

## creating the object 
##obj_SmartApi_try = SmartApi_try()      
##x = obj_SmartApi_try.myCommand()
obj_controls =  controls()
##obj_controls.commands()
#obj_controls.alarms(response = {'api_key' : "a1ebc37f43ee497ca453f84a9e9e7d11"})
obj_controls.lights(response = {'api_key' : "a1ebc37f43ee497ca453f84a9e9e7d11"})
