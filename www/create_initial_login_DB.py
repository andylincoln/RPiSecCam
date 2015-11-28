
import MySQLdb as mdb
import md5
import os
from time import sleep

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)

cnx = mdb.connect('127.0.0.1','root','');

if (GPIO.input(21)==True):
  with cnx:
    cur = cnx.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS iotdevdb")
    cur.execute("USE iotdevdb")
    cur.execute("DROP TABLE IF EXISTS login")
    cur.execute("CREATE TABLE login (L1 CHAR(32), L2 CHAR(64), role CHAR(1))")

    m = md5.new()
    m.update("123456789")
    epw= m.hexdigest()
    cur.execute("INSERT INTO login (L1, L2, role) \
		VALUES( 'administrator',%s,'a')", epw)
    
    cur.execute("DROP TABLE IF EXISTS iotlog")
    cur.execute("CREATE TABLE iotlog (ldate DATE, ltime TIME, devname TEXT, logentry VARCHAR(256))")
    cur.execute("INSERT INTO iotlog (ldate, ltime, devname, logentry) \
		VALUES( CURRENT_DATE() - INTERVAL 1 DAY, NOW(), 'exampledev', 'Initial State Setting on GPIO Reset')")
  
else:
    print "login database OK"




