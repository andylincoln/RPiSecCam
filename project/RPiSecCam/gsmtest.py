from notificationcontroller import GSMModem

gsm = GSMModem()

print "All"
print gsm.getAllMessagesByStatus("ALL")

#print "Read"
#print gsm.getAllMessagesByStatus("REC READ")
#print "\n"
#print "Unread"
#print gsm.getAllMessagesByStatus("REC UNREAD")
