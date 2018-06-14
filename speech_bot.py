import pyttsx
import speech_recognition as sr

engine=pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def myCommand():
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
                command = myCommand() ##if no input is provided by the user 
            except sr.RequestError as e:
                print ("Could not request your results due to lost connectivity")
                engine.say("could not request your results due to lost connectivity")
                engine.runAndWait()
                myCommand()
            except Exception as e :
                print ("Unknown Issues")
                myCommand()
    except Exception as e:
        print ("Unknown Issues executed")
        print (e)
        myCommand()
myCommand()
