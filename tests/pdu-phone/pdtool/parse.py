#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

# my tool: from 'fixes' import 'getch' 
import fixes

class DUNObj(object):
    __slots__= "info", "data", "othr",

def put_DUNtext():
    global input_file
    text_1 = input_file.readline()
    print "1: " + text_1
    text_2 = input_file.readline()
    print "2: " + text_2
    text_3 = input_file.readline()
    print "3: " + text_3
    print "-----------"
    res = DUNObj()
    res.info = text_1.rstrip('\r\n')
    res.data = text_2.rstrip('\r\n')
    res.othr = text_3.rstrip('\r\n')
    return res

def parseFile(filename):
  global input_file
  input_file = open(filename)
  #input_file = open(sys.argv[1])
  #text = input_file.readlines()

  progress = True
  dun_data = None
  while True:
    if progress == True:
        dun_data = put_DUNtext()
        progress = False
    txt = "Print single Info    (1)\n"\
          "Print single Blob    (2)\n"\
          "Decode PDU message   (3)\n"\
          "Add record to opened (4)\n"\
          "Stop                 (ESC)\n"\
          "Next                 (Enter or Space): "
    if dun_data.info == 'OK':
        print "Parse completed!\n"
        break
    sys.stdout.write(txt)
    c = fixes.getch()
    print ord(c)
    #c = raw_input('Press y to continue, or n to exit: ')
    if   c.upper() == '1':
        print "Entered 1"
    elif c.upper() == '2':
        print "Entered 2"
    elif c.upper() == '3':
        print "Entered 3"
        #print dun_data.info
        #print dun_data.data
        import gammu
        # Parses PDU packet
        dun_bin = dun_data.data.decode("hex")
        decoded = gammu.DecodePDU(dun_bin) # gammu.DecodePDU(dun_bin, SMSC = False)
        print ''
        print '-------- decoded PDU -------------------------------'
        print 'SMSC:             <>'
        print 'Number:           ' + decoded['Number'              ]
        print 'Name:             ' + decoded['Name'                ]
        print 'UDH:              <>'
        print 'Text:             ' + decoded['Text'                ]
        print 'Folder:           ' + str(decoded['Folder'          ])
        print 'Location:         ' + str(decoded['Location'        ])
        print 'InboxFolder:      ' + str(decoded['InboxFolder'     ])
        print 'DeliveryStatus:   ' + str(decoded['DeliveryStatus'  ])
        print 'ReplyViaSameSMSC: ' + str(decoded['ReplyViaSameSMSC'])
        print 'Class:            ' + str(decoded['Class'           ])
        print 'MessageReference: ' + str(decoded['MessageReference'])
        print 'ReplaceMessage:   ' + str(decoded['ReplaceMessage'  ])
        print 'RejectDuplicates: ' + str(decoded['RejectDuplicates'])
        print 'Memory:           ' + decoded['Memory'              ]
        print 'Type:             ' + decoded['Type'                ]
        print 'Coding:           ' + decoded['Coding'              ]
        print 'DateTime:         <>' #+ decoded['DateTime'].strftime("%Y-%m-%d %H:%M:%S")
        print 'SMSCDateTime:     ' + decoded['SMSCDateTime'].strftime("%Y-%m-%d %H:%M:%S")
        print 'State:            ' + decoded['State'               ]
        print '----------------------------------------------------'
        print ''
    elif c.upper() == '4':
        print "Entered 4"
    elif c == chr(27): break
    else:
        #print "Enter correct data"
        print "Entered any other key"
        progress = True
    #ch = sys.stdin.read(1)
    #if ch is not 'y': break

