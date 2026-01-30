import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-7cb26-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendance-7cb26.appspot.com"
})

# bucket = storage.bucket()
# imgstudent = []

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importing the mode images into a list
folderModepath = 'Resources/Modes'
modePathList = os.listdir(folderModepath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModepath, path)))

# load the encoding file
print("Loading Encode File....")
with open("EncodeFile.p", 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)
    encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(imgS)

    if face_locations:
        faceCurFrame = face_locations[0]
        encodeCurFrame = face_recognition.face_encodings(imgS, [faceCurFrame])

        imgBackground[162:162 + 480, 55:55 + 640] = img
        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

        for encodeFace, facLoc in zip(encodeCurFrame, [faceCurFrame]):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print("matches", matches)
            # print("faceDis", faceDis)
            matchIndex = np.argmin(faceDis)
            # print("matchIndex", matchIndex)
            if matches[matchIndex]:
                #print(studentIds[matchIndex])
                y1 , x2 , y2 , x1 = facLoc
                y1 , x2 , y2 , x1 =y1*4 , x2*4 , y2*4 , x1*4
                bbox = 55+x1 , 162+y1 , x2-x1 , y2-y1 
                imgBackground = cvzone.cornerRect(imgBackground,bbox,rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    cvzone.putTextRect(imgBackground,"Loding",(275,400))
                    cv2.imshow("Face Attendance", imgBackground)
                    counter =1
                    modeType = 1
    if counter != 0:

        if counter == 1:
            # Get the Data
            studentsInfo = db.reference(f'Students/{id}').get()
            print(studentsInfo)
            # # Get the Image from the Storage
            # blob = bucket.get_blob(f'Images/{id}.png')
            # array = np.frombuffer(blob.download_as_string(), np.uint8)
            # imgstudent = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)

        cv2.putText(imgBackground,str(studentsInfo['total_attendance']),(861,125),
                    cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
        cv2.putText(imgBackground,str(studentsInfo['branch']),(980,550),
                    cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)
        cv2.putText(imgBackground,str(id),(960,493),
                    cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)
        cv2.putText(imgBackground,str(studentsInfo['standing']),(910,625),
                    cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)
        cv2.putText(imgBackground,str(studentsInfo['year']),(1025,625),
                    cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)
        cv2.putText(imgBackground,str(studentsInfo['starting_year']),(1125,625),
                    cv2.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)
        
        (w, h) ,_ = cv2.getTextSize(studentsInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
        offset = (414 - w) // 2
        cv2.putText(imgBackground,str(studentsInfo['name']),(808+offset,445),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),1)
        # imgBackground[175:175+216,909:909+216]
        counter+=1
    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
