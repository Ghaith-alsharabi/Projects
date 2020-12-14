import paho.mqtt.client as mqtt
import time
from Calculations import Calculations
import RPi.GPIO as GPIO

c = Calculations()

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
except Exception as e:
    print("Er ging iets fout bij GPIO SETUP")
    print(e)

# MQTT_SERVER = "m24.cloudmqtt.com"
MQTT_SERVER = "ghaithpi"
# MQTT_PATH = "test_channel"
PORT = 8883


# user = "kcxqqglz"
# password = "sDPJ7cBDyool"
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


def on_connect(client, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("CoreElectronics/test")


def on_message(msg):
    global y, x1
    msgstr = msg.payload
    msgList = msgstr.split()
    print(msgList)
    x1 = int(msgList[0])
    print("x1: ", x1)
    y = int(msgList[1])
    print("y: ", y)
    x2 = int(msgList[2])
    print("x2: ", x2)

    offset_pan = c.line_left(x1=x1)
    offset_tilt = c.line_top(y1=y)
    turn_pan(steps=abs(offset_pan), direction=c.step_direction(n=offset_pan))
    turn_tilt(steps=abs(offset_tilt), direction=c.step_direction(n=offset_tilt))



client = mqtt.Client()
# client.username_pw_set(user, password=password)
print("setting  password")
client.username_pw_set(username="ghaith", password="ghaith099")
client.tls_set("/etc/mosquitto/certs/ca.crt")
# client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, PORT)
try:
    client.loop_start()
except KeyboardInterrupt:
    GPIO.cleanup()
    client.loop_stop()
