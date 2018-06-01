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

def main():
	print ("working")

	## for engine to convert every possible text into speech
	engine=pyttsx.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id)
	engine.setProperty('rate', 150)
	

if __name__ == "__main__":
	main()