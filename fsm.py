import time
from datetime import datetime, timedelta
from rs485 import *
import json
from Adafruit_IO import MQTTClient
from Adafruit_IO import Client, Feed, Data
ADAFRUIT_IO_USERNAME = 'kienpham'
ADAFRUIT_IO_KEY = 'aio_KyUO58IJ9uDMPOixYtTZkfcO69eX'


# Create an instance of the Adafruit IO client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Get data from a specific feed
feed_name1 = 'sched1'  # Replace with your feed name
data1 = aio.receive(feed_name1)
format_data1 = json.loads(data1.value)

feed_name2 = 'sched2'  # Replace with your feed name
data2 = aio.receive(feed_name2)
format_data2 = json.loads(data2.value)

feed_name3 = 'sched3'  # Replace with your feed name
data3 = aio.receive(feed_name3)
format_data3 = json.loads(data3.value)

# Print the data
print(format_data1)
print(format_data1.get('cycle'))

class IrrigationSchedule:
    def __init__(self, cycle, flow1, flow2, flow3, isActive, schedulerName, startTime, stopTime):
        self.cycle = cycle
        self.flow1 = flow1
        self.flow2 = flow2
        self.flow3 = flow3
        self.isActive = isActive
        self.schedulerName = schedulerName
        self.startTime = startTime
        self.stopTime = stopTime

def create_irrigation_schedule(cycle, flow1, flow2, flow3, isActive, schedulerName, startTime, stopTime):
    return IrrigationSchedule(cycle, flow1, flow2, flow3, isActive, schedulerName, startTime, stopTime)

# Create instances of the IrrigationSchedule class using the function
schedule1 = create_irrigation_schedule(format_data1.get('cycle'), format_data1.get('flow1'), format_data1.get('flow2'), format_data1.get('flow3'), format_data1.get('isActive'), format_data1.get('schedulerName'), format_data1.get('startTime'), format_data1.get('stopTime'))
# schedule1 = create_irrigation_schedule(3, 4, 5, 6, False, "Irrigation Schedule1", "22:02", "22:04")
schedule2 = create_irrigation_schedule(format_data2.get('cycle'), format_data2.get('flow1'), format_data2.get('flow2'), format_data2.get('flow3'), format_data2.get('isActive'), format_data2.get('schedulerName'), format_data2.get('startTime'), format_data2.get('stopTime'))
schedule3 = create_irrigation_schedule(format_data3.get('cycle'), format_data3.get('flow1'), format_data3.get('flow2'), format_data3.get('flow3'), format_data1.get('isActive'), format_data3.get('schedulerName'), format_data3.get('startTime'), format_data3.get('stopTime'))

# Print the details of each schedule to verify
print(vars(schedule1))
print(vars(schedule2))
print(vars(schedule3))

schedules = [schedule1, schedule2, schedule3]
# print(vars(schedules[0]))
# if schedules[1].startTime == (datetime.now()).strftime("%H:%M"):
#     print("ON TIME")
#print ((datetime.now() + timedelta(hours=6)).strftime("%H:%M"))
IDLE = 0
MIXER1 = 1
MIXER2 = 2
MIXER3 = 3
PUMP_IN = 4
SELECTOR = 5
PUMP_OUT = 6
NEXT_CYCLE = 7
END = 8
timeProcess = 0

schedule_id = 0
status = IDLE
cycle = 0
count = 0
count1 = 0
started = False

def fsm(schedules, client):
    global status, cycle, count,count1, schedule_id, started
    if count1 == 0:
       readSerial(client)
    if schedules[schedule_id].isActive == False:
        schedule_id = schedule_id + 1
        if schedule_id >= 3:
            schedule_id = 0
        status = IDLE
    
    if started == True and schedules[schedule_id].stopTime == (datetime.now()+ timedelta(hours=6)).strftime("%H:%M"):
        schedule_id = schedule_id + 1
        started = False
        if schedule_id >= 3:
            schedule_id = 0
        status = IDLE


    if status == IDLE:
        print("IDLE")
        if(schedules[schedule_id].startTime == (datetime.now()+ timedelta(hours=6)).strftime("%H:%M")):
          started = True
          status = MIXER1
          count = schedules[schedule_id].flow1
          print("CYCLE: " + str(cycle))
          print("MIXER1")
          print("TimeProcess: "+ str(count))

    elif status == MIXER1:
        if count <= 0:
            print("MIXER2")
            status = MIXER2
            count = schedules[schedule_id].flow2
        
        print("TimeProcess: "+ str(count))
    
    elif status == MIXER2:
        if count <= 0:
            print("MIXER3")
            status = MIXER3
            count = schedules[schedule_id].flow3

        print("TimeProcess: "+ str(count))
    
    elif status == MIXER3:
        if count <= 0:
            print("PUMP_IN")
            status = PUMP_IN
            count = 5

        print("TimeProcess: "+ str(count))
    
    elif status == PUMP_IN:
        if count <= 0:
            print("SELECTOR")
            status = SELECTOR
            print("Area selected: " + str(schedules[schedule_id].cycle % 3))
            count = 2

        print("TimeProcess: "+ str(count))
    elif status == SELECTOR:
        if count <= 0:
            print("PUMP_OUT")
            status = PUMP_OUT
            count = 5
        print("TimeProcess: "+ str(count))

    elif status == PUMP_OUT:
        if count <= 0:
            print("NEXT_CYCLE")
            status = NEXT_CYCLE
        
        if count > 0:
            print("TimeProcess: "+ str(count))
    
    elif status == NEXT_CYCLE:
        cycle += 1
        if cycle >= schedules[schedule_id].cycle:
            print("WAITING_NEXT_SCHEDULE")
            started = False
            schedule_id +=1
            if schedule_id >= 3:
               print("END")
               schedule_id = 0

            status = IDLE
            cycle = 0
        else:
            status = MIXER1
            count = schedules[schedule_id].flow1
            print("CYCLE: " + str(cycle))
            print("MIXER1")
            print("TimeProcess: "+ str(count))

        
    count -=1
    count1 +=1
    if count1 == 10:
        count1 = 0

# while True:
#     fsm(schedules)
#     time.sleep(1)
