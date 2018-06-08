import cv2
import face_recognition
import glob
import os
import natsort
import time 
from statistics import mode

def face():
	known_face_encoding , name_list = [] , []
	path = "/home/vinit/Desktop/ML/Self notes/Computer Vision/facial_rec/Pics"
	cap = cv2.VideoCapture(0)

	#Returns list of faces from the captured images
	img_file = os.listdir(path)
	#sorting the image label according to their numerical value written 
	img_file = natsort.natsorted(img_file)  

	for img in img_file:
	        #loads an image(.jpg,.png etc) into numpy array
	        image = face_recognition.load_image_file(path + '/' + img)
	        #128 measurements will be stored in encodings taking 68 landmarks on face for each person
	        encoding = face_recognition.face_encodings(image , num_jitters = 1)[0]
	        #num_jitters:How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower)
	        # i.e. 50 = 50 x slower
	        known_face_encoding.append(encoding)
	                                   
	#Returns list of known face names from the text file
	a = open("/home/vinit/Desktop/ML/Self notes/Computer Vision/facial_rec/Names.txt","r").read()
	known_face_names = a.split()

	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True	

	## while loop only work for 10 secs
	start_time = time.time()
	while (time.time() - start_time) < 10:
		ret,frame = cap.read()
		small_frame = cv2.resize(frame , (0 , 0) , fx = 0.25, fy = 0.25)
		#converting BGR to RGB format as dlib supports RGB
		rgb=small_frame[:,:,::-1]  

		if process_this_frame:
		        #Returns an array of bounding boxes of human faces in a image.
			face_locations = face_recognition.face_locations(rgb , model = "hog")
			#Given an image, return the 128-dimension face encoding for the face
			face_encodings = face_recognition.face_encodings(rgb,face_locations)
			face_names = []

			for face_encoding in face_encodings:
				matches=face_recognition.compare_faces(known_face_encoding,face_encoding,tolerance=0.5)
				#lower the tolerance more strict the comparisons i.e. error reduces
		
				name="Stranger"
				if True in matches:
					first_match_index = matches.index(True)
					name = known_face_names[first_match_index]

				face_names.append(name)
		process_this_frame = not process_this_frame
		for (top, right, bottom, left), name in zip(face_locations, face_names):
			top=top*4
			right=right*4
	    	right *= 4
	    	bottom *= 4
	    	left *= 4

		    # Drawing rectangular box aroung the face
	        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
	        # Draw a label with a name below the face
	        cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (255, 0, 0), cv2.FILLED)
	        font = cv2.FONT_HERSHEY_DUPLEX
	        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
	        name_list.append(name)
		    # Display the resulting image
		cv2.imshow('Video', frame)

		    # Hit 'q' on the keyboard to quit!
		if cv2.waitKey(1) & 0xFF == ord('q'):
		    break
	# Release webcam
	cap.release()
	cv2.destroyAllWindows()
	return (mode(name_list))
