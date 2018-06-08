import pyttsx
import speech_recognition as sr
import nltk
import re
import sys
import dateutil
import os
import webbrowser
import smtplib
import requests
import ast 
import time 
import sys
import datetime 

from datetime import datetime
from dateutil import parser
from gtts import gTTS

engine =  pyttsx.init()
voices = engine.getProperty("voices")
engine.setProperty('voice' , voices[1].id)
engine.setProperty('rate' , 150)

##http://codeglobal.in/home_automation1/alarm.php?api_key=XXXXXXXXXXXXXXXXXXXXXX&mode=set&alarm_date=2018-06-11&alarm_time=19:00:00&alarm_day=monday

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
            #engine.say("timeout try again")
            #engine.runAndWait()
            time.sleep(5)
            self.valid_url(url)
        except requests.exceptions.TooManyRedirects:
            print ("Too Many Requests")
            #engine.say("too Many requests")
            #engine.runAndWait()
            time.sleep(5)
            self.valid_url(url)
        except requests.exceptions.RequestException as e:
            print ("lost connectivity")
            #engine.say("lost connectivity")
            #engine.runAndWait()
            time.sleep(5)
            self.valid_url(url)
        except RuntimeError as e:
            print ("Took too long to connect , Try Again!")
            #engine.say("too Many requests")
            #engine.runAndWait()            
            sys.exit()

    def myCommand(self):
        ## function to be executed till internet connectivity is available again
        r = sr.Recognizer()
        try :
            with sr.Microphone() as source:
                print('Ready...')
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source, duration=1)
                print("Speak")
                audio = r.listen(source)
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

