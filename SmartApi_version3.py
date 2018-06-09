## for multiple devices 
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
 
    def alarms(self , response):
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
                alarm_url = fixed_alarm_url + 'api_key='+response['api_key']+'&mode='+mode+'&alarm_date='+alarm_date+'&alarm_day='+alarm_day+'&alarm_time='+alarm_time+'&time='+str(time_milli)
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
                fetch_url =  fixed_fetch_url + "api_key="+response['api_key']
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

        self.response = response

        fixed_url = "http://codeglobal.in/home_automation1/update.php?"

        while 1 :
            ## which device to operate by user  
            print ("\n")
            print ("options for light controls are \n device 1 \n device 2 \n device 3 \n device 4 \n all devices\n")              
            #engine.say("options for light controls are device 1 device 2 device 3 device 4 and all devices ")              
            #engine.runAndWait()

            print ("choose your light which you want to turn on or off , if you want to logout say logout , and for controling other devices say go back ")
            print ("in order to check the status of lights say check status of lights")
            #engine.say("choose your light which you want to turn on or off , if you want to logout say logout , and for controling other devices say go back ")
            #engine.runAndWait()

            ## checking the device input by user 

            #device_operate = SmartApi_try.myCommand(self)
            ##>>>>> change this 
            device_operate =  raw_input("device_operate = ")
            #print (str(device_operate))

            ## check the current status of all devices 
            device_status = str(requests.get("http://codeglobal.in/home_automation1/read_all.php?api=a1ebc37f43ee497ca453f84a9e9e7d11").text)
            device_status = ast.literal_eval(device_status)['hardware'][0]
            ## upgrade for all other devices 
            if re.search("device" , str(device_operate)) and re.search("off|of" , str(device_operate)):
                if re.search(r" 1 | one " , str(device_operate)):
                    if device_status['status1'] == 'off':
                        print ("device 1 is already off")
                        engine.say("device 1 is already off")
                        engine.runAndWait()
                    else :
                        url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status1"+"="+"off"
                        requests.get(url_parsed)
                        print (url_parsed)                                #print (url_parsed)
                        ## check the status of all other device 
                        #print (device_status)
                elif re.search(r"2 | to | two " , str(device_operate)):
                    if device_status['status2'] == 'off':
                        print ("device 2 is already off")
                        engine.say("device 2 is already off")
                        engine.runAndWait()
                    else :
                        url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status2"+"="+"off"
                        requests.get(url_parsed) #print (url_parsed)
                        ## check the status of all other device 
                        #print (device_status)
                elif re.search(r" 3 | three | tree " , str(device_operate)):
                    if device_status['status3'] == 'off':
                        print ("device 3 is already off")
                        engine.say("device 3 is already off")
                        engine.runAndWait()
                    else :
                        url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status3"+"="+"off"
                        requests.get(url_parsed)                                #print (url_parsed)
                        ## check the status of all other device 
                        #print (device_status)                    
                elif re.search(r" 4 | four " , str(device_operate)):
                    if device_status['status4'] == 'off':
                        print ("device 4 is already off")
                        engine.say("device 4 is already off")
                        engine.runAndWait()
                    else :
                        url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status4"+"="+"off"
                        requests.get(url_parsed)                                #print (url_parsed)
                        ## check the status of all other device 
                        #print (device_status)
                elif re.search(r"all" , str(device_operate)):
                    if device_status['status1'] == 'off' and device_status['status2'] == 'off' and device_status['status3'] == 'off' and device_status['status4'] == 'off':
                        print ("all devices are  already off")
                        engine.say("all devices are already off")
                        engine.runAndWait()
                    else :
                        requests.get(fixed_url+"api_key="+self.response["api_key"]+"&"+"status1"+"="+"off")
                        requests.get(fixed_url+"api_key="+self.response["api_key"]+"&"+"status2"+"="+"off")
                        requests.get(fixed_url+"api_key="+self.response["api_key"]+"&"+"status3"+"="+"off")
                        requests.get(fixed_url+"api_key="+self.response["api_key"]+"&"+"status4"+"="+"off")
                        ## check the status of all other device 
                        #print (device_status)
                else :
                    engine.say("no such device registered")
                    engine.runAndWait()
                    print ("no such device registered")
                    self.lights()
            elif re.search("device" , str(device_operate)) and re.search("on" , str(device_operate)):
                if re.search(r" 1 | one " , str(device_operate)):
                    if device_status['status1'] == 'on':
                        print ("device 1 is already on")
                        engine.say("device 1 is already on")
                        engine.runAndWait()
                    else :
                        url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status1"+"="+"on"
                        requests.get(url_parsed)                    #print (url_parsed)
                        ## check the status of all other device 
                        #print (device_status)
                elif re.search(r" 2 | to | two " , str(device_operate)):
                    if device_status['status2'] == 'on':
                        print ("device 2 is already on")
                        engine.say("device 2 is already on")
                        engine.runAndWait()
                    else :
                        url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status2"+"="+"on"
                        requests.get(url_parsed)                    #print (url_parsed)
                        ## check the status of all other device 
                        #print (device_status)
                elif re.search(r" 3 | three | tree " , str(device_operate)):
                    if device_status['status3'] == 'on':
                        print ("device 3 is already on")
                        engine.say("device 3 is already on")
                        engine.runAndWait()
                    else :
                        url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status3"+"="+"on"
                        requests.get(url_parsed)                    #print (url_parsed)
                        ## check the status of all other device 
                        #print (device_status)
                elif re.search(r" 4 | four " , str(device_operate)):
                    if device_status['status4'] == 'on':
                        print ("device 4 is already on")
                        engine.say("device 4 is already on")
                        engine.runAndWait()
                    else :
                        url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status4"+"="+"on"
                        requests.get(url_parsed)                    #print (url_parsed)
                        ## check the status of all other device 
                        #print (device_status)
                elif re.search(r"all" , str(device_operate)):
                    if device_status['status1'] == 'on' and device_status['status4'] == 'on' and device_status['status3'] == 'on' and device_status['status2'] == 'on':
                        print ("all devices are already on")
                        engine.say("all devices are already on")
                        engine.runAndWait()
                    else:
                        requests.get(fixed_url+"api_key="+self.response["api_key"]+"&"+"status1"+"="+"on")
                        requests.get(fixed_url+"api_key="+self.response["api_key"]+"&"+"status2"+"="+"on")
                        requests.get(fixed_url+"api_key="+self.response["api_key"]+"&"+"status3"+"="+"on")
                        requests.get(fixed_url+"api_key="+self.response["api_key"]+"&"+"status4"+"="+"on")
                        ## check the status of all other device 
                        #print (device_status)
                else :
                    engine.say("no such device registered")
                    engine.runAndWait()
                    print ("no such device registered")
                    self.lights()
            elif re.search(r"log.?out" , str(device_operate)):
                self.response["api_key"] = None
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
                self.lights()



    def commands(self):
        ## extracting variables from the command for user defined input
        ## call the function of base class for taking the input command through speech

        print ("1.to control devices please login ! , say home automation login \nto exit the console say exit")
        #engine.say("to control devices please login for login , say home automation login to exit the console say exit")
        #engine.runAndWait()

        ## >>>> #extract_command = str(SmartApi_try.myCommand(self))
        extract_command = raw_input('extract_command = ')
        ## this loop works fine and returns only expected value
        if re.search(r"home automation" , extract_command) and re.search(r"login" , extract_command) :

            ## once login and password are it should be in infinte loop 
            ## and after a fixed time say 5 mins the program ends 
            ## only 3 attempts are allowed for mail_id input
            for i in [0,1,2]:
                ## in general program we will match through usernames not mail ids
                ## that too from stored data in database
                print ("Your mail id please !")
                #engine.say('Your mail id please !')
                #engine.runAndWait()

                ## takes the input for mail_id

                ## >>>> extra   self.mail_id = SmartApi_try.myCommand(self)
                self.mail_id = 'chetna agarwal'

                ## taking the password for only 1 id , 
                ## that can be upgraded afterwards , for multiple users

                ## to check the mail id of user if mail id matches then ask for password only
                if self.mail_id == "chetna agarwal":

                    ## taking password for the ids but only 3 attempts are allowed  
                    flag = 3
                    engine.say("Enter your password")
                    engine.runAndWait()
                    password = raw_input("Enter your password = ")                  
                    while re.search("chetna agarwal" , str(self.mail_id)):
                        ## if password is correct then ask for device operations (3 attempts)
                        if password == "chetna":
                            ## it can be reomved only if we call lights or alarm function after it  , user_log for login confirmation
                            ## confirming the log in by voice output
                            print ("You are logged in %s" %(self.mail_id))
                            engine.say("You are logged in %s" %(self.mail_id))
                            engine.runAndWait()

                            try :
                                requests_out =  requests.get("http://codeglobal.in/home_automation1/android_login.php?tag=login&user=chetna.agarwal@codeglobal.in&pass="+password)
                                ## checking the output of both json and text to get the api_key
                                print ("json output of the response \n %s"%(requests_out.json))
                                ## in case of response 200 , print "ok"
                                if int(re.findall(r'[0-9]+', str(requests_out.json))[0]) == 200:
                                    print ("OK")
                                    while 1:
                                        ## taking out API key from the response 
                                        self.response = ast.literal_eval(requests_out.text)
                                        user_input = 'yes'
                                        while (re.search(user_input , 'yes')):
                                            ## which device to operate by user  
                                            print ("what do you want to control \n1. alarm  \n2. lights")
                                            engine.say("choose one of them what do you want to control alarm or lights")
                                            engine.runAndWait()                                             
                                            #>>>>>>>>>>>>>>>>>>>>>>>>>>>            #self.device_operate = SmartApi_try.myCommand(self)
                                            self.device_operate = raw_input("device operate = ")
                                            ## more devices can be added in this module at 
                                            if re.search(r'lights|light' , self.device_operate) :
                                                ## call lights
                                                ## checking the status of lights
                                                self.lights()
                                            elif re.search(r'alarm' , self.device_operate):
                                                print ("Module is incomplete") 
                                                engine.say("Module is incomplete")
                                                engine.runAndWait()
                                                ## call alarm function here
                                            else :
                                                print ("I cannot control %s " %self.device_operate)
                                                engine.say("I cannot control %s " %self.device_operate)
                                                engine.runAndWait()
                                            
                                            ## for another session
                                            print ("do you want to operate other devices , yes or no") 
                                            engine.say("do you want to operate other devices , yes or no")
                                            engine.runAndWait()
                                            #>>>>>>>>>>>>>>>>>>>>>>>>>>>           
                                            #user_input = SmartApi_try.myCommand(self)
                                            user_input =  raw_input("user_input = ")
                                            if re.search('no' , user_input) or re.search('logout',  user_input):
                                                print ("logging out of system")
                                                engine.say("logging out of system")
                                                engine.runAndWait()
                                                self.response['api_key'] = "0"
                                                self.commands()
                                            else :
                                                pass
                            except requests.exceptions.Timeout as e:
                                print ("Timeout ! Try Again !")
                                engine.say("timeout try again")
                                engine.runAndWait()
                                self.commands()
                            except requests.exceptions.TooManyRedirects:
                                print ("Too Many Requests passed , Try Again !")
                                engine.say("too many requests")
                                engine.runAndWait()
                                self.commands()
                            except requests.exceptions.RequestException as e:
                                print ("lost connectivity . Try Again !")
                                engine.say("lost connectivity try again")
                                engine.runAndWait()
                                self.commands()
                        elif flag > 0:
                        ## for wrong attempts
                            engine.say("Enter your password")
                            engine.runAndWait()
                            password = raw_input("Enter your password = ") 
                            flag = flag - 1
                        else :
                            print ("Exceeded the number of attempts , Try Again")
                            engine.say("Exceeded the number of attempts , Try Again")
                            engine.runAndWait()
                            sys.exit(0)
        
 
            ## we will exit  while loop only after flag becomes 0
            ## variable to check no of attempts  
            else :   
                print ("three wrong attempts for mail id , try again")
                engine.say("three wrong attempts for mail id , try again")
                engine.runAndWait()
                print ("Exiting the program ")
                engine.say("Exiting the program")
                engine.runAndWait()
                sys.exit()
   
            
        elif re.search(r'exit' , extract_command):
            print ("Exiting the console")
            engine.say("Exiting the console")
            engine.runAndWait()
            sys.exit()
        else :
            print ("Unexpected command given by user ")
            self.commands()
            engine.say("Unexpected command given by user")
            engine.runAndWait()            

## for simple commands using speech

    

## creating the object 
##obj_SmartApi_try = SmartApi_try()      
##x = obj_SmartApi_try.myCommand()
##obj_controls =  controls()
##obj_controls.commands()
##obj_controls.alarms()
##obj_controls.lights()