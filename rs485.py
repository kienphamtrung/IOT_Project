import time
import serial.tools.list_ports

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

portName = getPort()
print(portName)

try:
    ser = serial.Serial(port=portName, baudrate=9600)
    print("Open successfully")
except:
    print("Can not open the port")


relay1_ON = [2, 6, 0, 0, 0, 255]
relay1_OFF = [2, 6, 0, 0, 0, 0]

relay2_ON = [3, 6, 0, 0, 0, 255]
relay2_OFF = [3, 6, 0, 0, 0, 0]

relay3_ON = [4, 6, 0, 0, 0, 255]
relay3_OFF = [4, 6, 0, 0, 0, 0]

def setDeviceON(id):
    if id == 1:
        ser.write(addModbusCrc(relay1_ON))
    elif id == 2:
        ser.write(addModbusCrc(relay2_ON))
    elif id == 3:
        ser.write(addModbusCrc(relay3_ON))
    time.sleep(1)
    print(serial_read_data(ser))

def setDeviceOFF(id):
    if id == 1:
        ser.write(addModbusCrc(relay1_OFF))
    elif id == 2:
        ser.write(addModbusCrc(relay2_OFF))
    elif id == 3:
        ser.write(addModbusCrc(relay3_OFF))
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
#     print("TEST ACTUATOR")
#     setDeviceON(1)
#     time.sleep(1)
#     setDeviceOFF(1)
#     time.sleep(1)
#
#     setDeviceON(2)
#     time.sleep(1)
#     setDeviceOFF(2)
#     time.sleep(1)
#
#     setDeviceON(3)
#     time.sleep(1)
#     setDeviceOFF(3)
#     time.sleep(1)
#
#     print("TEST SENSOR")
#     print(readMoisture())
#     time.sleep(1)
#     print(readTemperature())
#     time.sleep(1)