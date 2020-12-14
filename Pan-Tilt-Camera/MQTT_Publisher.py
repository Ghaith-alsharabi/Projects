import paho.mqtt.publish as publish
 
#MQTT_SERVER = "192.168.1.5"
#MQTT_PATH = "test_channel"
 
publish.single("CoreElectronics/test","Hello", hostname="test.mosquitto.org")

publish.single("CoreElectronics/topic","world!", hostname="test.mosquitto.org")
print("Done")