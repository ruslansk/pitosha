#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pdtool import fixes

import cmd

class PduToolCmd(cmd.Cmd):
    """Simple command processor example."""

    prompt = 'pdutool#: '
    intro  = "Добро пожаловать в сборщик PDU :)\n"\
             "Для справки по доступным командам наберите: help\n"

    #def preloop(self):
    #    #print 'Welcome to DPU collector :)'
    #    print 'Добро пожаловать в сборщик PDU :)'
    #    print ''
    
    def do_greet(self, person):
        if person:
            print "hello,", person
        else:
            print 'hello'
    def help_greet(self):
        print '\n'.join([ 'greet [person]',
                          'Greet the named person',
                        ])
    
    def do_EOF(self, line):   # Ctrl-D, ^D$
        return True
    def do_exit(self, line):
        return True
    def do_e(self, line):
        return True
    def do_quit(self, line):
        return True
    def do_q(self, line):
        return True

    def postloop(self):
        #print "Bye!"
        print ''
        print 'Пока-пока!'

if __name__ == '__main__':
    PduToolCmd().cmdloop()

#while True:
#    sys.stdout.write("any? (Y/n): ")
#    c = fixes.getch()
#    print ""
#    #c = raw_input('Press y to continue, or n to exit: ')
#    if c.upper() == 'N': break

exit()
##########################################################

#import pdtool
#import pdtool.dbsqc as sqtool
#from pdtool import dbsqc as sqtool

import bluetooth
import serial
import time

#def spyder_getpass(prompt='Password: '):
#  set_spyder_echo(False)
#  password = raw_input(prompt)
#  set_spyder_echo(True)
#  return password
#
#print "Oops! Ha-ha! :) Your password is: " + spyder_getpass()

import getpass
import sys

ppp = getpass.getpass(stream=sys.stderr,              # где ты была сегодня киска?
                      prompt='Wath? ')
# warning: for set bluetooth PIN use command:
#   $> bluetooth-agent 0000 &
mac = 'E8:92:A4:04:99:4A'                             # bt-адрес mtk_first
mac = '00:AA:70:1E:08:B3'                             # bt-адрес mtk_second
chn = 9                                               # канал DUN-интерфейса (для mtk)

sockfd = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sockfd.connect((mac, chn))                            # BT Адрес и номер канала

#sockfd.send('AT+CMGF=1\r')
#sockfd.send('AT+CMGF=0\r')
sockfd.send('AT+CPMS=?\r')
#sockfd.send('AT+CPMS?\r')
time.sleep(1)
print sockfd.recv(1024)

sockfd.send(chr(26))                                   # CTRL+Z
sockfd.close()

exit()

#################################################################################

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
