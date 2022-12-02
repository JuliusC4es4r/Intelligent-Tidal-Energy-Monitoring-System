import paho.mqtt.client as mqtt
import time

def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8")))

broker_address = "192.168.0.112"
client = mqtt.Client("gs")
client.connect(broker_address)
client.subscribe("test/test/test")
client.on_message = on_message
client.loop_start()


while 1:
    time.sleep(1)