# -*- coding: utf-8 -*-
"""faceRecognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mJdfjWVrwHdzPcAR2n9XlLnNAlkwrdIn
"""

!wget https://www.dropbox.com/s/dgjhhjeisle9w60/jackelonfaces.zip?dl=0 -O jackelonfaces.zip

!unzip -q -o /content/jackelonfaces.zip

import numpy as np
import os
import cv2
from joblib import dump,load
from sklearn.svm import SVC
from imutils import paths

imagePaths = list(paths.list_images("jackelonfaces"))
print(imagePaths)
data = []
label = []

for imagePath in imagePaths:
  print(imagePath.split(os.path.sep))

imagePaths = list(paths.list_images("jackelonfaces"))
data = []
labels = []
#print(imagePaths)

for imagePath in imagePaths:
	label = imagePath.split(os.path.sep)[-2]
	#print(label)
	if label == "elonmusk":
		label = 0
	else :
		label = 1
	image = cv2.imread(imagePath)
	resized = cv2.resize(image,(64,64),interpolation=cv2.INTER_LINEAR)
	gray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
	data.append(np.ravel(gray))
	labels.append(label)

	
labels = np.array(labels)
clf = SVC(kernel='linear',probability=True)
clf.fit(data,labels)
dump(clf,"jackelonsvmclassifier.lib")
print("Train Sucess")

from google.colab.patches import cv2_imshow

faceCascades = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
svmClassifier = load("jackelonsvmclassifier.lib")

def face_detect(img,clf):
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  faces = faceCascades.detectMultiScale(gray,1.2,15)
  text = "None"
  for (x,y,w,h) in faces:
    faceset = []
    face = gray[y:y+h,x:x+w]
    face_resized = cv2.resize(face,(64,64),interpolation=cv2.INTER_LINEAR)
    faceset.append(np.ravel(face_resized))
    pred = clf.predict(faceset)
    prob = clf.predict_proba(faceset)
    print(pred,prob)
    if pred == [0]:
      text = "Elon Musk"
    elif pred == [1]:
      text = "Jack Ma"
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.putText(img,text,(x,y-4),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,255),2)
  return img

image = cv2.imread("jackelon.jpg")
image = face_detect(image,svmClassifier)

cv2_imshow(image)