import time
import serial
from types import *
from curses import ascii

# Modem Commands and other necessary strings
AT='AT'
OK='OK'
CTRLZ=ascii.ctrl('z')
CR='\r'
PLUS='+'
NEWLINE='\n'
CMGF='+CMGF=1'
CMGS='+CMGS='
QUOTES='\"'
COPS='+COPS?'
CSQ='+CSQ'
CBC='+CBC'


def getCBC(serialConnection):
    sendCommand(serialConnection, AT+CBC+NEWLINE)
    response = sanitize(getResponse(serialConnection))
    return response

def getBatteryLevel(serialConnection):
    response = getCBC(serialConnection)
    return response[8:10]

def getVoltageLevel(serialConnection):
    response = getCBC(serialConnection)
    return response[11:]

def getCOPS(serialConnection):
    sendCommand(serialConnection, AT+COPS+NEWLINE)
    response = sanitize(getResponse(serialConnection))
    return response

def getNetwork(serialConnection):
    response = getCOPS(serialConnection)
    return response[12:-1]

def getCSQ(serialConnection):
    sendCommand(serialConnection, AT+CSQ+NEWLINE)
    response = sanitize(getResponse(serialConnection))
    return response

def getSignalStrength(serialConnection):
    response = getCSQ(serialConnection)
    return response[6:]

# Send a message over a serial connection to specified telphone number
def sendSMS(serialConnection, message, telephoneNumber):

        if isTelephoneNumber(telephoneNumber) != True:
            raise ValueError("Bad phone number!")

        sendCommand(serialConnection, AT+CMGF+NEWLINE)
        # AT+CMGS="+19783190545"\n
        sendCommand(serialConnection, AT+CMGS+QUOTES+telephoneNumber+QUOTES+NEWLINE)
        # write the message
        sendCommand(serialConnection, message)
        sendCommand(serialConnection, CTRLZ)

# For some reason this doesn't work
def openConnection(connection='/dev/ttyUSB0', timeout=5):
    return serial.Serial(connection, 9600, timeout)  # open port

# But this does
def closeConnection(serialConnection):
    serialConnection.close()

# Pass a string of characters, this will tell you if it is in the proper telephone number format
def isTelephoneNumber(number):
    if len(number) != 12:
        return False
    if number[1] != '1':
        return False # Don't want to accidentally text a foreign number
    for i, digit in enumerate(number):
        if i == 0: #skip plus sign!
            if digit == PLUS:
                continue
            else:
                return False
        if digit.isdigit() != True:
            return False
    return True

# Use this to check if the array returned from getResponse() is what you expected it to be
def isValidResponse(ack, str_input, expected):
    assert isinstance(ack, list) is True, "ack must be an array %s" % s
    sanitize(ack)
    return ((ack[0] == str_input) and (ack[1] == expected))

# Pass a string to this to get all the garbage characters out there that we don't need to see
def sanitize(str):
    chars_to_remove = ['\x00', '\t', CR, NEWLINE]
    str = str.translate(None,''.join(chars_to_remove))
    return str

# A nice layer over serialConnection.write to make it more readable
def sendCommand(serialConnection, str_input):
    serialConnection.write(str_input)
    serialConnection.flush()

# Use this after a sendCommand() to get the output, which should be a list of length 2, with the echo and the response
def getAck(serialConnection):
    return serialConnection.readlines()
# Shortcut
def getEcho(serialConnection):
    return getAck(serialConnection)[0]
#Shortcut
def getResponse(serialConnection):
    return getAck(serialConnection)[1]






# Main code

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=5)  # open port
try:
    sendCommand(ser, AT+NEWLINE)
    getAck(ser)
    # print "Testing phone number validity code:"
    # phoneNumber = '+19783190545'
    # message = "This should definitely work now!"
    # if (isTelephoneNumber(phoneNumber)):
        # sendSMS(ser,message,phoneNumber) # commented out so I don't accidentally text
    #    print getResponse(ser)

    print "Checking CBC"
    print getCBC(ser)
    print getBatteryLevel(ser)
    print getVoltageLevel(ser)

    print "Checking COPS"
    print getCOPS(ser)
    print getNetwork(ser)

    print "Checking CSQ"
    print getCSQ(ser)
    print getSignalStrength(ser)
finally:
    print "Closing connection!"
    closeConnection(ser)

