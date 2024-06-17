import numpy as np
import cv2 as cv
from datetime import datetime
import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

# CREATE TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY,
    name TEXT,
    status TEXT,
    date NUMERIC
)
''')
conn.commit()

haar_cascade = cv.CascadeClassifier('haar_face.xml')

people =['Leonardo','Christine']

ispresent = []
for person in people:
    ispresent[{person: "NO"}]
    

face_recognizer = cv.face.LBPHFaceRecognizer_create()
face_recognizer.read('face_trained.yml')

cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 9)

    for (x, y, w, h) in faces_rect:
        faces_roi = gray[y:y+h, x:x+w]

        label, confidence = face_recognizer.predict(faces_roi)

        cv.putText(frame, str(people[label]), (x, y-10), cv.FONT_HERSHEY_COMPLEX, 1.0, (0, 255, 0), thickness=2)
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if ispresent[people[label]] == "NO":
            #INSERT DATA
            cursor.execute('''
                INSERT INTO attendance (name, status, date)
                VALUES (?, ?, ?)
            ''', (people[label], "Present", timestamp))
            conn.commit()
        print(f"{timestamp} - {people[label]}: Is present")
        ispresent[people[label]] == "YES"

    frame = cv.resize(frame, (min(frame.shape[1], 800), min(frame.shape[0], 600)))

    cv.imshow("Face Detection", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
conn.close()
cv.destroyAllWindows()
