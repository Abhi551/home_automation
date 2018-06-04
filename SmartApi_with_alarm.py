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

url = "http://codeglobal.in/home_automation1/alarms.php?mode=set&time=bsdh&hours="
class controls(SmartApi):

    ## to access alarms and remainder 
    def alarms():
        ## first parser is used but it doesn't give result always and it doesn't recognize the days of wee
        while 1:
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

                time = (re.findall(r' [0-1]?[0-9]:?.?[0-5][0-9].?p\.m\.| [0-1]?[0-9]:?.?[0-5][0-9].?p\.m\.|[0-1]?[0-9].?p\.m\ | [0-1]?[0-9].?a\.m\.', alarm ))
                print (time)
                print (day)
                print (date_time)
                ## parse this into database  
                #return (date_time , day , time)
                engine.say("do you want to set another alarm yes or no")
                engine.runAndWait()
                ## call the SmartApi()
                user_input = raw_input("do you want to set another alarm , yes or no ")
                if re.search(r'no',user_input):
                    return 1
            except Exception as e:
                print (e)
                print ("alarm set in wrong format")


    ## lights function for accessing the lights 
    def lights(self):

        fixed_url = "http://codeglobal.in/home_automation1/update.php?"


        ## which device to operate by user                
        print ("which light you want to turn on or off ,say device 2 on or device 2 off , to enter main console say go back" )
        engine.say("which light you want to turn on or off ,say device 2 on or device 2 off , to enter main console say go back")
        engine.runAndWait()

        ## working on device 2 only
        ## checking the device input by user 
        device_operate = SmartApi.myCommand(self)
        print (str(device_operate))

        while 1 :

            #requests.get("http://codeglobal.in/home_automation1/update.php?api_key=a1ebc37f43ee497ca453f84a9e9e7d11&status2=off
            ## upgrade for all other devices 
            response = {'api_key' : "a1ebc37f43ee497ca453f84a9e9e7d11"}
            if re.search("device 2|device to" , str(device_operate)) and re.search("on" , str(device_operate)):
                url_parsed =  fixed_url+"api_key="+response["api_key"]+"&"+"status2"+"="+"on"
                print (url_parsed)
                print ("device gets on")
                requests.get(url_parsed)
            elif re.search("device 2|device to" , str(device_operate)) and re.search("off" , str(device_operate)):
                url_parsed =  fixed_url+"api_key="+response["api_key"]+"&"+"status2"+"="+"off"
                requests.get(url_parsed)
                print ("device gets off")
            elif re.search("logout" , str(device_operate)):
                response["api_key"] = None
                print ("Exiting the Smart Api")
                engine.say("Exiting the Smart Api")
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

        extract_command = SmartApi.myCommand(self)
    

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
                self.mail_id = SmartApi.myCommand(self)

                ## taking the password for only 1 id , chetna agarwal
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

                            requests_out =  requests.get("http://codeglobal.in/home_automation1/android_login.php?tag=login&user=chetna.agarwal@codeglobal.in&pass=chetna")
                            
                            ## checking the output of both json and text to get the api_key
                            print ("json output of the response \n %s"%(requests_out.json))
                            ## in case of response 200 , print "ok"

                            ## only if the response recieved is 200
                            if int(re.findall(r'[0-9]+', str(requests_out.json))[0]) == 200:
                                print ("OK")
                                while 1:
                                    ## taking out API key from the response 
                                    response = ast.literal_eval(requests_out.text)
                                    user_input = 'no'
                                    while not((re.search("yes", user_input) or (re.search("logout" , user_input)): 
                                        print ("what do you want to control \n1. alarm  \n2.lights")
                                        engine.say("choose one of them what do you want to control alarm or lights")
                                        engine.runAndWait()                                             
                                        self.device_operate = SmartApi.myCommand(self)
                                        if re.search(r'lights|light' , self.device_operate):
                                            ## call lights
                                            self.lights()
                                        elif re.search(r'alarm' , self.device_operate):
                                            engine.runAndWait()
                                            return ("Module is incomplete") 
                                        engine.say("do you want to logout , yes or no")
                                        engine.runAndWait()
                                        user_input = SmartApi.myCommand(self)
                                    elif re.search("logout" , user_input) or re.search("yes" , user_input) :
                                        print ("logging out of system")
                                        engine.say("logging out of system")
                                        engine.runAndWait()
                                        sys.exit()
                                        ## which device to operate by user   




                        elif flag > 0:
                        ## for wrong attempts
                            flag =  flag - 1
                            engine.say("Enter your password")
                            engine.runAndWait()
                            password = raw_input("Enter your password = ") 
                            
                        else :
                            print ("Exceeded the number of attempts , Try Again")
                            engine.say("Exceeded the number of attempts , Try Again")
                            engine.runAndWait()
                            sys.exit(0)
        
 
            ## we will exit  while loop only after flag becomes 0
            ## variable to check no of attempts        
            
        elif re.search(r'exit' , extract_command):
            print ("Exiting the console")
            engine.say("Exiting the console")
            engine.runAndWait()
            sys.exit()
        else :
            print ("Unexpected command given by user ")
            engine.say("Unexpected command given by user")
            engine.runAndWait()            
## creating the object 
obj_SmartApi = SmartApi()      

obj_controls = controls()
obj_controls.commands()
obj_controls.lights()
