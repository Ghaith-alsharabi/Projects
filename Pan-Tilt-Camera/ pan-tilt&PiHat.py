
import paho.mqtt.client as mqtt 
import time 
from adafruit_motorkit import MotorKit 
from adafruit_motor import stepper

#MQTT_SERVER = "m24.cloudmqtt.com"
MQTT_SERVER ="ghaithpi"
#MQTT_PATH = "test_channel"
PORT =8883
kit = MotorKit(address=0x6f)
myvar  =0

#qwer = 0

#user = "kcxqqglz"
#password = "sDPJ7cBDyool"
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("CoreElectronics/test")
#    client.subscribe("CoreElectronics/topic")
     
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe(MQTT_PATH)
 
# The callback for when a PUBLISH message is received from the server.


def on_message(client, userdata, msg): 
    msgstr = msg.payload
    msgList = msgstr.split()
    print(msgList)
    x =int(msgList[0])
    print("x: ",x)
    y = int(msgList[1])
    print("y: ",y)
#Filtering X
    if x > 200 and x<275:
       print("face in range X ")
#BACKWARD INTERLEAVE step
    elif x>275:
        for i in range(15):
             kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
#FORWARD INTERLEAVE step
    elif x < 200:
        for i in range(15):
             kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
#Filtering Y
    if y > 125 and y<175:
        print("face in range (Y) ")
#BACKWARD INTERLEAVE step
    elif y>175:
        for i in range(2):
             kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
#FORWARD INTERLEAVE step    
    elif y < 125:
        for i in range(2):
             kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)




client = mqtt.Client()

print("setting  password")
client.username_pw_set(username="ghaith",password="ghaith099")
client.tls_set("/etc/mosquitto/certs/ca.crt")
#client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, PORT)
client.loop_forever()

