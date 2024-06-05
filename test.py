import sys
from Adafruit_IO import MQTTClient
import time
import random
from fsm import *
# from simple_ai import *
# from uart import *
# from rs485 import *
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
        schedules[0] = create_irrigation_schedule(format_data1.get('cycle'), format_data1.get('flow1'), format_data1.get('flow2'), format_data1.get('flow3'), format_data1.get('isActive') , format_data1.get('schedulerName'), format_data1.get('startTime'), format_data1.get('stopTime'))
        print_data(schedules[0])
    if feed_id =="sched2":
        schedules[1] = create_irrigation_schedule(format_data2.get('cycle'), format_data2.get('flow1'), format_data2.get('flow2'), format_data2.get('flow3'), format_data2.get('isActive') , format_data2.get('schedulerName'), format_data2.get('startTime'), format_data2.get('stopTime'))
        print_data(schedules[1])
    if feed_id =="sched3":
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
    # counter = counter - 1
    # if counter <= 0:
    #         counter = 10
            
    #         print("Random data is publishing...")
    #         if sensor_type == 0:
    #                 temp = random.randint(10, 20)
    #                 print("Temperature..." + str(temp))

    #                 client.publish("cambien1", temp)
    #                 sensor_type = 1
    #         elif sensor_type == 1:
    #                 humid = random.randint(0, 100)
    #                 print("Humidity... " + str(humid))
    #                 client.publish("cambien2", humid)
    #                 sensor_type = 2
    #         elif sensor_type == 2:
    #                 light = random.randint(0, 500)
    #                 print("Light..." + str(light))

    #                 client.publish("cambien3", light)
    #                 sensor_type = 0
    
    # counter_ai = counter_ai - 1
            
    # if counter_ai <=0:
    #     counter_ai = 5
    #     previous_result = ai_result
    #     ai_result = image_detector()
    #     print("AI Output: ",ai_result)
    #     if previous_result != ai_result:
    #         client.publish("AI", ai_result)
      
    # readSerial(client)
    fsm(schedules, client)
    time.sleep(1)
