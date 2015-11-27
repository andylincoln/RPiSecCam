from notificationcontroller import GSMModem
from notificationcontroller import Message

gsm = GSMModem()

print "All"
print gsm.getAllMessagesByStatus("ALL")

print "Get message count"
print gsm.getAllMessageCount()

print "Get last message"
lastMessageRaw = gsm.getLastMessage()

print lastMessageRaw
print "Length: " + str(len(lastMessageRaw))

for string in lastMessageRaw:
    print string

message = Message(lastMessageRaw)
print message.status
print message.content
print message.phoneNumber
print message.timestamp

#print "Read"
#print gsm.getAllMessagesByStatus("REC READ")
#print "\n"
#print "Unread"
#print gsm.getAllMessagesByStatus("REC UNREAD")
