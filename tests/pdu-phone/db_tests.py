#!/usr/bin/env python
# -*- coding: utf-8 -*-

##  import pysqlcipher.dbapi2 as sqlite
##  >>> sqlite.version
##  '2.6.3'
##  >>> sqlite.sqlite_version
##  '3.7.14.1'

import sys
import pysqlcipher.dbapi2 as sqc3
print "lib ver.: " + sqc3.version
print "sql ver.: " + sqc3.sqlite_version

conn=sqc3.connect('bdata.db')
cur = conn.cursor()
cur.execute("PRAGMA key='123'")
#c.execute('select * from info')
#
#for row in c:
#    print row[0]

def create_table(table_name):
    global conn, cur
    sql = 'create table if not exists ' + table_name + ' (id integer)'
    cur.execute(sql)
    conn.commit()

def createT():
    global conn, cur
    #sql = 'CREATE TABLE pdu_data ('       +\
    sql = 'CREATE TABLE IF NOT EXISTS pdu_data ('       \
                      ' id       INTEGER PRIMARY KEY, ' \
                      ' dev_name VARCHAR(100), '        \
                      ' date_add VARCHAR(30),  '        \
                      ' pdu_blob VARCHAR(500)) '
    cur.execute(sql)
    conn.commit()

def insertT(devName, dateAdd, pduBlob):
    global conn, cur
    cur.execute('INSERT INTO pdu_data VALUES (null, ?, ?, ?)', (devName, dateAdd, pduBlob))
    conn.commit()

def selectAll():
    global conn, cur
    cur.execute('SELECT * FROM pdu_data')
    for row in cur:
        print '-'*10
        print '     ID: ', row[0]
        print 'DevName: ', row[1]
        print 'DateAdd: ', row[2]
        print 'PduBlob: ', row[3]
        print '-'*10

def selectOne(idx):
    global conn, cur
    cur.execute('SELECT * FROM pdu_data pd WHERE pd.id=' + str(idx))
    for row in cur:
        print '-'*10
        print '     ID: ', row[0]
        print 'DevName: ', row[1]
        print 'DateAdd: ', row[2]
        print 'PduBlob: ', row[3]
        print '-'*10

def insert_to_table(table_name, num):
    global conn, cur
    sql = 'insert into ' + table_name + ' (id) values (%d)' % (num)
    cur.execute(sql)
    conn.commit()

def select_from_table(table_name):
    global conn, cur
    cur.execute('select * from ' + table_name)
    for row in cur:
        print row[0]

#########

try:
    cur.execute('SELECT SQLITE_VERSION()')
    data = cur.fetchone()
    print "SQLite version: %s" % data

    #create_table('testinger')
    #insert_to_table('testinger', 4)
    #select_from_table('testinger')
    createT()
    #insertT(devName, dateAdd, pduBlob)
    #insertT('devMTK_1', '11 feb', "394874jkfgfksh895419593451")
    #selectAll()
    #selectOne(1)

    input_file = open(sys.argv[1])
    while True:
        put_DUNtext()
        sys.stdout.write("any? (Y/n): ")
        c = getch()
        print ""
        if c.upper() == 'N': break

#except sqc3.Error, e:
#    print "Error %s:" % e.args[0]
#    sys.exit(1)
finally:
    if conn:
        conn.close()

#cur.close()
#conn.close()

exit()

##############################################################################

import sys

try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try:
        import msvcrt
    except ImportError:
        # FIXME what to do on other platforms?
        # Just give up here.
        raise ImportError('getch not available')
    else:
        getch = msvcrt.getch
else:
    def getch():
        """getch() -> key character

        Read a single keypress from stdin and return the resulting character. 
        Nothing is echoed to the console. This call will block if a keypress 
        is not already available, but will not wait for Enter to be pressed. 

        If the pressed key was a modifier key, nothing will be detected; if
        it were a special function key, it may return the first character of
        of an escape sequence, leaving additional characters in the buffer.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

input_file = open(sys.argv[1])
#text = input_file.readlines()

def put_DUNtext():
    global input_file
    text_1 = input_file.readline()
    print "1: " + text_1
    text_2 = input_file.readline()
    print "2: " + text_2
    text_3 = input_file.readline()
    print "3: " + text_3
    print "-----------"

while True:
    put_DUNtext()
    sys.stdout.write("any? (Y/n): ")
    c = getch()
    print ""
    #c = raw_input('Press y to continue, or n to exit: ')
    if c.upper() == 'N': break
    #ch = sys.stdin.read(1)
    #if ch is not 'y': break

exit()

import bluetooth
import serial
import time

#def SendViaBluetooth():
sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#sockfd.connect(('E8:92:A4:04:99:4A', 9))               # BT Адрес и номер канала
sockfd.connect(('00:AA:70:1E:08:B3', 9))

#sockfd.send('AT+CNUM\r')
#time.sleep(1)
#print sockfd.recv(1024)
#sockfd.send(chr(26))                                   # CTRL+Z
#sockfd.close()
#exit()

#sockfd.send('AT+CMGF=1\r')                            #
sockfd.send('AT+CMGF=0\r')                             #
time.sleep(1)
print sockfd.recv(1024)

sockfd.send('AT+CMGL=4\r')
#sockfd.send('AT+CMGR=2\r')
#sockfd.send('AT+CMGR=1\r')
#sockfd.send('AT+CMGR=3\r')
#sockfd.send('AT+CMGR=4\r')

#sockfd.send('AT+CUSD=1,"*105#"\r')                    #
time.sleep(1)
#print sockfd.recv(1024)
#print sockfd.recv(1024)
#print sockfd.recv(2048)
print sockfd.recv(40000)
sockfd.send(chr(26))                                   # CTRL+Z
sockfd.close()

#sockfd.send('ATZ\r')
#time.sleep(1)
#print sockfd.recv(1024)
#sockfd.send(chr(26))                                   # CTRL+Z
#sockfd.close()
