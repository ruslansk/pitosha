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
    #sql = 'CREATE TABLE pdu_data ('       +\
    sql = 'CREATE TABLE IF NOT EXISTS pdu_data ('       \
                      ' id       INTEGER PRIMARY KEY, ' \
                      ' dev_name VARCHAR(100), '        \
                      ' date_add VARCHAR(30),  '        \
                      ' pdu_blob VARCHAR(500)) '
    cur.execute(sql)
    conn.commit()

def insertT(devName, dateAdd, pduBlob):
    global conn, cur
    cur.execute('INSERT INTO pdu_data VALUES (null, ?, ?, ?)', (devName, dateAdd, pduBlob))
    conn.commit()

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

