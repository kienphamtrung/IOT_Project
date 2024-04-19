print("Sensors and Actuators")

import time
import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort
    # return "/dev/ttyUSB1"

portName = "/dev/ttyUSB1"
print(portName)

try:
    ser = serial.Serial(port=portName, baudrate=115200)
    print("Open successfully")
except:
    print("Can not open the port")

def addModbusCrc(msg):
    crc = 0xFFFF
    for n in range(len(msg)):
        crc ^= msg[n]
        for i in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    ba = crc.to_bytes(2, byteorder='little')
    msg.append(ba[0])
    msg.append(ba[1])
    return msg


# relay1_ON = [1, 6, 0, 0, 0, 255]
# relay1_OFF = [1, 6, 0, 0, 0, 0]

relay2_ON = [2, 6, 0, 0, 0, 255]
relay2_OFF = [2, 6, 0, 0, 0, 0]

relay3_ON = [3, 6, 0, 0, 0, 255]
relay3_OFF = [3, 6, 0, 0, 0, 0]

relay4_ON = [4, 6, 0, 0, 0, 255]
relay4_OFF = [4, 6, 0, 0, 0, 0]

# relay5_ON = [5, 6, 0, 0, 0, 255]
# relay5_OFF = [5, 6, 0, 0, 0, 0]

# relay6_ON = [6, 6, 0, 0, 0, 255]
# relay6_OFF = [6, 6, 0, 0, 0, 0]

# relay7_ON = [7, 6, 0, 0, 0, 255]
# relay7_OFF = [7, 6, 0, 0, 0, 0]

# relay8_ON = [8, 6, 0, 0, 0, 255]
# relay8_OFF = [8, 6, 0, 0, 0, 0]

def setDeviceON(id):
    match id:
        case 2:
            ser.write(addModbusCrc(relay2_ON))
        case 3:
            ser.write(addModbusCrc(relay3_ON))
        case 4:
            ser.write(addModbusCrc(relay4_ON))

    time.sleep(1)
    print(serial_read_data(ser))

def setDeviceOFF(id):
    match id:
        case 2:
            ser.write(addModbusCrc(relay2_OFF))
        case 3:
            ser.write(addModbusCrc(relay3_OFF))
        case 4:
            ser.write(addModbusCrc(relay4_OFF))

    time.sleep(1)
    print(serial_read_data(ser))




def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0

soil_temperature =[1, 3, 0, 6, 0, 1]
def readTemperature():
    serial_read_data(ser)
    ser.write(addModbusCrc(soil_temperature))
    time.sleep(1)
    return serial_read_data(ser)

soil_moisture = [1, 3, 0, 7, 0, 1]
def readMoisture():
    serial_read_data(ser)
    ser.write(addModbusCrc(soil_moisture))
    time.sleep(1)
    return serial_read_data(ser)

def writeData(id, state):
    if state == "1":
        setDeviceON(id)
    else:
        setDeviceOFF(id)

def readSerial(client):
    client.publish("cambien1", readTemperature())
    time.sleep(2)
    client.publish("cambien2", readMoisture())

# while True:
#     print("TEST SENSOR")
#     print(readMoisture())
#     time.sleep(1)
#     print(readTemperature())
#     time.sleep(1)