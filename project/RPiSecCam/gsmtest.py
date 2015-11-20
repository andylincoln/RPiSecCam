from notificationcontroller import GSMModem

gsm = GSMModem()

print "All"
print gsm.getAllMessagesByStatus("ALL")

print "Get message @ index 3"
print gsm.getSMS(3)

print "Get message count"
print gsm.getAllMessageCount()

print "Get last message"
print gsm.getLastMessage()

#print "Read"
#print gsm.getAllMessagesByStatus("REC READ")
#print "\n"
#print "Unread"
#print gsm.getAllMessagesByStatus("REC UNREAD")
