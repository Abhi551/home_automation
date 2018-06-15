import speech_recognition as sr
import re
import ast
import json, requests 
import time 
import pandas as pd
import pyttsx
from gtts import gTTS
from time import sleep
engine=pyttsx.init()
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
        
'''
def myCommand():
    r = sr.Recognizer()

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
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command
'''

def assistant(command):
    if re.search('anaya|inaya|aanaya' , command) :
        if re.search('who' , str(command)) and re.search('are|r' , str(command)) and re.search('you|u' , str(command)):
            command = "who are you"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('old' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "how old are you"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)            
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('annoying|annoy' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "you are annoying"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)             
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('answer' , str(command)) and re.search('my|mi' , str(command)) and  re.search('question' ,str(command)):
            command = "answer my question"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('can' , str(command)) and re.search('get' , str(command)) and  re.search('you|u' ,str(command)):
            command = "can you get smarter"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('bad' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "you are bad"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)              
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('beautiful|beauty' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "you are beautiful"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('birth.?date|birth' , str(command)) and  re.search('your|ur' ,str(command)):
            command = "what is your birth date"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('bose|boss' , str(command)) and re.search('your|ur' ,str(command)):
            command = "who is your boss"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('boring' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "you are boring"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('busy' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "are you busy"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait() 
        elif re.search('help' , str(command)) and re.search('me' , str(command)) and  re.search('you|u' ,str(command)):
            command = "can you help me"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()             
        elif re.search('chat.?bot' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "you are a chatbot"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()        
        elif re.search('clever' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "you are so clever"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('crazy' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "you are crazy"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('do' , str(command)) and re.search('hobby' , str(command)) and  re.search('you|u' ,str(command)):
            command = "do you have a hobby"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('funny|fun.?' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "you are funny"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('good|gud' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "you are good"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('happy' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "are you happy"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('hungry' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "are you hungry"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('marry' , str(command))  and  re.search('you|u' ,str(command)):
            command = "will you marry me"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('friends' , str(command)) and re.search('are|r' , str(command)) and  re.search('we|v|wee' ,str(command)):
            command = "are we friends"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('where|were' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "where are you from"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('ready' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "are you ready"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('real|reel' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "are you real"
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()
        elif re.search('right' , str(command)) and re.search('are|r' , str(command)) and  re.search('you|u' ,str(command)):
            command = "you are right."
            url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command)
            time.sleep(2)
            while (url_text) == None :
                url_text = valid_url('http://codeglobal.in/home_automation1/fetchsmarttalkdetails.php?command='+command) 
            print (url_text['Answer'])
            #engine.say(result)
            #engine.runAndWait()

command =  raw_input("Enter the command = ")
assistant(command)
'''
df = pd.read_csv('a.csv',header = None ,)
for column in  df[0]:
    i = 1
    print ('anaya ' + str(column))
    assistant("anaya "+str(column))
    i=i+1
    if i==29:
        break
'''
