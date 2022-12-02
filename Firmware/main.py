import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import network
import micropython
import gc
from machine import UART, Pin, Timer, reset
from time import sleep_us


#networking
SSID = 'lochwood mesh'
PASSWORD = '123456789c'
SERVER = '192.168.0.112'
ID = ubinascii.hexlify(machine.unique_id())
TOPIC = 'ITEMS/DATA'

last_message = 0
message_interval = 5

interruptFlag = 0
pulseCount = 0
flowRate = 0
calibrationFactor = 4.5

pin = Pin(2,Pin.IN,Pin.PULL_DOWN)
timer = Timer(period = 1000, mode=Timer.PERIODIC, callback = lambda t:calculateFlow())
pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)

class myUART(UART):
    def readUntil(self, termination, maxlen=-1, includeTermination=True):
        result = ''
        while maxlen < 0 or len(result) < maxlen:
            if self.any():
                print("here")
                result += chr(self.read(1)[0])
                print(result)
                if result.endswith(termination):
                    if not includeTermination:
                        result = result[:-len(termination)]
                    break
            sleep_us(10)
        return result

def connect():
  client = MQTTClient(ID, SERVER)
  client.connect()
  print('Connected to %s MQTT broker', (TOPIC))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def callback(pin):
    global interruptFlag
    interruptFlag=1

def calculateFlow():
    global pulseCount
    print("calculating flow...")
    flowRate = pulseCount / (calibrationFactor)
    print("Flow Rate:" + str(flowRate) + " L/min")
    pulseCount = 0

def main():
    
    uart = myUART(0, baudrate=9600, tx=Pin(0), rx=Pin(1), bits=8, parity=None, stop=1)
    
    #networking
    gc.collect()

    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(SSID, PASSWORD)
    
    while station.isconnected() == False:
      pass
    
    print('Connection successful')
    print(station.ifconfig())
    
    try:
      client = connect()
    except OSError as e:
      restart_and_reconnect()
      

    while True:
        
        try:
            client.check_msg()
            if (time.time() - last_message) > message_interval:
                msg = 'Carter sucks :P'
                client.publish(TOPIC, msg)
                last_message = time.time()
        except OSError as e:
            restart_and_reconnect()
        
        if interruptFlag is 1:
            pulseCount = pulseCount + 1;
            interruptFlag=0
    
    
    
main()

