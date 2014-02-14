#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import bluetooth
import serial
import time

#################################################################################
# warning: for set bluetooth PIN use command:
#   $> bluetooth-agent 0000 &

mac = '00:AA:70:1E:08:B3'                                 # bt-адрес mtk_second
mac = 'E8:92:A4:04:99:4A'                                 # bt-адрес mtk_first
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
# 'AT+CNUM\r'

# AT+ESUO?
# AT+EFSR -> Err
# AT+ESLP=0
# AT+ESUO=3
# AT+EFSR -> NO err
# AT+ESUO=4
# ATE0
# AT+CMGF=0
# AT+CSCS="UCS2_0x81"
# AT+CSCS="UCS2"
# AT+ESUO=3
# AT+EFSW?
# AT+EFSC=?
# AT+ESUO=4
# AT+EQUERY=0
# AT+EVCARD=?
# AT+CPMS=?
# AT+EQUERY=5
# AT+EMMSFS=?
# AT+EQUERY=6
# AT+EMGR=?
# AT+EQUERY=7
# AT+ESUO=?
# AT+ESUO=5
# ATE0
# AT+CSCS="UCS2"
# AT+ESUO=6
# ATE0
# AT+CSCS="UCS2"
# AT+ESUO=4
# AT+CPMS?
# AT+EQSI="SM"
# AT+EQSI="ME"
# AT+CPMS="SM", "SM_P"
# AT+EMGR=1

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

def st_readSM():
    sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sockfd.connect((mac, chn))                            # BT Адрес и номер канала
    
    sockfd.send('AT+CPMS="SM_P"\r')                       # выбор хранилища SIM
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send('AT+CMGL=4\r')                            # чтение sms по индексу
    time.sleep(2)
    out_data = sockfd.recv(40000)

    fh = open("temp.bkp","w")
    fh.write(out_data)
    fh.close()
    print out_data

    sockfd.send(chr(26))                                  # CTRL+Z
    sockfd.close()

def st_readME():
    sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sockfd.connect((mac, chn))                            # BT Адрес и номер канала
    
    sockfd.send('AT+CPMS="ME"\r')                         # выбор хранилища в памяти телефона
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send('AT+CMGL=4\r')                            # чтение sms по индексу
    time.sleep(8)
    out_data = sockfd.recv(700000)

    fh = open("temp.bkp","w")
    fh.write(out_data)
    fh.close()
    print out_data

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

def st_send(atcmd):
    sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sockfd.connect((mac, chn))                            # BT Адрес и номер канала
    
    sockfd.send(atcmd+'\r')                               # manual AT-command
    time.sleep(1)
    print sockfd.recv(1024)

    sockfd.send(chr(26))                                  # CTRL+Z
    sockfd.close()

#################################################################################

