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
    def search(self):
        command = SmartApi.command(self)
        elif 'who is' in command:
            command = command.split()
            name = command[2]
            print("Hold on satyam, I will tell you who " + name + " is.")
            sam= wikipedia.summary(name, sentences=3)
            engine.say(sam)
            engine.runAndWait()

obj = assistant()
