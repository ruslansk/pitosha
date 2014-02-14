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
  text_head = input_file.readline()
  print text_head

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
        print 'SMSC:             SMSC Object'
        smscobj = decoded['SMSC']
        print '  .Location:      ' + str(smscobj['Location'        ])
        print '  .Number:        ' + smscobj['Number'              ]
        print '  .Name:          ' + smscobj['Name'                ]
        print '  .DefaultNumber: ' + smscobj['DefaultNumber'       ]
        print '  .Format:        ' + smscobj['Format'              ]
        print '  .Validity:      ' + smscobj['Validity'            ]
        print 'Number:           ' + decoded['Number'              ]
        print 'Name:             ' + decoded['Name'                ]
        print 'UDH:              UDH Object'
        udh_obj = decoded['UDH']
        print '  .ID8bit:        ' + str(udh_obj['ID8bit'          ])
        print '  .ID16bit:       ' + str(udh_obj['ID16bit'         ])
        print '  .PartNumber:    ' + str(udh_obj['PartNumber'      ])
        print '  .AllParts:      ' + str(udh_obj['AllParts'        ])
        print '  .Type:          ' + udh_obj['Type'                ]
        print '  .Text:          ' + udh_obj['Text'                ]
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
        #print 'DateTime:         ' + decoded['DateTime'].strftime("%Y-%m-%d %H:%M:%S")
        print 'DateTime:         ' + str('<>' if   decoded['DateTime'] is None
                                              else decoded['DateTime'].strftime("%Y-%m-%d %H:%M:%S"))
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

def decodeFile(filename, offset=0):
    # dd bs=512 count=1 if=/dev/sda of=mbr.bkp
    import struct, binascii
    f = open(filename, 'rb')
    f_data = f.read()
    t_data = f_data[0:3]
    print " Jump Instruction: " + t_data.encode('hex')
    #t_data = f_data[3:11]
    #print "           OEM ID: " + t_data.encode('hex')
    #t_data = binascii.b2a_uu(f_data[3:11])
    t_data = struct.unpack_from('8s', f_data[3:11])
    print "           OEM ID: " + t_data[0]
    t_data = f_data[11:36]
    print "              BPB: " + t_data.encode('hex')
    f_len  = len(f_data)
    if f_len < 512:
        print "Read this many bytes: " + str(f_len)
    #values = struct.unpack('17d', f_data[ offset + 0 : offset + 8*17 ])
    f.close()

#########################################################################

