import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import gc
gc.collect()

ssid = 'Loin-Net_2.4G'
password = 'Archon98furion2003'
mqtt_server = '192.168.0.112'
#EXAMPLE IP ADDRESS
#mqtt_server = '192.168.1.144'
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'notification'
topic_pub = 'test/test/test'

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())