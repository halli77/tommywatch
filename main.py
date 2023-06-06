# main.py 
# secrets are defined in boot.py

# https://github.com/Carlo47/NtpTime
# https://github.com/TomWis97/NTPClock

from time import sleep, time, mktime, localtime
from machine import Pin
from neopixel import NeoPixel
import network
import json
from umqttsimple import MQTTClient


pin = Pin(4, Pin.OUT)  
np = NeoPixel(pin, 12)   


def np_clear():
    for i in range(0, np.n):
        np[i] = (0, 0, 0)
    np.write()
    
def np_ok():
    pattern = [(0, 0, 254), (0, 0, 0), (0, 0, 254), (0, 0, 0)]
    
    for p in pattern:
        for i in range(0, np.n):
            np[i] = p
        np.write()
        sleep(0.5)

def np_spinner():
    for i in range(0, np.n):
        np[i] = (254, 254, 254)
        if i == 0:
            np[np.n-1] = (0, 0, 0)
        else:
            np[i-1] = (0, 0, 0)
        np.write()
        sleep(0.2)

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        np_clear()
        wlan.connect(SSID, PSK)
        while not wlan.isconnected():
            np_spinner()    
    print('network config:', wlan.ifconfig())
    np_ok()


def mqtt_msg_received(topic, message):
    print("---- new mqtt meassage ----")
    print(topic)
    print(message) 
    msg = json.loads(message)
    print(msg)
    
    if msg["debug"] == 1:
        demo(msg["time"], msg["start"], msg["stop"])
    else:
        draw_watch(msg["time"], msg["start"], msg["stop"])

    
def connect_and_subscribe():
    global MQTT_CLIENT_ID, MQTT_TOPIC_SUB, MQTT_SERVER, MQTT_USER, MQTT_PASSWORD
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_SERVER, user=MQTT_USER, password=MQTT_PASSWORD)
    client.set_callback(mqtt_msg_received)
    client.connect()
    client.subscribe(MQTT_TOPIC_SUB)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (MQTT_SERVER, MQTT_TOPIC_SUB))
    return client




def h2pixel(h):
    return h-12 if h >=12 else h



def draw_watch(h, start, stop):
    
    color_pointer = (0x00, 0xAA, 0x00)
    color_night = (5, 0, 0)

    # all LED off
    np_clear()
 
    # draw night
    night = []
    for i in range(start, 24):
        night.append(i)
    for i in range(0, stop+1):
        night.append(i)  
        
         # draw pointer
    np[h2pixel(h)] = color_night if h in night else color_pointer    
        
        
    while h in night:
        night.pop(0)
    
    print(night)
    
    if h >= start or h <= stop:   
        for i in night:
            np[h2pixel(i)] = color_night    


   
    
    
    np.write()
    

def demo(time, start, stop):
    print("Start Demo (16-14 Uhr, night=19,6)")
    for h in range(start, 24):
        print (h)
        draw_watch(h, start, stop)
        sleep(0.8)
    for h in range(0, 14):
        print (h) 
        draw_watch(h, start, stop)
        sleep(0.8)
    print("End Demo")



############

# demo(12, 19, 6)

do_connect()
mqtt = connect_and_subscribe()

while True:
    mqtt.check_msg() 
    sleep(60)
