import cv2
import logging as log
import datetime as dt
import paho.mqtt.publish as publish
import time

cap = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier(
    'C:/Users/Ghais/AppData/Local/Programs/Python/Python37-32/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml')
log.basicConfig(filename='webcam.log', level=log.INFO)
check = None

x1 = 50
y1 = 90
x2 = 400
y2 = 400

list = [0] * 3

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    i = 0
    log.info("Found {0} faces!".format(len(faces)) + " at " + str(dt.datetime.now()))

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        log.info("x= %d y= %d.", x, y)
       
        if x2 > x > x1 and y2 > y > y1 and x2 > x + w > x1 and y2 > y + h > y1:
            check = True 
        #	list=[x,y,x+w]
        #	publish.single("CoreElectronics/test",x, hostname="test.mosquitto.org")
        else:
            check = False
            #list = [x, y, x + w]
            xw = x+w
            stri =str(x) + " "  + str(y) + " " +  str(xw) 
            publish.single("CoreElectronics/test", stri, hostname="192.168.137.45")
           # time.sleep(2)
        i = i + 1
        print('%d = %s' % (i, check))
    # time.sleep(3)

    cv2.imshow('frame', frame)
    # Display the resulting frame
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
