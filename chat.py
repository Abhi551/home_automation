import speech_recognition as sr
import re
import ast
import json, requests 
import time 
# one of pyttsx or pytssx3 is used 
#import pyttsx3
import pyttsx
from gtts import gTTS
from time import sleep
engine = pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def valid_url(url):
    #print (url)
    try:
        url_try = url
        r = requests.get(url)
        return json.loads(r.text)
    except requests.exceptions.Timeout as e:
        print ("Timeout ! Try Again")
        engine.say("timeout try again")
        engine.runAndWait()
        time.sleep(5)
        valid_url(url)
    except requests.exceptions.TooManyRedirects:
        print ("Too Many Requests")
        engine.say("too Many requests")
        engine.runAndWait()
        time.sleep(5)
        valid_url(url)
    except requests.exceptions.RequestException as e:
        print ("lost connectivity")
        engine.say("lost connectivity")
        engine.runAndWait()
        time.sleep(5)
        valid_url(url)
    except RuntimeError as e:
        print ("Took too long to connect , Try Again!")
        engine.say("too Many requests")
        engine.runAndWait()            
        sys.exit()
    except Exception as e :
        print (e)
        engine.say("couldn't handle ")
        engine.runAndWait()
        valid_url(url)

def assistant(command):
        try :
            url = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            while url == None :
                url = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            print (url['Answer'])
            engine.say(url['Answer'])
            engine.runAndWait()
        except ValueError as e:
            print ('nothing to say')
            engine.say('nothing to say')
