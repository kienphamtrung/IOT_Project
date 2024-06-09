import sys
from Adafruit_IO import MQTTClient
import time
import random
from fsm import *
AIO_FEED_IDs = ["nutnhan1", "nutnhan2", "sched1", "sched2","sched3"]
AIO_USERNAME = "kienpham"
AIO_KEY = "aio_aSjg21TMvndcyD7i1X64FA46g8pa"

def connected(client):
    print("Ket noi thanh cong ...")
    for topic in AIO_FEED_IDs:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + " feed id: " + feed_id)
    if feed_id =="sched1":
        data1 = aio.receive(feed_name1)
        format_data1 = json.loads(data1.value)
        schedules[0] = create_irrigation_schedule(format_data1.get('cycle'), format_data1.get('flow1'), format_data1.get('flow2'), format_data1.get('flow3'), format_data1.get('isActive') , format_data1.get('schedulerName'), format_data1.get('startTime'), format_data1.get('stopTime'))
        print_data(schedules[0])
    if feed_id =="sched2":
        data2 = aio.receive(feed_name2)
        format_data2 = json.loads(data2.value)
        schedules[1] = create_irrigation_schedule(format_data2.get('cycle'), format_data2.get('flow1'), format_data2.get('flow2'), format_data2.get('flow3'), format_data2.get('isActive') , format_data2.get('schedulerName'), format_data2.get('startTime'), format_data2.get('stopTime'))
        print_data(schedules[1])
    if feed_id =="sched3":
        data3 = aio.receive(feed_name3)
        format_data3 = json.loads(data3.value)
        schedules[2] = create_irrigation_schedule(format_data3.get('cycle'), format_data3.get('flow1'), format_data3.get('flow2'), format_data3.get('flow3'), format_data3.get('isActive') , format_data3.get('schedulerName'), format_data3.get('startTime'), format_data3.get('stopTime'))
        print_data(schedules[2])
    if feed_id =="nutnhan1" and payload == '0':  
        schedules[0] =  create_irrigation_schedule(format_data1.get('cycle'), format_data1.get('flow1'), format_data1.get('flow2'), format_data1.get('flow3'), False , format_data1.get('schedulerName'), format_data1.get('startTime'), format_data1.get('stopTime'))
        print_data(schedules[0])
    if feed_id =="nutnhan1" and payload == '1':  
        schedules[0] =  create_irrigation_schedule(format_data1.get('cycle'), format_data1.get('flow1'), format_data1.get('flow2'), format_data1.get('flow3'), True , format_data1.get('schedulerName'), format_data1.get('startTime'), format_data1.get('stopTime'))  
        print_data(schedules[0])
 
    # if feed_id =="nutnhan2":
        # writeData(2, payload)


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter = 10
sensor_type = 0
counter_ai = 5
ai_result =""
previous_result =""
while True:
    fsm(schedules, client)
    time.sleep(1)
