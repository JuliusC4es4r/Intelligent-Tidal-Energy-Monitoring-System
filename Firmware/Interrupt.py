from machine import Pin
from machine import Timer

interruptFlag = 0
pulseCount = 0
flowRate = 0
calibrationFactor = 4.5

pin = Pin(2,Pin.IN,Pin.PULL_DOWN)
timer = Timer(period = 1000, mode=Timer.PERIODIC, callback = lambda t:calculateFlow())

def callback(pin):
    global interruptFlag
    interruptFlag=1

def calculateFlow():
    global pulseCount
    print("calculating flow...")
    flowRate = pulseCount / (calibrationFactor)
    print("Flow Rate:" + str(flowRate) + " L/min")
    pulseCount = 0
    
pin.irq(trigger=Pin.IRQ_FALLING, handler=callback)
while True:
    if interruptFlag is 1:
        pulseCount = pulseCount + 1;
        interruptFlag=0