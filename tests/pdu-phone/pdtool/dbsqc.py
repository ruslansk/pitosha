#!/usr/bin/env python
# -*- coding: utf-8 -*-

##  import pysqlcipher.dbapi2 as sqlite
##  >>> sqlite.version
##  '2.6.3'
##  >>> sqlite.sqlite_version
##  '3.7.14.1'

##def spyder_getpass(prompt='Password: '):
##  set_spyder_echo(False)
##  password = raw_input(prompt)
##  set_spyder_echo(True)
##  return password
##
##print "Oops! Ha-ha! :) Your password is: " + spyder_getpass()
##
##import getpass
##import sys
##
##ppp = getpass.getpass(stream=sys.stderr,              # где ты была сегодня киска?
##                      prompt='Wath? ')

import sys
import getpass
import pysqlcipher.dbapi2 as sqc3
print "lib ver.: " + sqc3.version
print "sql ver.: " + sqc3.sqlite_version

conn=sqc3.connect('bdata.db')
cur = conn.cursor()
ppp = getpass.getpass(stream=sys.stderr,              # где ты была сегодня киска?
                      prompt='Wath? ')
cur.execute("PRAGMA key='" + ppp + "'")
ppp = 'ihlwgkjglbo47r2498rt234807ryiwhfgsdfkgaskegf'

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
    #sql = 'DROP TABLE IF EXISTS pdu_data'
    #cur.execute(sql)
    #conn.commit()
    ##sql = 'CREATE TABLE pdu_data ('       +\
    #sql = 'CREATE TABLE IF NOT EXISTS pdu_data ('       \
    #                  ' id       INTEGER PRIMARY KEY, ' \
    #                  ' dev_name VARCHAR(100), '        \
    #                  ' date_add VARCHAR(30),  '        \
    #                  ' pdu_blob VARCHAR(500)) '
    #cur.execute(sql)
    #conn.commit()
    #sql = 'DROP TABLE IF EXISTS raw_data'
    #cur.execute(sql)
    #conn.commit()
    #sql = 'CREATE TABLE IF NOT EXISTS raw_data ( '      \
    #                  ' id       INTEGER PRIMARY KEY, ' \
    #                  ' file     VARCHAR(256), ' \
    #                  ' comment  VARCHAR(50),' \
    #                  ' data     BLOB)'
    #cur.execute(sql)
    #conn.commit()
    sql = 'CREATE TABLE IF NOT EXISTS sms_data ( '      \
                      ' id       INTEGER PRIMARY KEY, ' \
                      ' comment  VARCHAR(50),  ' \
                      ' txt_md5  VARCHAR(64),  ' \
                      ' pdu_txt  VARCHAR(500), ' \
                      ' bin_md5  VARCHAR(64),  ' \
                      ' pdu_bin  BLOB)'
    cur.execute(sql)
    conn.commit()

def sqlEx(txt):
    global conn, cur
    print "Execute: " + txt
    cur.execute(txt)
    r = cur.fetchone()
    print r.keys()
    for row in cur:
        print row[0]

def insertSMS(pdu_txt=None, pdu_bin=None, pdu_dtm=None):
    global conn, cur
    if   pdu_txt and pdu_bin:
      if pdu_txt is not pdu_bin.encode("hex"):
        print "pdu_txt and pdu_bin is not equal!"
        return
    elif pdu_txt:
      pdu_bin = pdu_txt.decode("hex")
    elif pdu_bin:
      pdu_txt = pdu_bin.encode("hex")
    else:
        print "pdu_txt and pdu_bin not set!"
        return
    import hashlib
    #str_h = 'My hesh'
    str_h = pdu_txt
    hsh = hashlib.md5()
    hsh.update(str_h)
    txt_md5 = hsh.hexdigest()
    str_h = pdu_bin
    hsh = hashlib.md5()
    hsh.update(str_h)
    bin_md5 = hsh.hexdigest()
    cur.execute('INSERT INTO sms_data (comment, pdu_txt, txt_md5, pdu_bin, bin_md5) VALUES("comment", ?, ?, ?, ?)', \
                [pdu_txt, txt_md5, sqc3.Binary(pdu_bin), bin_md5])
    conn.commit()

def insertTT(txt, idx):
    global conn, cur
    #txt = "2_MPA3_001.bkp"
    print "Inserting: " + txt
    with open(txt, "rb") as input_file:
        ablob = input_file.read()
        cur.execute('INSERT INTO raw_data (id, file, comment, data) VALUES(' + str(idx) + ', ?, "comment", ?)', \
                    [txt, sqc3.Binary(ablob)])
        conn.commit()
    #with open("output.bkp", "wb") as output_file:
    #    cur.execute("SELECT data FROM raw_data WHERE id = 1")
    #    ablob = cur.fetchone()
    #    output_file.write(ablob[0])

def extractTT(idx):
    global conn, cur
    cur.execute("SELECT data FROM raw_data WHERE id = " + str(idx))
    ablob = cur.fetchone()
    return ablob[0]

def insertT(devName, dateAdd, pduBlob):
    global conn, cur
    #cur.execute('INSERT INTO pdu_data VALUES (null, ?, ?, ?)', (devName, dateAdd, pduBlob))
    #conn.commit()
    #  0 - 1_MPA3_001.bkp
    #  1 - 2_MPA3_001.bkp
    #insertTT('1_MP0C_004.bkp', 2)
    #insertTT('1_MP84_002.bkp', 3)
    #insertTT('1_MPD1_001.bkp', 4)
    #insertTT('1_MP0H_007.bkp', 5)
    #insertTT('2_MP0C_004.bkp', 6)
    #insertTT('2_MPD1_001.bkp', 7)

def selectAll():
    global conn, cur
    cur.execute('SELECT * FROM pdu_data')
    for row in cur:
        print '-'*70
        print '     ID: ', row[0]
        print 'DevName: ', row[1]
        print 'DateAdd: ', row[2]
        print 'PduBlob: ', row[3]
    print '-'*70

def selectOne(idx):
    global conn, cur
    cur.execute('SELECT * FROM pdu_data pd WHERE pd.id=' + str(idx))
    for row in cur:
        print '-'*70
        print '     ID: ', row[0]
        print 'DevName: ', row[1]
        print 'DateAdd: ', row[2]
        print 'PduBlob: ', row[3]
    print '-'*70

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

'''
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
    selectAll()
    #selectOne(1)

#    input_file = open(sys.argv[1])
#    while True:
#        put_DUNtext()
#        sys.stdout.write("any? (Y/n): ")
#        c = getch()
#        print ""
#        if c.upper() == 'N': break

#except sqc3.Error, e:
#    print "Error %s:" % e.args[0]
#    sys.exit(1)
finally:
    if conn:
        conn.close()

#cur.close()
#conn.close()

exit()

'''

