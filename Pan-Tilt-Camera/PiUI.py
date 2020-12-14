import paho.mqtt.client as mqtt

MQTT_SERVER ="ghaithpi"
PORT =8883

def on_connect(client,userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("test")
#    if not gh:
    print(userdata)
    client.subscribe("ui")

def on_message(client,userdata, msg):
    gh = str(msg.payload)
    ghlist = gh.split("'")
    cleanV = ghlist[1]

    if msg.topic == "ui"  and cleanV == "start":
         client.unsubscribe("test")
         print(cleanV)
    if msg.topic == "ui"  and cleanV == "exit":
         client.subscribe("test")
         print(cleanV)
    print(cleanV)
client = mqtt.Client()
#client.username_pw_set(user, password=password)
print("setting password")
client.username_pw_set(username="ghaith",password="ghaith099")
client.tls_set("/etc/mosquitto/certs/ca.crt")
#client.tls_insecure_set(True)
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, PORT)
client.loop_forever()

