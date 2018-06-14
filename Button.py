from Tkinter import *
#import recognition
#import DataCollection
import SmartApi_main
#from SmartApi_main import *

def open():
	SmartApi_main.main()


Gui=Tk(className="  Face Recognition")
Gui.geometry('615x400')

#pic=PhotoImage(file="background.png")
#label=Label(Gui, image=pic).pack()


button=Button(text="Press", command=open ,fg='red').pack()
#button2=Button(text="Add New Face", command=open2, fg='blue').pack()

Gui.mainloop()
