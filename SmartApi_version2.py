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

check_start = 1

## for speech to speech interaction
class SmartApi():
    def __init__(self):
        self.fixed_url = "http://codeglobal.in/home_automation1/update.php?"


    ## takes the command from user through Microphone
    def myCommand(self):
        "Takes the command from user through voice"
        ## function to be executed till internet connectivity is available again
        #engine.say('I am ready for your command sir')
        #engine.runAndWait()
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
                #loop back to continue to listen for commands if unrecognizable speech is received
                except sr.UnknownValueError:
                    print("We couldn't understand your last command \nTry Again!")
                    engine.say("We couldn't understand your last command Try Again!")
                    engine.runAndWait()
                ## recursion if no input is provided by the user 
                    command = self.myCommand();
                except sr.RequestError as e:
                    print ("Could not request your results due to lost connectivity")
                    engine.say("Could not request your results due to lost connectivity")
                    engine.runAndWait()
                    self.myCommand()
                except Exception as e :
                    print ("Unknown Issues")
                    self.myCommand()
        except Exception as e:
            print ("Unknown Issues executed")
            print (e)
            self.myCommand()

class controls(SmartApi):

    ## to access alarms and remainder 
    ## to access alarms and remainder 
    def alarms(self):

        ## typical statement will be of form , set alarm to 7:00 p.m. for Monday
        self.response = {}

        self.response['api_key'] = "a1ebc37f43ee497ca453f84a9e9e7d11"
        ## parser.parse is used but it doesn't give good result always
        while 1:
            ##http://codeglobal.in/home_automation1/fetchalarmdetails.php?api_key=a1ebc37f43ee497ca453f84a9e9e7d11
            fixed_fetch_url = "http://codeglobal.in/home_automation1/fetchalarmdetails.php?"
            fixed_alarm_url = "http://codeglobal.in/home_automation1/alarm.php?"
            print ("typical statement of form , set  alarm to 7:00 p.m. for Monday or remove alarm to 7:00 p.m. for Monday , to see exiting alarms say see my previous alarms")
            #engine.say("typical statement of form , set  alarm to 7:00 p.m. for monday or remove alarm to 7:00 p.m. for monday")
            #engine.runAndWait()


            #alarm_set =  SmartApi.myCommand(self)
            alarm_set = raw_input("set alarm = ")
            
            if re.search(r'alarm' , alarm_set) and (re.search(r'set' , alarm_set) or re.search(r'remove' , alarm_set)):
                date_time = str(parser.parse(alarm_set , fuzzy = True))
                date_time = date_time.split(" ")

                ## user customized regex for recognition of day and time of alarm_set
                if re.findall(r'monday' , alarm_set):
                   alarm_day = re.findall(r'monday' , alarm_set)[0]
                if re.findall(r'tuesday' , alarm_set):
                   alarm_day = re.findall(r'tuesday' , alarm_set)[0]
                if re.findall(r'wednesday' , alarm_set):
                   alarm_day = re.findall(r'wednesday' , alarm_set)[0]
                if re.findall(r'thursday' , alarm_set):
                   alarm_day = re.findall(r'thursday' , alarm_set)[0]
                if re.findall(r'friday' , alarm_set):
                   alarm_day = re.findall(r'friday', alarm_set)[0]
                if re.findall(r'saturday' , alarm_set):
                   alarm_day = re.findall(r'saturday' , alarm_set)[0]
                if re.findall(r'sunday' , alarm_set):
                   alarm_day = re.findall(r'sunday' , alarm_set)[0]

                ## use of regex to find exact time 
                '''
                time = (re.findall(r' [0-1]?[0-9]:?.?[0-5][0-9].?p\.m\.| [0-1]?[0-9]:?.?[0-5][0-9].?p\.m\.|[0-1]?[0-9].?p\.m\ | [0-1]?[0-9].?a\.m\.', alarm_set ))
                '''
                week_days = {0 : 'monday' , 1 : 'tuesday' , 2 : 'wednesday' , 3 : 'thursday' , 4 : 'friday' , 5 : 'saturday' , 6 : 'sunday'}
                alarm_time , alarm_date = date_time[1] , date_time[0]

                if re.findall(r'remove' , alarm_set):
                    mode = 'remove'
                elif re.findall(r'set' , alarm_set):
                    mode = 'set'

                ## thus 4 things are to be passed in the database 
                ## action , alarm_day , alarm_date , alarm_time

                try :
                    print (alarm_day)
                except Exception as e:
                    print ('day is not specified so by default current day is used')
                    day = parser.parse(alarm_s , fuzzy = True).weekday()
                    alarm_day = week_days[day]

                ## converting into milliseconds 
                date_time = str(parser.parse(alarm_set , fuzzy = True))
                dt = datetime.strptime(str(date_time) , "%Y-%m-%d %H:%M:%S")
                time_milli = time.mktime(dt.timetuple())*1000 + int(76)*10                
                alarm_url = fixed_alarm_url + 'api_key='+self.response['api_key']+'&mode='+mode+'&alarm_date='+alarm_date+'&alarm_day='+alarm_day+'&alarm_time='+alarm_time+'&time='+str(time_milli)
                '''
                print ("mode = %s " %(mode))                
                print ("time = %s" %(alarm_time))
                print ("date = %s "%(alarm_date)) 
                print ("alarm_day = %s"%(alarm_day))               
                print (alarm_url)
                '''

                try:
                    r = requests.get(alarm_url)
                    output = ast.literal_eval(r.text)
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

                    engine.say("do you want to set another alarm yes or no")
                    engine.runAndWait()

                    ## call the SmartApi()
                    #user_input = SmartApi.myCommand(self)
                except requests.exceptions.Timeout as e:
                    print ("Timeout ! Try Again")
                    engine.say("timeout try again")
                    engine.runAndWait()
                    self.alarms()
                except requests.exceptions.TooManyRedirects:
                    print ("Too Many Requests")
                    print ("Too Many Requests")
                    engine.say("too Many requests")
                    engine.runAndWait()
                    self.alarms()
                except requests.exceptions.RequestException as e:
                    print ("lost connectivity")
                    engine.say("lost connectivity")
                    engine.runAndWait()
                    self.alarms()

            elif re.search(r'previous' , alarm_set) and re.search(r'alarm' , alarm_set):
                fetch_url =  fixed_fetch_url + "api_key="+self.response['api_key']
                print (fetch_url)
                try:
                    r = requests.get(fetch_url)
                    #print (r.text)
                    if not(re.search(r'Date' , r.text)):
                        print ("no alarm has been set")
                    else :
                        alarm_status = r.text
                        alarm_status = ast.literal_eval(alarm_status)
                        #print (alarm_status)
                        for status in alarm_status:
                            result_status = "your alarm is on " + status['Day'] +  " at " + status['Time']
                            print (result_status)
                except requests.exceptions.Timeout:
                    print ("Timeout ! Try Again")
                    engine.say("timeout try again")
                    engine.runAndWait()
                    self.alarms()
                except requests.exceptions.TooManyRedirects:
                    print ("Too Many Requests")
                    engine.say("too Many requests")
                    engine.runAndWait()
                    self.alarms()
                except requests.exceptions.RequestException as e:
                    print ("lost connectivity")
                    engine.say("lost connectivity")
                    engine.runAndWait()
                    self.alarms()


            else :  
                self.alarms()
                print ("Wrong command , Try Again !")
                engine.say("wrong command , try Again")
                engine.runAndWait()                

            while 1:
                user_input = raw_input("do you want to set another alarm , yes or no \n")
                if re.search(r'no' , user_input):
                    return 1
                elif re.search(r'yes' , user_input) :
                    break
                else :
                    print ("Wrong Input , Try Again !")
                    engine.say("rong input , try again")
                    engine.runAndWait()


    ## lights function for accessing the lights 
    def lights(self):

        self.response = {}
        self.response['api_key'] = "a1ebc37f43ee497ca453f84a9e9e7d11"

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

            #device_operate = SmartApi.myCommand(self)
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
                print ("\n\n")
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

        ## >>>> #extract_command = str(SmartApi.myCommand(self))
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

                ## >>>> extra   self.mail_id = SmartApi.myCommand(self)
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
                                            #>>>>>>>>>>>>>>>>>>>>>>>>>>>            #self.device_operate = SmartApi.myCommand(self)
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
                                            #user_input = SmartApi.myCommand(self)
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
class assistant(SmartApi):

    def reddit(self):
        command = SmartApi.myCommand(self)
        if 'open reddit' in command:
            reg_ex = re.search('open reddit (.*)', command)
            url = 'https://www.reddit.com/'
            if reg_ex:
                subreddit = reg_ex.group(1)
                url = url + 'r/' + subreddit
            webbrowser.open(url)
            print('Done!')
            engine.say("Done")
            engine.runAndWait()
    def talkback(self):
        command =SmartApi.myCommand(self)
        if "how are you" in command:
            engine.say('i am fine, what about you')
            engine.runAndWait()
        elif "tell me about your features" in command:
            engine.say('i am specially designed as a personal home assistant, i can'
                       'switch on and off Lights, fans, tv, air conditioners, set alarm and reminder')
            engine.runAndWait()
        elif "who are you" in command:
            engine.say('i am a smart intelligence system, designed by satyam sir')
            engine.runAndWait()
        elif 'open website' in command:
            reg_ex = re.search('open website (.+)', command)
            if reg_ex:
                domain = reg_ex.group(1)
                url = 'https://www.' + domain
                try :
                    webbrowser.open(url)
                    print('Done!')
                    engine.say("Done")
                    engine.runAndWait()
                except Exception as e:
                    print (e)
            else:
                pass

        elif 'what are you doing' in command:
            engine.say('Just doing my thing')
            engine.runAndWait()
        elif 'joke' in command:
            res = requests.get(
                    'https://icanhazdadjoke.com/',
                    headers={"Accept":"application/json"}
                    )
            if res.status_code == requests.codes.ok:
                engine.say(str(res.json()['joke']))
                engine.runAndWait()
            else:
                engine.say('oops!I ran out of jokes')
                engine.runAndWait()

    def weather(self):
        command = SmartApi.myCommand(self)
        if 'weather in' in command:
            reg_ex = re.search('weather in (.*)', command)
            if reg_ex:
                city = reg_ex.group(1)
                weather = Weather()
                location = weather.lookup_by_location(city)
                condition = location.condition()
                engine.say('The Current weather in %s is %s The tempeture is %.1f degree' % (city, condition.text(), (int(condition.temp())-32)/1.8))
                engine.runAndWait()
            
        elif 'weather forecast in' in command:
            reg_ex = re.search('weather forecast in (.*)', command)
            if reg_ex:
                city = reg_ex.group(1)
                weather = Weather()
                location = weather.lookup_by_location(city)
                forecasts = location.forecast()
                for i in range(0,3):
                    engine.say('On %s will it %s. The maximum temperture will be %.1f degree.'
                             'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))
                    engine.runAndWait()

            else:
                engine.say('I don\'t know what you mean!')
                engine.runAndWait()

    def search(self):
        command = SmartApi.myCommand(self)
        if 'who is' in command:
            command = command.split()
            name = command[2]
            print("Hold on satyam, I will tell you who " + name + " is.")
            sam= wikipedia.summary(name, sentences=3)
            engine.say(sam)
            engine.runAndWait()
    

## creating the object 
obj_SmartApi = SmartApi()      
#x = obj_SmartApi.myCommand()
obj_controls =  controls()
#obj_controls.commands()
#obj_controls.alarms()
obj_controls.lights()