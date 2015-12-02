# NotificationController.py
# Andy Lincoln
# RPiSecCam

import smtplib as SMTP
import email
import email.mime.application
import yaml
import socket
import time
import serial
import pykka
import logging
import re
from operator import itemgetter
from types import *
from curses import ascii


# EmailClient class for sending emails over SMTP using the details given in config.yaml
class EmailClient:

    def __init__(self):
        with open('../data/config.yaml', 'r') as f:
            doc = yaml.load(f)
        self.host = doc["email"]["host"]
        self.port = doc["email"]["port"]
        self.fromAddr = doc["email"]["address"]
        self.password = doc["email"]["password"]
        self.local_hostname = socket.gethostname()

        self.smtp = SMTP.SMTP(self.host, self.port)
        # Debugger Check
        self.smtp.set_debuglevel(False)
        self.smtp.starttls()
        self.smtp.login(self.fromAddr,self.password)

    def sendEmail(self, toAddr, subject, message, attachments=[]):
        msg = email.mime.Multipart.MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.fromAddr
        msg['To'] = toAddr
        # TODO add attachements
        body = email.mime.Text.MIMEText(message)
        msg.attach(body)

        self.smtp.sendmail(self.fromAddr, toAddr, msg.as_string())

# GSMModem class enables use of the serial connection to the GSM Modem
class GSMModem:

    # Modem Commands and other necessary strings
    AT      = 'AT'
    ALL     = 'ALL'
    CBC     = '+CBC'
    CMGD    = '+CMGD='
    CMGF    = '+CMGF='
    CMGL    = '+CMGL='
    CMGR    = '+CMGR='
    CMGS    = '+CMGS='
    COPS    = '+COPS?'
    CPAS    = '+CPAS'
    CPMS    = '+CPMS='
    CR      = '\r'
    CSQ     = '+CSQ'
    CTRLZ   = ascii.ctrl('z')
    NEWLINE = '\n'
    ME      = 'ME'
    MT      = 'MT'
    OK      = 'OK'
    PLUS    = '+'
    QUOTES  = '\"'
    SM      = 'SM'

    def __init__(self):
        self.serialPort="/dev/ttyUSB0"

        response = self.sendCommand(GSMModem.AT + GSMModem.NEWLINE)
        if (response != GSMModem.OK):
            raise Exception("Failed to establish connection to GSM Modem {x}".format(x=self.serialPort))
        self.sendCommand(GSMModem.AT + "CMGF=1" + GSMModem.NEWLINE)
        self.sendCommand(GSMModem.AT + "CMGF=?" + GSMModem.NEWLINE)
        self.sendCommand(GSMModem.AT+GSMModem.NEWLINE)

    def getCBC(self):
        return self.sendCommand(GSMModem.AT+GSMModem.CBC+GSMModem.NEWLINE)

    def getBatteryLevel(self):
        response = self.getCBC()
        return response[8:10]

    def getVoltageLevel(self):
        response = self.getCBC()
        return response[11:]

    def getLastMessage(self):
        count = self.getAllMessageCount()
        return self.getSMS(count)

    def getCMGL(self):
        return self.sendCommand(GSMModem.AT+GSMModem.CMGL+GSMModem.NEWLINE)

    def getCOPS(self):
        return sendCommand(GSMModem.AT+GSMModem.COPS+GSMModem.NEWLINE)

    def getNetwork(self):
        response = self.getCOPS()
        return response[12:-1]

    def getCSQ(self):
        return sendCommand(GSMModem.AT+GSMModem.CSQ+GSMModem.NEWLINE)

    def getSignalStrength(self):
        response = self.getCSQ()
        return response[6:]

    def setCPMS(self, storageToRead):
        self.sendCommand(GSMModem.AT+GSMModem.CMGF+GSMModem.NEWLINE)
        response = self.sendCommand(GSMModem.AT+GSMModem.CPMS+GSMModem.QUOTES+storageToRead+GSMModem.QUOTES+GSMModem.NEWLINE)
        #return (response[3]).translate(None,"".join('\n'))
        return response


    # Pass the index of the message, a Message object is returned
    def getSMS(self, messageIndex):
        serialConnection = serial.Serial(self.serialPort, baudrate=9600, timeout=8)
        serialConnection.write(GSMModem.AT + GSMModem.CMGF + GSMModem.NEWLINE)
        serialConnection.write(GSMModem.AT + GSMModem.CMGR + str(messageIndex) + GSMModem.NEWLINE)
        messagePosition = [3, 4]
        response = itemgetter(*messagePosition)(serialConnection.readlines())
        serialConnection.close()
        return Message(response)

    def getAllMessagesByStatus(self, messageStatus):
        serialConnection = serial.Serial(self.serialPort, baudrate=9600, timeout=8)
        serialConnection.write(GSMModem.AT + GSMModem.CMGF + GSMModem.NEWLINE)
        serialConnection.write(GSMModem.AT + GSMModem.CMGL+ GSMModem.QUOTES + messageStatus + GSMModem.QUOTES + GSMModem.NEWLINE)

        response = serialConnection.readlines()
        serialConnection.close()

        first_ok_index = ''.join(response).find('OK')
        last_ok_index = ''.join(response).find('OK', first_ok_index + 1)

        return ''.join(response)[first_ok_index+6:last_ok_index-1]

    def getAllMessageCount(self):
        cpmsResponse = self.setCPMS(GSMModem.MT)
        digitSearch = re.search("\d", cpmsResponse)
        messageCount = cpmsResponse[digitSearch.start():digitSearch.start()+1]
        return int(messageCount)

    # Send a message over a serial connection to specified telphone number
    def sendSMS(self, telephoneNumber, message):

            if (self.isTelephoneNumber(telephoneNumber) != True):
                raise ValueError("Bad phone number!")
            serialConnection = serial.Serial(self.serialPort, baudrate=9600, timeout=5)
            serialConnection.write(GSMModem.AT+GSMModem.CMGF+'1'+GSMModem.NEWLINE)
            # AT+CMGS="+19783190545"\n
            serialConnection.write(GSMModem.AT+GSMModem.CMGS+GSMModem.QUOTES+telephoneNumber+GSMModem.QUOTES+GSMModem.NEWLINE)
            # write the message
            serialConnection.write(message)
            serialConnection.write(GSMModem.CTRLZ)
            serialConnection.close()

    # Pass a string of characters, this will tell you if it is in the proper telephone number format
    def isTelephoneNumber(self, number):
        if len(number) != 12:
            return False
        if number[1] != '1':
            return False # Don't want to accidentally text a foreign number
        for i, digit in enumerate(number):
            if i == 0: #skip plus sign!
                if digit == GSMModem.PLUS:
                    continue
                else:
                    return False
            if digit.isdigit() != True:
                return False
        return True

    # Use this to check if the array returned from getResponse() is what you expected it to be
    def isValidResponse(self, ack, str_input, expected):
        assert isinstance(ack, list) is True, "ack must be an array %s" % s
        self.sanitize(ack)
        return ((ack[0] == str_input) and (ack[1] == expected))

    # Pass a string to this to get all the garbage characters out there that we don't need to see
    def sanitize(self, str):
        chars_to_remove = ['\x00', '\t', GSMModem.CR, GSMModem.NEWLINE]
        str = str.translate(None,''.join(chars_to_remove))
        return str

    # Identify message details from the response string of reading a single message
    def reformatSingleMessage(self, messageString):
        quotationIndex = messageString.find('"')
        nextQuotationIndex = messageString.find('"', quotationIndex+1)
        messageStatus = 'Status: '+messageString[quotationIndex+1:nextQuotationIndex]

        quotationIndex = messageString.find('"', nextQuotationIndex+1)
        nextQuotationIndex = messageString.find('"', quotationIndex+1)
        messageSenderNumber = '\nSender: '+messageString[quotationIndex+1:nextQuotationIndex]

        quotationIndex = messageString.find('"', nextQuotationIndex+4)
        nextQuotationIndex = messageString.find('"', quotationIndex+1)
        messageTimeStamp = '\nReceived on:' + messageString[quotationIndex+1:nextQuotationIndex]

        quotationIndex = messageString.find('\'', nextQuotationIndex+6)
        nextQuotationIndex = messageString.find('\'', quotationIndex+1)
        messageValue = '\nMessage:' + messageString[quotationIndex+1:nextQuotationIndex-4]

        return messageStatus+messageSenderNumber+messageTimeStamp+messageValue

    def sendCommand(self, str_input):
        serialConnection = serial.Serial(self.serialPort, baudrate=9600, timeout=8)
        serialConnection.write(str_input)
        ack = serialConnection.readlines()
        serialConnection.close()

        #Lop off the echo
        ack.pop(0)

        # Clean out unneeded chars
        return self.sanitize(ack[0])

class Message:

    def __init__(self, tup):
        self.status      = tup[0][12:16]
        self.phoneNumber = tup[0][19:31]
        self.timestamp   = tup[0][40:57]
        self.content     = tup[1]

    def status(self):
        return self.status

    def phoneNumber(self):
        return self.phoneNumber

    def timestamp(self):
        return self.timestamp

    def content(self):
        return self.content


class NotificationController(pykka.ThreadingActor):

    emailClient = EmailClient()
    gsm = GSMModem()

    def __init__(self):
        super(NotificationController, self).__init__()

    def notify(message, numbers, addresses, attachment=None, phone=False, email=True):

        if (Not(phone or email)):
           raise Exception("You must use at least one notification system!")
        if (email):
            for email in addresses:
                emailClient.sendEmail(email, "Activity Detected", "Activity has been detected, photo is attached",
                attachment)
        if (phone):
            for number in numbers:
                gsm.sendSMS()
    def on_receive(self, message):
        if (message == { 'msg': "STATUS"}):
            return self.status()

    def status(self):

        message = self.gsm.getLastMessage()

        if ("DISARMED" in message.content):
            return False
        elif ("ARMED" in message.content):
            return True
        else:
            return None
