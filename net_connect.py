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

from requests.adapters import HTTPAdapter 
from gtts import gTTS

engine=pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.say("hello")
engine.runAndWait()



def myCommand():
    "Takes the command from user through voice"
    ## function to be executed till internet connectivity is available again
    engine.say('I am ready for your command sir')
    engine.runAndWait()
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
        #loop back to continue to listen for commands if unrecognizable speech is received
            except sr.UnknownValueError:
                print("We couldn't understand your last command \Try Again!")
                engine.say("We couldn't understand your last command \Try Again!")
                engine.runAndWait()
            ## recursion if no input is provided by the user 
                command = myCommand();
            except sr.RequestError as e:
                print ("Could not request your results due to lost connectivity")
                engine.say("Could not request your results due to lost connectivity")
                engine.runAndWait()
                myCommand()
            except Exception as e :
                print ("Unknown Issues")
    except Exception as e:
        print ("Unknown Issues executed")
        print (e)

myCommand()
