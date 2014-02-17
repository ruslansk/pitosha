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

def parsePDU(data):
    import gammu
    try:
        decoded = gammu.DecodePDU(data) # gammu.DecodePDU(dun_bin, SMSC = False)
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
    except gammu.ERR_CORRUPTED, e:
        ee = e[0]
        print ''
        print 'Gammu PDU decode error:'
        print '    -  Text: ' + str(ee['Text'])
        print '    -  Code: ' + str(ee['Code'])
        print '    - Where: ' + str(ee['Where'])
        print ''

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
        # Parses PDU packet
        dun_bin = dun_data.data.decode("hex")
        parsePDU(dun_bin)
    elif c.upper() == '4':
        print "Entered 4"
    elif c == chr(27): break
    else:
        #print "Enter correct data"
        print "Entered any other key"
        progress = True
    #ch = sys.stdin.read(1)
    #if ch is not 'y': break

def decodeTest(cmd_idx):
    import struct, binascii
    if   cmd_idx == '1':
      f = open('1_MPA3_001.bkp', 'rb')  # SMS
      f_data = f.read()
      f_len  = len(f_data)

      idx = 0
      pdu = True
      while True:
        #idx = 3 # 0, 1, 2, 3, ...
        pkt = f_data[ 0+(idx)*(186): 186+(idx)*(186)]
        pkt_one = pkt[  0:   1]
        i = pkt.index('\xff')
        t_test  = pkt[  0:  176]

        import re
        from datetime import *
        from dateutil import *
        from dateutil.tz import *
        from dateutil import tz
        #object = re.compile( ur"(.)\1{1,}$" )
        #result = object.finditer( u"hellowffffff" )
        #object = re.compile( b"(.)\xFF{1,}$" )
        #result = object.finditer( b"\xAA\xBB\xCC\xDD\xDD\xEE\xAB\xFF\xFF" )
        object = re.compile( b"(.)\xFF{1,}$" )
        result = object.finditer( t_test )
        group_name_by_index = dict( [ (v, k) for k, v in object.groupindex.items() ] )
        print group_name_by_index
        for match in result :
          #vv1 = match.groups()
          #vvv = match.span( vv1[0] + 1 )
          #print "vvv[0]: " + vvv[0]
          for group_index, group in enumerate( match.groups() ) :
            if group :
              print "text: %s" % group
              print "position: %d, %d" % match.span( group_index + 1 )
              vv = match.span( group_index + 1 )
              print vv[0]+1
              i = vv[0]+1
              #print "group: %s" % group_name_by_index[ group_index + 1 ]
            else:
              i = 176

        t_data  = pkt[  1:  i]
        #j = pkt.rfind('\xff') + 1
        #pkt__ff = pkt[  i:  j]
        #pkt_two = pkt[  j:186]
        pkt__ff = pkt[  i:176]
        pkt_two = pkt[176:186]
        h_data = t_data.encode('hex')
        print " index " + str(idx)
        print "     pkt_one: " + pkt_one.encode('hex')
        print "      t_data: " + h_data
        print " len(t_data): " + str(len(t_data))
        print "     pkt__ff: " + pkt__ff.encode('hex')
        print "     pkt_two: " + pkt_two.encode('hex')
        pkt_two_datetime   = pkt_two[0:4]
        pkt_two_datetime_r = pkt_two_datetime[::-1]
        pkt_two_datetime_h = pkt_two_datetime_r.encode('hex')
        recoverstamp       = struct.unpack('<L', pkt_two_datetime)[0]
        #recovernow         = datetime.datetime.fromtimestamp(recoverstamp)
        recovernow         = datetime.fromtimestamp(recoverstamp)
        recovernow_str     = recovernow.strftime("%Y-%m-%d %H:%M:%S")
        # auto-detect zones:
        utc_zone   = tz.tzutc()
        local_zone = tz.tzlocal()
        recovernow = recovernow.replace(tzinfo=local_zone)
        recovernow_2     = recovernow.astimezone(utc_zone)
        recovernow_str_2 = recovernow_2.strftime("%Y-%m-%d %H:%M:%S")
        print "       - datetime: " + pkt_two_datetime_h \
                                    + ' (' + str(recoverstamp) + ') ' \
                                    + recovernow_str_2
        if pdu == True and len(t_data)>0 and (pkt_one=='\x01' or pkt_one=='\x05'):
          parsePDU(t_data)

        txt = "Print prev packet       (1)\n"\
              "Print next packet       (2)\n"\
              "Decode/No PDU message   (3)\n"\
              "Stop                    (ESC)\n"
        sys.stdout.write(txt)
        c = fixes.getch()
        if   c.upper() == '1':
          if idx > 0:
            idx = idx - 1
        elif c.upper() == '2':
          if 186+(idx)*(186) < f_len:
            idx = idx + 1
        elif c.upper() == '3':
          pdu = not pdu
        elif c == chr(27): break
        else:
          #print "Enter correct data"
          print "Entered any other key"

      f.close()
    elif cmd_idx == '2':
        f = open('MP0C_004.bkp', 'rb')  # ? Ext Phonebook
        f_data = f.read()
        f_len  = len(f_data)
        f.close()
    elif cmd_idx == '3':
        f = open('MPD1_001.bkp', 'rb')  # Phonebook
        f_data = f.read()
        f_len  = len(f_data)
        f.close()
    else:
        print "Enter actual command"

