import serial
import time 

def initConnection(portNo, baudRate):
    try:
        ser = serial.Serial(portNo, baudRate)
        print("Device connected")
        return ser
    except:
        print("Not Connected")

def sendData(se, data, digits):
    myString = "$"
    for d in data:
        myString += str(d).zfill(digits)

    try:
        se.write(myString.encode())
        print(myString)
    except:
        print("Data Transmission Failed")




if __name__ == "__main__":
    ser = initConnection( "/dev/ttyACM0",9600)
    while True:
        sendData(ser,[50,255],3)
        time.sleep(1)
        sendData(ser,[50,0],3)
        time.sleep(1)