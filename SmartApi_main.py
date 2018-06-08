import pyttsx
import speech_recognition as sr
import os
import nltk
import re
import requests
import ast 
import time 
import sys

from statistics import mode
#import recognition
#import face_recognition
import try2

## import other modules also
class SmartApi():
    ## takes the command from user through Microphone
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
            	#loop back to continue to listen for commands if unrecognizable speech is received
                except sr.UnknownValueError:
                    print("We couldn't understand your last command \nTry Again!")
                    engine.say("we couldn't understand your last command Try Again!")
                    engine.runAndWait()
                    command = self.myCommand() ##if no input is provided by the user 
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
    def valid_func(self , password , ):
    	try:
    		## run function from try2 file
            requests_out =  requests.get("http://codeglobal.in/home_automation1/android_login.php?tag=login&user=chetna.agarwal@codeglobal.in&pass="+password)
           	requests_out =      
            ##print ("json output of the response \n %s"%(requests_out.json))
          	## only if 200 recieved  
            if int(re.findall(r'[0-9]+', str(requests_out.json))[0]) == 200:
                print ("OK")
                while 1:
                    response = ast.literal_eval(requests_out.text)
                    user_input = 'yes'
                    while (re.search(r'yes',user_input)):
                        ## which device to operate by user  
                        print ("what do you want to control \n1. alarm  \n2. lights")
                        #engine.say("choose one of them what do you want to control alarm or lights")
                        #engine.runAndWait()                                             
                        ##device_operate = SmartApi.myCommand(self)
                        device_operate = raw_input("device operate = ")
                        print (device_operate)
                        if re.search(r'lights|light' , device_operate) :
                            obj_controls.lights(response)
                        elif re.search(r'alarm' , device_operate):
                            obj_controls.alarms(response)
                        else :
                            print ("I cannot control %s " %device_operate)
                            engine.say("i cannot control %s " %device_operate)
                            engine.runAndWait()
                        
                        ## for another session
                        print ("do you want to operate other devices , yes or no") 
                        #engine.say("do you want to operate other devices , yes or no")
                        #engine.runAndWait()
                        #user_input = SmartApi.myCommand(self)
                        user_input =  raw_input("user_input = ")
                        if re.search(r'no' , user_input) or re.search(r'logout',  user_input):
                            print ("logging out of system")
                            engine.say("logging out of system")
                            engine.runAndWait()
                            response['api_key'] = "0"
                            print ("call commands function")
                            main()
                        else :
                            pass
        except requests.exceptions.Timeout as e:
            print ("Timeout ! Try Again")
            engine.say("timeout try again")
            engine.runAndWait()
            self.valid_func()
        except requests.exceptions.TooManyRedirects:
            print ("Too Many Requests")
            print ("Too Many Requests")
            engine.say("too Many requests")
            engine.runAndWait()
            self.valid_func()
        except requests.exceptions.RequestException as e:
            print ("lost connectivity")
            engine.say("lost connectivity")
            engine.runAndWait()
            self.valid_func




## might work on controlling the objects of SmartApi_version2 from here 
## other modules of facial recognition and sentiment analysis will also be controlled from here only 

def main():
	#obj_controls = SmartApi_with_alarm.controls()
	#obj_controls.alarms()
    print ("1.to control devices please login ! , say home automation login \nto exit the console say exit")
   	#engine.say("to control devices please login ! for login , say home automation login to exit the console say exit")
    #engine.runAndWait()

    #>>>> extract_command = SmartApi.myCommand(self)
    extract_command = raw_input("extract_command = ")

    ## run facial recognition module here 
    ## tells whether a person is stranger or authorized
    ##name = recognition.face()
    ##if name == 'Stranger':
    	#print ("you are unauthorized person")
    	#engine.say("you are unauthorized person")
    	#engine.runAndWait()
    	#sys.exit()

    ## this loop works fine and returns only expected value
    if re.search(r"home automation" , extract_command) and re.search(r"login" , extract_command) :
        ## once login and password are it should be in infinte loop 
        ## only 3 attempts are allowed for mail_id input
        for i in [0,1,2]:
            ## in general program we will match through usernames not mail ids stored data in database
            print ("Your mail id please !")
            #engine.say('Your mail id please !')
            #engine.runAndWait()
            #mail_id = SmartApi.myCommand(self)
            mail_id = raw_input("mail_id = ")
            ## taking the password for only 1 id , can be upgraded afterwards , for multiple users
            if mail_id == "chetna agarwal":
                ## taking password for the ids but only 3 attempts are allowed  
                flag = 3
                #engine.say("enter your password")
                #engine.runAndWait()
                password = raw_input("Enter your password = ")                  
                while (mail_id == "chetna agarwal"):
                    ## if password is correct then ask for device operations (3 attempts)
                    if password == "chetna":
                        ## it can be reomved only if we call lights or alarm function after it  , user_log for login confirmation
                        ## confirming the log in by voice output
                        state = "You are logged in " + mail_id
                        print (state)
                        ##engine.say(state)
                        ##engine.runAndWait()
                        obj_SmartApi.valid_func(password)
                        ##("http://codeglobal.in/home_automation1/android_login.php?tag=login&user=chetna.agarwal@codeglobal.in&pass="+password)
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
    elif re.search(r'exit' , extract_command):
        print ("Exiting the console")
        engine.say("exiting the console")
        engine.runAndWait()
        sys.exit()
    else :
        print ("Unexpected command given by user ")
        engine.say("unexpected command given by user")
        engine.runAndWait()  
        main()   
        #self.commands()  


if __name__ == "__main__":

	## intialising the engine module for text to speech
	engine=pyttsx.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id)
	engine.setProperty('rate', 150)
	
	## calling the objects of SmartApi_version2 module
	obj_controls = try2.controls()
	obj_SmartApi_try = SmartApi_try()
	main()