def decodeFile(filename, offset=0, magic='bootsect'):
    import struct, binascii
    f = open(filename, 'rb')
    f_data = f.read()
    f_len  = len(f_data)
    if magic == 'bootsect':
      if f_len < 512:
        print "Read this many bytes: " + str(f_len)
      else:
        # dd bs=512 count=1 if=/dev/sda of=mbr.bkp
        t_data = f_data[0:3]
        print " Jump Instruction: " + t_data.encode('hex')
        #t_data = f_data[3:11]
        #print "           OEM ID: " + t_data.encode('hex')
        #t_data = binascii.b2a_uu(f_data[3:11])
        t_data = struct.unpack_from('8s', f_data[3:11])
        print "           OEM ID: " + t_data[0]
        t_data = f_data[11:36]
        print "              BPB: " + t_data.encode('hex')
        #values = struct.unpack('17d', f_data[ offset + 0 : offset + 8*17 ])
    elif magic == 'pe':
      if f_len < 4:
        print "Read this many bytes: " + str(f_len)
      else:
        t_data = f_data[ 0: 2]; t_data = t_data[::-1]; print "      Old DOS (MZ) Signature: " + t_data.encode('hex')
        t_data = f_data[ 2: 4]; t_data = t_data[::-1]; print "              Last Page Size: " + t_data.encode('hex')
        t_data = f_data[ 4: 6]; t_data = t_data[::-1]; print "         Total Pages in File: " + t_data.encode('hex')
        t_data = f_data[ 6: 8]; t_data = t_data[::-1]; print "            Relocation Items: " + t_data.encode('hex')
        t_data = f_data[ 8:10]; t_data = t_data[::-1]; print "        Paragraphs in Header: " + t_data.encode('hex')
        t_data = f_data[10:12]; t_data = t_data[::-1]; print "    Minimum Extra Paragraphs: " + t_data.encode('hex')
        t_data = f_data[12:14]; t_data = t_data[::-1]; print "    Maximum Extra Paragraphs: " + t_data.encode('hex')
        t_data = f_data[14:16]; t_data = t_data[::-1]; print "       Initial Stack Segment: " + t_data.encode('hex')
        t_data = f_data[16:18]; t_data = t_data[::-1]; print "       Initial Stack Pointer: " + t_data.encode('hex')
        t_data = f_data[18:20]; t_data = t_data[::-1]; print "       Complemented Checksum: " + t_data.encode('hex')
        t_data = f_data[20:22]; t_data = t_data[::-1]; print " Initial Instruction Pointer: " + t_data.encode('hex')
        t_data = f_data[22:24]; t_data = t_data[::-1]; print "        Initial Code Segment: " + t_data.encode('hex')
        t_data = f_data[24:26]; t_data = t_data[::-1]; print "     Relocation Table Offset: " + t_data.encode('hex')
        t_data = f_data[26:28]; t_data = t_data[::-1]; print "              Overlay Number: " + t_data.encode('hex')
        t_data = f_data[28:36]; t_data = t_data[::-1]; print "                    Reserved: " + t_data.encode('hex')
        t_data = f_data[36:44]; t_data = t_data[::-1]; print "                              " + t_data.encode('hex')
        t_data = f_data[44:52]; t_data = t_data[::-1]; print "                              " + t_data.encode('hex')
        t_data = f_data[52:60]; t_data = t_data[::-1]; print "                              " + t_data.encode('hex')
        t_data = f_data[60:64]; t_data = t_data[::-1]; print "   Offset to New (PE) Header: " + t_data.encode('hex')
    else:
      if f_len < 4:
        print "Read this many bytes: " + str(f_len)
      else:
        t_data = f_data[0:4]
        print " First 4 bytes is: " + t_data.encode('hex')
    f.close()

#########################################################################

