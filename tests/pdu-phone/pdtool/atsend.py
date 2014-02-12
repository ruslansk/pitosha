#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import bluetooth
import serial
import time

#################################################################################
# warning: for set bluetooth PIN use command:
#   $> bluetooth-agent 0000 &

mac = 'E8:92:A4:04:99:4A'                                 # bt-адрес mtk_first
mac = '00:AA:70:1E:08:B3'                                 # bt-адрес mtk_second
chn = 9                                                   # канал DUN-интерфейса (для mtk)

# 'AT+CMGF=1\r'         # установка передачи в режиме PDU
# 'AT+CMGF=0\r'         # установка передачи в текстовом режиме
# 'AT+CPMS=?\r'         # приоритет систем хранения sms
# 'AT+CPMS?\r'          # количество sms в системах хранения
# 'AT+CPMS="SM_P"\r'    # установка текущего хранилища на SIM
# 'AT+CPMS="ME"\r'      # установка текущего хранилища на память телефона
# 'AT+CMGL=4\r'         # 4 - чтение всех смс с текущего хранилища
# 'AT+CMGR=2\r'         # чтение смс с определенным индексом (например: 2)
# chr(26)               # CTRL+Z

# 'ATZ\r'
# 'AT+CUSD=1,"*105#"\r'

def st_priority():
    sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sockfd.connect((mac, chn))                            # BT Адрес и номер канала
    
    sockfd.send('AT+CPMS=?\r')   # приоритет систем хранения sms
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send(chr(26))                                  # CTRL+Z
    sockfd.close()

def st_counts():
    sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sockfd.connect((mac, chn))                            # BT Адрес и номер канала
    
    sockfd.send('AT+CPMS?\r')    # количество sms в системах хранения
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send(chr(26))                                  # CTRL+Z
    sockfd.close()

def st_setSM():
    sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sockfd.connect((mac, chn))                            # BT Адрес и номер канала
    
    sockfd.send('AT+CPMS=?\r')   # приоритет систем хранения sms
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send('AT+CPMS="SM_P"\r')                       # выбор хранилища на SIM
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send('AT+CPMS=?\r')   # приоритет систем хранения sms
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send(chr(26))                                  # CTRL+Z
    sockfd.close()

def st_setME():
    sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sockfd.connect((mac, chn))                            # BT Адрес и номер канала
    
    sockfd.send('AT+CPMS=?\r')   # приоритет систем хранения sms
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send('AT+CPMS="ME"\r')                         # выбор хранилища в памяти телефона
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send('AT+CPMS=?\r')   # приоритет систем хранения sms
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send(chr(26))                                  # CTRL+Z
    sockfd.close()

def st_readOneFromSM(idx):
    sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sockfd.connect((mac, chn))                            # BT Адрес и номер канала
    
    sockfd.send('AT+CPMS="SM_P"\r')                       # выбор хранилища SIM
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send('AT+CMGR=' + str(idx) + '\r')             # чтение sms по индексу
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send(chr(26))                                  # CTRL+Z
    sockfd.close()

def st_readOneFromME(idx):
    sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sockfd.connect((mac, chn))                            # BT Адрес и номер канала
    
    sockfd.send('AT+CPMS="ME"\r')                         # выбор хранилища в памяти телефона
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send('AT+CMGR=' + str(idx) + '\r')             # чтение sms по индексу
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send(chr(26))                                  # CTRL+Z
    sockfd.close()

#################################################################################

'''
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
#sockfd.send('AT+CMGF=0\r')                             #

#sockfd.send('AT+CPMS=?\r')
#sockfd.send('AT+CPMS?\r')
sockfd.send('AT+CPMS="SM_P"\r')
time.sleep(1)
print sockfd.recv(1024)
#sockfd.send(chr(26))                                   # CTRL+Z
#sockfd.close()
#exit()

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
'''
