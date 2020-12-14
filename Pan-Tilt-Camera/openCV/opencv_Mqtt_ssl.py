import cv2
import logging as log
import datetime as dt
import paho.mqtt.client as paho
import time
import datetime
cap = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier(
    'C:/Users/Ghais/AppData/Local/Programs/Python/Python37-32/Lib/site-packages/cv2/data/haarcascade_frontalface_alt.xml')
log.basicConfig(filename='webcam.log', level=log.INFO)
check = None
secoundpass = None

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
    
    #calling the client method for the mqtt lib
    client1= paho.Client("controll1")
    #sending username and password to the borker 
    client1.username_pw_set(username="ghaith",password="ghaith099")
			
		#	secoundpass=True
		# lasttimesecound=curenttime
    # sending the certificate to the broker
    client1.tls_set("C:\Program Files (x86)\mosquitto\certs\ca.crt")
    #connect with the borker on port 8883 and hostname ghaithpi
    client1.connect("ghaithpi", 8883, 60)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        log.info("x= %d y= %d.", x, y)
        #	list=[x,y,x+w]
        #	publish.single("CoreElectronics/test",x, hostname="test.mosquitto.org192.168.137.236")
       # curtime = datetime.datetime.second.now()
        #curtime=('%02d:%02d.%d'%(now.minute,now.second,now.microsecond))[:-4]
        if x2 > x > x1 and y2 > y > y1 and x2 > x + w > x1 and y2 > y + h > y1:
            check = True
        else:
            check = False
            #list = [x, y, x + w]
            xw = x+w
            stri =str(x) + " "  + str(y) + " " +  str(xw) 
            #if(secoundpass==True):
            #publish message(stri) on the topic (test)
            client1.publish("CoreElectronics/test", stri)
             #  secoundpass=False
             #  print(curtime)
			   #curtime += 3
			
            #else: 
             #   if(curtime!=datetime.datetime.now()): 
               #    secoundpass=True 
			
			
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

			