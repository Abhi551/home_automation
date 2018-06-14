#########################################################################
####         Title:   Data Collection for Facial Recognition         ####
####         Author:  Vinit                                          ####
####         Date:    22nd May 2018                                  ####
#########################################################################

import os 
import cv2
import numpy as np
from functions import *

def collect():
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalcatface.xml')


	head=0
	cap=cv2.VideoCapture(0)

	while head < 1:
		ret,img=cap.read()
		gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		#for showing how the camera is capturing the picture
		cv2.imshow("Current frame",gray)
		cv2.waitKey(30) 
		raw_input("Press Enter to continue:")
		
		#Brightness control
		if np.average(gray)> 90:
		      faces=face_cascade.detectMultiScale(gray,1.2,5) 
	              for (x,y,w,h) in faces:
	                FaceImage = gray[y - int(h / 2): y + int(h * 1.5), x - int(x / 2): x + int(w * 1.5)]
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			frame=gray[y:y+h, x:x+w]
			#Adding name in the list
			ID=AddName()
		        cv2.imwrite("Pics/User."+ str(ID)+ "." + str(head) + ".jpg",frame)
		        print("Data Collection is successful!")
	                print("Thank you for the Pic!!!")
		        cv2.waitKey(30)
		        cv2.imshow("Captured Pic",frame)
		        head=head+1

		      cv2.imshow("image",img)
		      if cv2.waitKey(0) == ord('q'):
	                break

	cap.release()
	cv2.destroyAllWindows()
