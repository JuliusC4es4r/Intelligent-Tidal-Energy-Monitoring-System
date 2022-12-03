import paho.mqtt.client as mqtt
import time
from datetime import datetime
import sqlite3 as db

flow_data = {}
coords = {}
battery = {}

conn = db.connect('ITEMS.db')
cursor = conn.cursor()

table ="""CREATE TABLE DATA(TIMESTAMP VARCHAR(255),
            ID VARCHAR(255),
            LAT VARCHAR(255),
            ONG VARCHAR(255),
            FLOW VARCHAR(255),
            BATT VARCHAR(255));"""

cursor.execute(table)

def on_message(client, userdata, message):
    timestamp = datetime.now()
    msg = str(message.payload.decode("utf-8"))
    items_id = msg[0:3]
    coords[items_id] = (msg[3:10], msg[10:17])
    flow_data[items_id] = msg[17:20]
    battery[items_id] = msg[20:22]
    
    cursor.execute('INSERT INTO DATA VALUES ('+timestamp+', '+items_id+', '+coords[items_id][0]+', '+coords[items_id][1]+', '+flow_data[items_id]+', '+battery[items_id]+')')

def main():
    broker_address = "192.168.86.112"
    client = mqtt.Client("gs")
    client.connect(broker_address)
    client.subscribe("ITEMS/DATA")
    client.on_message = on_message
    client.loop_start()
    
    
    
    while 1:
        pass

main()