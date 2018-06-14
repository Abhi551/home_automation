""" 
Title: Function for Facial Recognition
Author: Vinit
"""

import cv2
import os

def AddName():
	Name=raw_input("Enter your Name:")
	info=open("Names.txt","r+")
	ID=((sum(1 for line in info))+1)
	info.write(Name+"\n")
	#print("Nmae Stored in"+str(ID))
	info.close()
	return ID
