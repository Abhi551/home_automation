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


from dateutil import parser
from gtts import gTTS

engine =  pyttsx.init()
voices = engine.getProperty("voices")
engine.setProperty('voice' , voices[1].id)
engine.setProperty('rate' , 150)

##http://codeglobal.in/home_automation1/alarm.php?api_key=XXXXXXXXXXXXXXXXXXXXXX&mode=set&alarm_date=2018-06-11&alarm_time=19:00:00&alarm_day=monday
url = "http://codeglobal.in/home_automation1/alarms.php?api_key=456dsfmdm455&mode=set&time=bsdh&hours="

class SmartApi():
    def __init__(self):
        self.fixed_url = "http://codeglobal.in/home_automation1/update.php?"


    ## takes the command from user through Microphone
    def myCommand(self):
        "Takes the command from user through voice"
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
            #loop back to continue to listen for commands if unrecognizable speech is received
                except sr.UnknownValueError:
                    print("We couldn't understand your last command \nTry Again!")
                    engine.say("we couldn't understand your last command Try Again!")
                    engine.runAndWait()
                ## recursion if no input is provided by the user 
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
            

class controls(SmartApi):

    ## to access alarms and remainder 
    def alarms(self):


        ## typical statement will be of form , set alarm to 7:00 p.m. for Monday
        self.response = {}

        ## parser.parse is used but it doesn't give good result always
        while 1:
            ##http://codeglobal.in/home_automation1/fetchalarmdetails.php?api_key=x
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
                else :
                    mode = 'set'

                ## thus 4 things are to be passed in the database 
                ## action , alarm_day , alarm_date , alarm_time
                print ("time = %s" %(alarm_time))
                print ("date = %s "%(alarm_date))
                try :
                    print ('day = %s' %(alarm_day))
                except Exception as e:
                    print ('day is not specified so by default current day is used')
                    day = parser.parse(alarm_set , fuzzy = True).weekday()
                    print ('day = %s' %week_days[day])
                    alarm_day = week_days[day]
                print ("mode = %s " %(mode))
                alarm_url = fixed_alarm_url + 'api_key='+self.response['api_key']+'&mode='+mode+'&alarm_date='+alarm_date+'&alarm_day='+alarm_day+'&alarm_time='+alarm_time
                
                #print (alarm_url)
                
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
                    elif output['success'] == "-2":
                        print ("alarm doesn't exit " )
                        engine.say("alarm doesn't exist")
                        engine.runAndWait()
                    else :
                        print ("unrecognizable operations")
                        engine.say("unrecognizable operations")
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
                    self.alarms()
                except requests.exceptions.RequestException as e:
                    print ("lost connectivity")
                    engine.say("lost connectivity")
                    engine.runAndWait()
                    self.alarms()

            elif re.search(r'previous' , alarm_set) and re.search(r'alarm' , alarm_set):
                fetch_url =  fixed_fetch_url + "api_key="+self.response['api_key']
                try:
                    r = requests.get(fetch_url)
                    alarm_status = r.text.encode("UTF8")[2:-1]
                    alarm_status=list(ast.literal_eval(alarm_status))
                    for status in alarm_status[1:]:
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

        fixed_url = "http://codeglobal.in/home_automation1/update.php?"

        ## working on device 2 only
        ## checking the device input by user 
        
        while 1 :
            print ("which light you want to turn on or off ,say device 2 on or device 2 off , to enter main console say go back" )
            engine.say("which light you want to turn on or off ,say device 2 on or device 2 off , to enter main console say go back")
            engine.runAndWait()
            #>>>>>>device_operate = SmartApi.myCommand(self)
            device_operate = raw_input("device_operate = ")
            print (str(device_operate))
            ## upgrade for all other devices 
            device_status = str(requests.get("http://codeglobal.in/home_automation1/read_all.php?api="+self.response['api_key'].text)
            device_status = ast.literal_eval(device_status)['hardware'][0]

            if re.search("device 2|device to" , str(device_operate)) and re.search("on" , str(device_operate)):
                if device_status['status2'] == 'on':
                    print ("device 2 is already on")
                    engine.say("device 2 is already on")
                    engine.runAndWait()
                else :
                    url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status2"+"="+"on"
                    requests.get(url_parsed) #print (url_parsed)
                    ## check the status of all other device
                    print (device_status) 
                    print ("device gets on")
            elif re.search("device 2|device to" , str(device_operate)) and re.search("off" , str(device_operate)):
                if device_status['status2'] == 'off':
                    print ("device 2 is already off")
                    engine.say("device 2 is already off")
                    engine.runAndWait()
                else :
                    url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status2"+"="+"off"
                    requests.get(url_parsed) #print (url_parsed)
                    ## check the status of all other device 
                    print (device_status)
                    print ("device gets off")
            elif re.search("logout" , str(device_operate)):
                response["api_key"] = None
                print ("Exiting the Smart Api")
                engine.say("exiting the smart api")
                engine.runAndWait()
                sys.exit()
            elif re.search('go' , str(device_operate)) and re.search('back', str(device_operate)):
                return 1
            else :
                print ("nothing fetched")
                self.lights()


    def commands(self):
        ## extracting variables from the command for user defined input
        ## call the function of base class for taking the input command through speech

        print ("1.to control devices please login ! , say home automation login \nto exit the console say exit")
        engine.say("to control devices please login !") 
        engine.say("for login , say home automation login")
        engine.say("to exit the console say exit")
        engine.runAndWait()

        #>>>> extract_command = SmartApi.myCommand(self)
        extract_command = raw_input("extract_command = ")

        ## this loop works fine and returns only expected value
        if re.search(r"home automation" , extract_command) and re.search(r"login" , extract_command) :

            ## once login and password are it should be in infinte loop 
            ## and after a fixed time say 5 mins the program ends 
            ## only 3 attempts are allowed for mail_id input
            for i in [0,1,2]:
                ## in general program we will match through usernames not mail ids
                ## that too from stored data in database
                print ("Your mail id please !")
                engine.say('Your mail id please !')
                engine.runAndWait()

                ## takes the input for mail_id
                
                #self.mail_id = SmartApi.myCommand(self)
                self.mail_id = raw_input("mail_id = ")
                ## taking the password for only 1 id , 
                ## that can be upgraded afterwards , for multiple users

                ## to check the mail id of user if mail id matches then ask for password only
                if self.mail_id == "xxxxxxxx":
                    ## taking password for the ids but only 3 attempts are allowed  
                    flag = 3
                    engine.say("enter your password")
                    engine.runAndWait()
                    password = raw_input("Enter your password = ")                  
                    while re.search("xxxxxxx" , str(self.mail_id)):
                        ## if password is correct then ask for device operations (3 attempts)
                        if password == "xxxxx":
                            ## it can be reomved only if we call lights or alarm function after it  , user_log for login confirmation
                            ## confirming the log in by voice output
                            print ("You are logged in %s" %(self.mail_id))
                            engine.say("you are logged in %s" %(self.mail_id))
                            engine.runAndWait()

                            requests_out =  requests.get("http://codeglobal.in/home_automation1/android_login.php?XXXXXXXXXXXXXXXXXXXXXX"+password)
                            
                            ## checking the output of both json and text to get the api_key
                            print ("json output of the response \n %s"%(requests_out.json))
                            ## in case of response 200 , print "ok"

                            ## only if the response recieved is 200
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
                                        print (self.device_operate)
                                        if re.search(r'lights|light' , self.device_operate) :
                                            ## call lights
                                            self.lights()
                                        elif re.search(r'alarm' , self.device_operate):
                                            ## call alarm function 
                                            self.alarms()
                                        else :
                                            print ("I cannot control %s " %self.device_operate)
                                            engine.say("i cannot control %s " %self.device_operate)
                                            engine.runAndWait()
                                        
                                        ## for another session
                                        print ("do you want to operate other devices , yes or no") 
                                        engine.say("do you want to operate other devices , yes or no")
                                        engine.runAndWait()
                                        #>>>>>>>>>>>>>>>>>>>>>>>>>>>           user_input = SmartApi.myCommand(self)
                                        user_input =  raw_input("user_input = ")
                                        if re.search('no' , user_input) or re.search('logout',  user_input):
                                            print ("logging out of system")
                                            engine.say("logging out of system")
                                            engine.runAndWait()
                                            self.response['api_key'] = "0"
                                            self.commands()
                                        else :
                                            pass



                        elif flag > 0:
                        ## for wrong attempts
                            flag =  flag - 1
                            engine.say("enter your password")
                            engine.runAndWait()
                            password = raw_input("Enter your password = ") 
                            
                        else :
                            print ("Exceeded the number of attempts , Try Again")
                            engine.say("exceeded the number of attempts , try again")
                            engine.runAndWait()
                            sys.exit(0)
            else :
                print ("wrong attempts exceeded")
                print ("Exiting the program ")
                engine.say("exiting the program")
                engine.runAndWait()
                sys.exit()

        
 
            ## we will exit  while loop only after flag becomes 0
            ## variable to check no of attempts        
            
        elif re.search(r'exit' , extract_command):
            print ("Exiting the console")
            engine.say("exiting the console")
            engine.runAndWait()
            sys.exit()
        else :
            print ("Unexpected command given by user ")
            engine.say("unexpected command given by user")
            engine.runAndWait()     
            self.commands()       
## creating the object 
#obj_SmartApi = SmartApi()      

obj_controls = controls()
obj_controls.alarms()
#obj_controls.commands()
#obj_controls.lights()
