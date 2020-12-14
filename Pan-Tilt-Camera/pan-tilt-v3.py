import paho.mqtt.client as mqtt
import time
from Calculations import Calculations
import RPi.GPIO as GPIO

c=Calculations()

try:
    STEPPIN_PAN = 20
    DIRPIN_PAN = 21
    STEPPIN_TILT = 14
    DIRPIN_TILT = 15
    M_PINS = (13, 19, 26)
    DELAYTILT = 0.0025
    DELAYPAN = 0.00025
    RESOLUTION = {'Full': (0, 0, 0),
                  'Half': (1, 0, 0),
                  '1/4': (0, 1, 0),
                  '1/8': (1, 1, 0),
                  '1/16': (0, 0, 1),
                  '1/32': (1, 0, 1)}

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(STEPPIN_PAN, GPIO.OUT)
    GPIO.setup(DIRPIN_PAN, GPIO.OUT)
    GPIO.setup(STEPPIN_TILT, GPIO.OUT)
    GPIO.setup(DIRPIN_TILT, GPIO.OUT)
    GPIO.setup(M_PINS, GPIO.OUT)
    GPIO.output(M_PINS, RESOLUTION['Half'])
except Exception:
    print("Er ging iets fout bij GPIO SETUP")

buffer = 50
anker_x = 480
anker_y = 640
x_max = anker_x + (buffer/2)
x_min = anker_x - (buffer/2)
y_max = anker_y + (buffer/2)
y_min = anker_y - (buffer/2)

#MQTT_SERVER = "m24.cloudmqtt.com"
MQTT_SERVER ="ghaithpi"
#MQTT_PATH = "test_channel"
PORT =8883

#user = "kcxqqglz"
#password = "sDPJ7cBDyool"
# The callback for when the client receives a CONNACK response from the server.

def turn_tilt(steps, direction):
    GPIO.output(DIRPIN_TILT, direction)
    print("Direction: ", direction)
    count = 0
    for i in range(steps):
        count += 1
        print(count)
        GPIO.output(STEPPIN_TILT, GPIO.HIGH)
        time.sleep(DELAYTILT)
        GPIO.output(STEPPIN_TILT, GPIO.LOW)
        time.sleep(DELAYTILT)
    print("steps: ", count)


def turn_pan(steps, direction):
    GPIO.output(DIRPIN_PAN, direction)
    print("Direction: ", direction)
    count = 0
    for i in range(steps):
        count += 1
        print(count)
        GPIO.output(STEPPIN_PAN, GPIO.HIGH)
        time.sleep(DELAYPAN)
        GPIO.output(STEPPIN_PAN, GPIO.LOW)
        time.sleep(DELAYPAN)
    print("steps: ", count)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("openCV")
    client.subscribe("ui")


def on_message(client, userdata, msg):
    gh = str(msg.payload)
    ghlist = gh.split("'")
    cleanV = ghlist[1]
    x = ghlist[2]
    y = ghlist[3]

    if msg.topic == "ui"  and cleanV == "start":
         client.unsubscribe("test")
         

         if x = 1
            turn_pan(steps=abs(15), direction=0)
         if x = -1
            turn_pan(steps=abs(15), direction=1)
         if y = 1
            turn_tilt(steps=abs(12), direction=1)
         if y = -1
            turn_tilt(steps=abs(12), direction=0)

    if msg.topic == "ui"  and cleanV == "exit":
         client.subscribe("test")
         

    
    if msg.topic == "openCV"  and cleanV == "opencv":
        if x > x_min and x<x_max:
           print("face in range X ")
        #BACKWARD INTERLEAVE step
        elif x>x_max:
            turn_pan(steps=abs(15), direction=0)
        #FORWARD INTERLEAVE step
        elif x < x_min:
            turn_pan(steps=abs(15), direction=1)
        #Filtering Y
        if y > y_min and y<y_max:
            print("face in range (Y) ")
        #BACKWARD INTERLEAVE step
        elif y>y_max:
            turn_tilt(steps=abs(12), direction=1)
        #FORWARD INTERLEAVE step    
        elif y < y_min:
            turn_tilt(steps=abs(12), direction=0)


client = mqtt.Client()
#client.username_pw_set(user, password=password)
print("setting  password")
client.username_pw_set(username="ghaith",password="ghaith099")
client.tls_set("/etc/mosquitto/certs/ca.crt")
#client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, PORT) 
client.loop_forever()

