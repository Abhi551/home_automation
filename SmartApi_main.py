import pyttsx
import speech_recognition as sr
import os
import nltk
import re
import requests
import ast 
import time 
import sys

#from statistics import mode
#import recognition
#import face_recognition
#import SmartApi_with_alarm2
import SmartApi_version3

## import other modules also
class SmartApi():
    ## takes the command from user through Microphone
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
    def valid_func(self ):
        ## run function from SmartApi_with_alarm2/SmartApi_version3 file
        r , requests_out = obj_SmartApi_try.valid_url("http://codeglobal.in/home_automation1/android_login.php?tag=login&user=chetna.agarwal@codeglobal.in&pass=chetna") 
        ## only if 200 recieved
        if int(re.findall(r'[0-9]+', str(requests_out.json))[0]) == 200:
            print ("OK")
            while 1:
                response = ast.literal_eval(requests_out.text)
                user_input = 'yes'
                while (re.search(r'yes', str(user_input))):
                    ## which device to operate by user  
                    print ("what do you want to control \n1. alarm  \n2. lights")
                    engine.say("choose one of them what do you want to control alarm or lights")
                    engine.runAndWait()                                             
                    device_operate = SmartApi.myCommand(self)
                    #device_operate = raw_input("device operate = ")
                    #print (device_operate)
                    if re.search('lights|light' , str(device_operate)) :
                        obj_controls.lights(response)
                    elif re.search('alarm|reminder' , str(device_operate)):
                        obj_controls.alarms(response)
                    else :
                        print ("I cannot control %s " %device_operate)
                        engine.say("i cannot control %s " %device_operate)
                        engine.runAndWait()
                    
                    ## for another session
                    print ("do you want to operate other devices , yes or no") 
                    engine.say("do you want to operate other devices , yes or no")
                    engine.runAndWait()
                    user_input = SmartApi.myCommand(self)
                    #user_input =  raw_input("user_input = ")
                    if re.search(r'no' , str(user_input)) or re.search(r'log.?out',  str(user_input)):
                        print ("logging out of system")
                        engine.say("logging out of system")
                        engine.runAndWait()
                        response['api_key'] = "0"
                        sys.exit()
                    else :
                        pass

## might work on controlling the objects of SmartApi_version2 from here 
## other modules of facial recognition and sentiment analysis will also be controlled from here only 

def main():

    ## run facial recognition module here 
    ## tells whether a person is stranger or authorized
    #name = recognition.face()
    name = ""
    if name == 'Stranger':
        print ("you are unauthorized person")
        engine.say("you are unauthorized person")
        engine.runAndWait()
        sys.exit()
    else :
        print ("You are logged in ")
        engine.say("Welcome ")
        engine.runAndWait()
        obj_SmartApi.valid_func()

if __name__ == "__main__":

    ## intialising the engine module for text to speech
    engine=pyttsx.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 150)
    
    ## making the objects from the current module of SmartApi 
    obj_SmartApi = SmartApi()
    ## making the objects of SmartApi_version2 module
    obj_controls = SmartApi_version3.controls()
    obj_SmartApi_try = SmartApi_version3.SmartApi_try()
    main()
