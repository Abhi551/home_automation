import requests
import time
import sys

class SmartApi():
    ## takes the command from user through Microphone
    def valid_url(self,url):
        start_time = time.time()
        try:
            r = requests.get(url)
            return r
        except requests.exceptions.Timeout as e:
            print ("Timeout ! Try Again")
            #engine.say("timeout try again")
            #engine.runAndWait()
            time.sleep(10)
            self.valid_url(url)
        except requests.exceptions.TooManyRedirects:
            print ("Too Many Requests")
            print ("Too Many Requests")
            #engine.say("too Many requests")
            #engine.runAndWait()
            time.sleep(10)
            self.valid_url(url)
        except requests.exceptions.RequestException as e:
            print ("lost connectivity")
            #engine.say("lost connectivity")
            #engine.runAndWait()
            time.sleep(10)
            self.valid_url(url)
        except RuntimeError as e:
            print ("Took too long to connect , Try Again!")
            #engine.say("too Many requests")
            #engine.runAndWait()            
            sys.exit()

new_url="http://codeglobal.in/home_automation1/fetchalarmdetails.php?api_key=a1ebc37f43ee497ca453f84a9e9e7d11"
s = SmartApi()
s.valid_url(new_url)