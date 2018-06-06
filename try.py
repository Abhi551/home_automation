## to conver fetch time readable format , 
import datetime 
import requests 


try:
    r = requests.get(fetch_url)
    alarm_status = r.text.encode("UTF8")
    print (alarm_status)
    x = datetime.datetime.fromtimestamp(float(alarm_status/1000)).strftime('%Y-%m-%d %H:%M:%S')
    print (x)
    print x.split(" ")
    alarm_status=list(ast.literal_eval(alarm_status))
    for status in alarm_status[1:]:
        result_status = "your alarm is on " + status['Day'] +  " at " + status['Time']
        print (result_status)
except requests.exceptions.Timeout:
    print ("Timeout ! Try Again")
    #engine.say("timeout try again")
    #engine.runAndWait()
    self.alarms()
except requests.exceptions.TooManyRedirects:
    print ("Too Many Requests")
    #engine.say("too Many requests")
    #engine.runAndWait()
    #self.alarms()
except requests.exceptions.RequestException as e:
    print ("lost connectivity")
    #engine.say("lost connectivity")
    #engine.runAndWait()
    #self.alarms()