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
    OK      = 'OK'
    PLUS    = '+'
    QUOTES  = '\"'

    def __init__(self):
        self.serialPort="/dev/ttyUSB0"

        response = self.sendCommand(GSMModem.AT + GSMModem.NEWLINE)
        if (response != GSMModem.OK):
            raise Exception("Failed to establish connection to GSM Modem {x}".format(x=self.serialPort))

    def getCBC(self):
        return self.sendCommand(GSMModem.AT+GSMModem.CBC+GSMModem.NEWLINE)

    def getBatteryLevel(self):
        response = self.getCBC()
        return response[8:10]

    def getVoltageLevel(self):
        response = self.getCBC()
        return response[11:]

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
        response = self.sendCommand(GSMModem.AT+GSMMode.CPMS+storageToRead+GSMModem.NEWLINE)
        return response[3].translate(None,"".join('\n'))

    # TODO
    def getSMS(self, messageIndex):
        pass

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

    def sendCommand(self, str_input):
        serialConnection = serial.Serial(self.serialPort, baudrate=9600, timeout=8)
        serialConnection.write(str_input)
        ack = serialConnection.readlines()
        serialConnection.close()
        return self.sanitize(ack[1])

class NotificationController(pykka.ThreadingActor):

    emailClient = EmailClient()
    gsm = GSMModem()

    def __init__(self):
        super(NotificationController, self).__init__()

    def notify(message, attachment=None, phone=False, email=True):

        if (Not(phone or email)):
           raise Exception("You must use at least one notification system!")

        if (email):
            emailClient.sendEmail("andrewlincoln11@gmail.com", "Testing Notification Controller Class", "This is a test")
        if (phone):
           print "TODO"
           #gsm.sendSMS()
