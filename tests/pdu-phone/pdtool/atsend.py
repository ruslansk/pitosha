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

def st_send_port(atcmd):   #   atcmd = b'ATZ\r'
    #
    # USB модем ZTE 626 с прошивкой Revision: BD_BLNMOP673M3V1.0.0B01
    # без привязки к оператору
    # предварительно на модеме выполнено
    #   AT+ZCDRUN=8       Disable cd (flashdrive) autorun
    # что бы опознавался сразу как модем
    # в настройках указываем:
    #   Additional AT commands: AT+CPBS="SM"\r\nAT+CPMS="SM","SM",""\r\n
    # эти команды указывают, где хранятся SMS сообщения (без этих команд
    # модем раз в секунду пишет сообщение +ZUSIMR: 2).
    # и остальные стандартные параметры...
    #
    #phone = serial.Serial("/dev/ttyS0",  460800, timeout=5)
    #phone = serial.Serial("/dev/ttyACM0",  460800, timeout=5)
    #phone = serial.Serial('/dev/ttyUSB1', 115200, timeout=5)
    # in windows:
    #    phone = serial.Serial(port='COM1', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, xonoff=False, rtscts=False, dsrdtr=False)
    #    phone = serial.Serial(port=3,baudrate=115200,timeout=0,rtscts=0,xonxoff=0)
    #    port=0  <-->  port='COM1'
    #    port=1  <-->  port='COM2'

    #phone = serial.Serial("/dev/ttyUSB1",
    #                              460800,
    #                          bytesize = serial.EIGHTBITS,
    #                            parity = serial.PARITY_NONE,
    #                          stopbits = serial.STOPBITS_ONE,
    #                           timeout = 5)

    # initialization and open the port
    # possible timeout values:
    #    1. None: wait forever, block call
    #    2. 0: non-blocking mode, return immediately
    #    3. x, x is bigger than 0, float allowed, timeout block call

    ser = serial.Serial()
    ser.port         = "/dev/ttyUSB1"
    #ser.baudrate    = 9600
    ser.baudrate     = 460800
    ser.bytesize     = serial.EIGHTBITS     # number of bits per bytes
    ser.parity       = serial.PARITY_NONE   # set parity check: no parity
    ser.stopbits     = serial.STOPBITS_ONE  # number of stop bits
    #ser.timeout     = None                 # block read
    ser.timeout      = 1                    # non-block read
    #ser.timeout     = 2                    # timeout block read
    ser.xonxoff      = False                # disable software flow control
    ser.rtscts       = False                # disable hardware (RTS/CTS) flow control
    ser.dsrdtr       = False                # disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2                    # timeout for write

    try:
      ser.open()
    except Exception, e:
      print "error open serial port: " + str(e)
      exit()

    if ser.isOpen():
      try:
        ser.flushInput()                    # flush input buffer, discarding all its contents
        ser.flushOutput()                   # flush output buffer, aborting current output
                                            # and discard all that is in buffer

        ser.write(b'AT+CPBS="SM"\r')        # эти команды указывают, где хранятся SMS сообщения
        time.sleep(0.5)                     # (без этих команд
        ser.write(b'AT+CPMS="SM","SM",""\r')# модем раз в секунду пишет сообщение +ZUSIMR: 2).
        time.sleep(0.5)

        ser.write(atcmd + b'\r')            # manual AT-command
        time.sleep(0.5)
        #data = ser.readline()
        data = ser.readall()
        print data
        ser.write(bytes([26]))              # CTRL+Z
        time.sleep(0.5)
      finally:
        ser.close()

#################################################################################
