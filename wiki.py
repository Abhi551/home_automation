import wikipedia 
import re 
import pyttsx 

engine=pyttsx.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def search():
    #command = SmartApi.command(self)
    command =  raw_input ("command = ")
    if re.search('who is' , str(command)) or re.search("tell me about" , str(command)) :
        command = command.split()
        name = command[2]
        print("Hold on satyam, I will tell you who " + name + " is.")
        sam= wikipedia.summary(name, sentences=3)
        print sam
search()