class controls(SmartApi_try):

    ## to access alarms and remainder 
    def alarms(self , response):
        self.response = response
        while 1:
            ##http://codeglobal.in/home_automation1/fetchalarmdetails.php?api_key=x
            fixed_fetch_url = "http://codeglobal.in/home_automation1/fetchalarmdetails.php?"
            fixed_alarm_url = "http://codeglobal.in/home_automation1/alarm.php?"
            
            print ("typical statement of form , set  alarm to 7:00 p.m. for Monday or remove alarm to 7:00 p.m. for Monday , to see exiting alarms say see my previous alarms")
            #engine.say("typical statement of form , set  alarm to 7:00 p.m. for monday or remove alarm to 7:00 p.m. for monday")
            #engine.runAndWait()

            #alarm_set =  SmartApi_try.myCommand(self)
            alarm_mode = raw_input("set alarm = ")
            
            if re.search(r'alarm' , alarm_mode) and (re.search(r'set' , alarm_mode) or re.search(r'remove' , alarm_mode)):
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

                ## thus 4 things are to be passed in the database 
                ## action , alarm_day , alarm_date , alarm_time
                #print ("time = %s" %(alarm_time))
                #print ("date = %s "%(alarm_date))
                try :
                    print (alarm_day)
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
                    #engine.say("time already passed")
                    #engine.runAndWait()
                    self.alarms(12)
                else :
                    pass
                alarm_url = fixed_alarm_url + 'api_key='+self.response['api_key']+'&mode='+mode+'&alarm_date='+alarm_date+'&alarm_day='+alarm_day+'&alarm_time='+alarm_time+'&time='+str(time_milli)
                #print (alarm_url)
                #print ("mode = %s " %(mode))
                #print ("milliseconds = ")
                #print (time_milli)

                r , json = SmartApi_try.valid_url(self , alarm_url)
                output = ast.literal_eval(r)
                if output['success'] == "1":
                    print ("alarm had been added")
                    #engine.say("alarm had been added")
                    #engine.runAndWait()
                elif output['success'] == '-1':
                    print ("alarm already exists ")
                    #engine.say("alarm already exists")
                    #engine.runAndWait()
                elif output['success'] == "0":
                    print ("alarm had been removed")
                    #engine.say("alarm had been removed")
                    #engine.runAndWait()
                elif output['success'] == "2":
                    print ("alarm doesn't exit " )
                    #engine.say("alarm doesn't exist")
                    #engine.runAndWait()
                else :
                    print ("unrecognizable operations")
                    #engine.say("unrecognizable operations")
                    #engine.runAndWait()

            elif re.search(r'previous' , alarm_mode) and re.search(r'alarm' , alarm_mode):
                fetch_url =  fixed_fetch_url + "api_key="+self.response['api_key']
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
                            result_status = "your alarm is on " +status['Date']+ " " +status['Day'] +  " at " + status['Time']
                            print (result_status) 
                    except Exception as e:
                        print ("2\n error occured in exceptions here")
                        #print (alarm_status)
            else :
                print ("Wrong command , Try Again !")
                #engine.say("wrong command , try Again")
                #engine.runAndWait()             
                self.alarms()   
            while 1:
                ## call the SmartApi_try()
                user_input = raw_input("do you want to set another alarm , yes or no \n")
                #engine.say("do you want to set another alarm yes or no")
                #engine.runAndWait()
                #user_input = SmartApi_try.myCommand(self)
                ## check sometime gives wrong input 
                #print ("user_input = " ,user_input)
                if re.search(r'no' , user_input) or user_input == "no":
                    return 1
                elif re.search(r'yes' , user_input) or  user_input == "yes":
                    break
                else :
                    print ("Wrong Input , Try Again !")
                    #engine.say("wrong input , try again")
                    #engine.runAndWait()
    ## lights function for accessing the lights 
    def lights(self , response):

        fixed_url = "http://codeglobal.in/home_automation1/update.php?"
        self.response = response
        ## working on device 2 only
        ## checking the device input by user 
        while 1 :
            print ("which light you want to turn on or off ,say device 2 on or device 2 off , to enter main console say go back and for logout say logout" )
            #engine.say("which light you want to turn on or off ,say device 2 on or device 2 off , to enter main console say go back and for logout say logout")
            #engine.runAndWait()
            #device_operate = SmartApi_try.myCommand(self)
            device_operate = raw_input("device_operate = ")
            ## upgrade for all other devices 
            url = "http://codeglobal.in/home_automation1/read_all.php?api="+self.response['api_key']
            r , json = SmartApi_try.valid_url(self , url)
            device_status = r
            device_status = ast.literal_eval(device_status)['hardware'][0]
            #print ("the status of device_status is")
            #print (device_status)

            if re.search(r"device 2|device to" , str(device_operate)) and re.search(r"on" , str(device_operate)):
                if device_status['status2'] == 'on':
                    print ("device 2 is already on")
                    #engine.say("device 2 is already on")
                    #engine.runAndWait()
                else :
                    url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status2"+"="+"on"
                    SmartApi_try.valid_url(self , url_parsed) #print (url_parsed)
                    ## check the status of all other device
                    #print (device_status) 
                    print ("device is on now")
            elif re.search(r"device 2|device to" , str(device_operate)) and re.search(r"off" , str(device_operate)):
                if device_status['status2'] == 'off':
                    print ("device 2 is already off")
                    engine.say("device 2 is already off")
                    engine.runAndWait()
                else :
                    url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status2"+"="+"off"
                    SmartApi_try.valid_url(self , url_parsed) #print (url_parsed)
                    ## check the status of all other device 
                    #print (device_status)
                    print ("device is off now")
            elif re.search(r"logout" , str(device_operate)):
                self.response["api_key"] = None
                print ("Exiting the Smart Api")
                engine.say("exiting the smart api")
                engine.runAndWait()
                sys.exit()
            elif re.search(r'go' , (device_operate)) and re.search(r'back', (device_operate)):
                return 1
            else :
                print ("nothing fetched")
                self.lights()
## creating the object 
##obj_SmartApi_try = SmartApi_try()      
#obj_controls = controls()
#obj_controls.alarms("a1ebc37f43ee497ca453f84a9e9e7d11")
#obj_controls.commands()
#obj_controls.lights()
