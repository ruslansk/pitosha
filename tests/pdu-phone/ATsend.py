#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
