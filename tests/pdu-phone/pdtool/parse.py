#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# my tool: from 'fixes' import 'getch' 
import fixes

def put_DUNtext():
    global input_file
    text_1 = input_file.readline()
    print "1: " + text_1
    text_2 = input_file.readline()
    print "2: " + text_2
    text_3 = input_file.readline()
    print "3: " + text_3
    print "-----------"

def parseFile(filename):
  global input_file
  input_file = open(filename)
  #input_file = open(sys.argv[1])
  #text = input_file.readlines()

  while True:
    put_DUNtext()
    #txt = "next? (Y/n): "
    txt = "Print single Info    (1)\n"\
          "Print single Blob    (2)\n"\
          "Decode PDU message   (3)\n"\
          "Add record to opened (4)\n"\
          "Next?              (Y/n): "
    sys.stdout.write(txt)
    c = fixes.getch()
    print ""
    #c = raw_input('Press y to continue, or n to exit: ')
    if   c.upper() == 'N': break
    elif c.upper() == 'Y':
        print "Entered Y"
    elif c.upper() == '1':
        print "Entered 1"
    elif c.upper() == '2':
        print "Entered 2"
    elif c.upper() == '3':
        print "Entered 3"
    elif c.upper() == '4':
        print "Entered 4"
    else:
        print "Enter correct data"
    #ch = sys.stdin.read(1)
    #if ch is not 'y': break

