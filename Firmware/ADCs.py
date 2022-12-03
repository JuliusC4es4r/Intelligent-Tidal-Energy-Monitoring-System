from machine import Pin, ADC, Timer
import utime
timer_solar=Timer(-1) #virtual timer, the ID will be -1
timer_battery=Timer(-1) #virtual timer, the ID will be -1

timer_solar.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:print(solarPanelVoltage))
timer_battery.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:print(batteryVoltage))

batteryVoltage = 0
solarPanelVoltage = 0

solarPanelAnalogReading = 0 
batteryAnalogReading = 0

solarPanelAnalogPin = ADC(1) # Solar Panel Pin
batteryAnalogPin = ADC(2) # Battery Pin

voltageConversionFactor = 3.3 / (65535.0)
batteryConversionFactor = 33.0/43.0
solarPanelConversionFactor = 33.0/50.4

while 1:
    solarPanelAnalogReading = solarPanelAnalogPin.read_u16()
    utime.sleep(0.2)
    batteryAnalogReading = batteryAnalogPin.read_u16()
    utime.sleep(0.2)
    batteryVoltage = (batteryAnalogReading * voltageConversionFactor)
    solarPanelVoltage = (solarPanelAnalogReading * voltageConversionFactor)