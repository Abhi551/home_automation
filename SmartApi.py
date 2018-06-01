## for single devices only
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


from gtts import gTTS
#from weather import Weather

engine=pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

check_start = 1
## working properly , 
## for speech to speech interaction
class SmartApi():
    def __init__(self):
        self.fixed_url = "http://codeglobal.in/home_automation1/update.php?"


    ## takes the command from user through Microphone
    def myCommand(self):
        "Takes the command from user through voice"
        ## function to be executed till internet connectivity is available again
        #engine.say('I am ready for your command sir')
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
                return (str(command))
        except Exception as e:
            print ("Unknown Issues executed")
            print (e)
            self.myCommand()
            

## this should be in different class , a child class of SmartApi

class controls(SmartApi):

    ## to access alarms and remainder 
    def alarms (self):
        pass

    ## lights function for accessing the lights 
    def lights(self):

        fixed_url = "http://codeglobal.in/home_automation1/update.php?"


        ## which device to operate by user                
        print ("which light you want to turn on or off ,say device 2 on or device 2 off , if you want to logout say logout" )
        engine.say("which light you want to turn on or off , if you want to logout say log out")
        engine.runAndWait()

        ## working on device 2 only
        ## checking the device input by user 
        device_operate = SmartApi.myCommand(self)
        print (str(device_operate))
            
        ## upgrade for all other devices 

        if re.search("device 2|device to" , str(device_operate)) and re.search("on" , str(device_operate)):
            url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status2"+"="+"on"
            print (url_parsed)
            requests.get(url_parsed)
        elif re.search("device 2|device to" , str(device_operate)) and re.search("off" , str(device_operate)):
            url_parsed =  fixed_url+"api_key="+self.response["api_key"]+"&"+"status2"+"="+"off"
            requests.get(url_parsed)
            print (url_parsed)
        elif re.search(r"log[.]out" , str(device_operate)):
            response["api_key"] = None
            print ("Exiting the Smart Api")
            engine.say("Exiting the Smart Api")
            engine.runAndWait()
            sys.exit()
        elif re.search('enter',str(device_operate)) and re.search('console',str(device_operate)):
            return 1
        else :
            self.lights()
            engine.say("no such device registered")
            engine.runAndWait()
            print ("no such device registered")



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
                                    self.response = ast.literal_eval(requests_out.text)
                                    user_input = 'yes'
                                    while (re.search(user_input , 'yes')):
                                        ## which device to operate by user   
                                        print ("currently working for lights only") 
                                        print ("what do you want to control \n1. alarm  \n2.lights")
                                        engine.say("choose one of them what do you want to control alarm or lights")
                                        engine.runAndWait()                                             
                                        self.device_operate = SmartApi.myCommand(self)

                                        if re.search(r'lights|light' , self.device_operate):
                                            ## call lights
                                            self.lights()
                                        elif re.search(r'alarm' , self.device_operate):
                                            engine.say("Module is incomplete")
                                            engine.runAndWait()
                                            ## call alarm function here 
                                            ("Module is incomplete") 
                                        else :
                                            print ("I cannot control %s " %self.device_operate)
                                            engine.say("I cannot control %s " %self.device_operate)
                                            engine.runAndWait()
                                        
                                        ## for another session
                                        print ("do you want to continue , yes or no") 
                                        engine.say("do you want to continue , yes or no")
                                        engine.runAndWait()
                                        user_input = SmartApi.myCommand(self)
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
            self.commands()        

## for simple commands using speech
class assistant(SmartApi):

    def reddit(self):
        command = SmartApi.command(self)
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
        command =SmartApi.command(self)
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
        command = SmartApi.command(self)
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
    '''
    def search(self):
        command = SmartApi.command(self)
        elif 'who is' in command:
            command = command.split()
            name = command[2]
            print("Hold on satyam, I will tell you who " + name + " is.")
            sam= wikipedia.summary(name, sentences=3)
            engine.say(sam)
            engine.runAndWait()
    '''

## creating the object 
obj_SmartApi = SmartApi()      
#x = obj_SmartApi.myCommand()
#print (type(x))

obj_controls = controls()
obj_controls.commands()
