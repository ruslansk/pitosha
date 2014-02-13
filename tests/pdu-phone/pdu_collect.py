#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pdtool.fixes as fixes

#import pdtool
#import pdtool.dbsqc as sqtool
#from pdtool import dbsqc as sqtool

# warning: for set bluetooth PIN use command:
#   $> bluetooth-agent 0000 &

import cmd

class PduToolCmd(cmd.Cmd):
    """Simple command processor example."""

    FRIENDS  = [ 'Alice', 'Adam', 'Barbara', 'Bob' ]
    stor_cmd = [ 'priority', 'counts', 'setSM', 'setME', 'readSM', 'readME', 'readOneSM', 'readOneME' ]
    base_cmd = [ 'open', 'create', 'insert', 'select', 'sql', 'add', 'close' ]
    base_idx = None
    base_dbs = None

    prompt = 'pdutool#: '
    intro  = "Добро пожаловать в сборщик PDU :)\n"\
             "Для справки по доступным командам наберите: help\n"

    #def preloop(self):
    #    #print 'Welcome to DPU collector :)'
    #    print 'Добро пожаловать в сборщик PDU :)'
    #    print ''

    def do_storage(self, st_cmd):
        '''
          работа с системой хранения sms
              storage priority - показ приоритета чтения sms из хранилищ
              storage counts   - показ количества sms в хранилищах
              storage setSM    - установка SIM как текущего хранилища sms
              storage setME    - установка памяти телефона как текущего хранилища sms
        '''
        st_cmd_s = st_cmd.split(' ')
        st_cmd   = st_cmd_s[0]
        st_sub   = ''
        if len(st_cmd_s) > 1: st_sub = st_cmd_s[1]
        if st_cmd and st_cmd in self.stor_cmd:
            st_res = "Success"
            if   st_cmd == self.stor_cmd[0]:   # priority
                from pdtool import atsend as ats
                #if is_changed(ats): ats = reload(ats)
                reload(ats)
                ats.st_priority()
            elif st_cmd == self.stor_cmd[1]:   # counts
                from pdtool import atsend as ats
                #if is_changed(ats): ats = reload(ats)
                reload(ats)
                ats.st_counts()
            elif st_cmd == self.stor_cmd[2]:   # setSM
                from pdtool import atsend as ats
                #if is_changed(ats): ats = reload(ats)
                reload(ats)
                ats.st_setSM()
            elif st_cmd == self.stor_cmd[3]:   # setME
                from pdtool import atsend as ats
                #if is_changed(ats): ats = reload(ats)
                reload(ats)
                ats.st_setME()
            elif st_cmd == self.stor_cmd[4]:   # readSM
                from pdtool import atsend as ats
                #if is_changed(ats): ats = reload(ats)
                reload(ats)
                ats.st_readSM()
            elif st_cmd == self.stor_cmd[5]:   # readME
                from pdtool import atsend as ats
                #if is_changed(ats): ats = reload(ats)
                reload(ats)
                ats.st_readME()
            elif st_cmd == self.stor_cmd[6]:   # readOneSM
                from pdtool import atsend as ats
                #if is_changed(ats): ats = reload(ats)
                reload(ats)
                if st_sub:
                    ats.st_readOneFromSM(st_sub)
            else:                                 # readOneME
                from pdtool import atsend as ats
                #if is_changed(ats): ats = reload(ats)
                reload(ats)
                if st_sub:
                    ats.st_readOneFromME(st_sub)
        elif st_cmd:
            st_res = "Unknown storage command"
        else:
            st_res = 'Enter storage command'
        print st_res
    def complete_storage(self, text, line, begidx, endidx):
        if not text:
            completions = self.stor_cmd[:]
        else:
            completions = [ f
                            for f in self.stor_cmd
                            if f.startswith(text)
                          ]
        return completions

    def do_base(self, db_cmd):
        '''
          работа с base
              base open        -
              base create      -
              base insert      -
              base select      -
              base sql         -
              base add         -
              base close       -
        '''
        db_cmd_s = db_cmd.split(' ')
        db_cmd   = db_cmd_s[0]
        db_sub   = ''
        if len(db_cmd_s) > 1: db_sub = db_cmd_s[1]
        if db_cmd and db_cmd in self.base_cmd:
            db_res = "Success\n\n"
            if   db_cmd == self.base_cmd[0]:   # open
                from pdtool import dbsqc as dbs
                ##if is_changed(dbs): dbs = reload(dbs)
                #reload(dbs)
                if self.base_idx is True: reload(dbs)
                self.base_dbs = dbs
                self.base_idx = True
            elif db_cmd == self.base_cmd[1]:   # create
                #if is_changed(dbs): dbs = reload(dbs)
                self.base_dbs.createT()
            elif db_cmd == self.base_cmd[2]:   # insert
                #if is_changed(dbs): dbs = reload(dbs)
                #self.base_dbs.insertT('devName', 'dateAdd', 'pduBlob')
                self.base_dbs.insertT('devMTK_1', '11 feb', "394874jkfgfksh895419593451")
            elif db_cmd == self.base_cmd[3]:   # select
                #if is_changed(dbs): dbs = reload(dbs)
                if db_sub:
                    self.base_dbs.selectOne(db_sub)
                else:
                    self.base_dbs.selectAll()
            elif db_cmd == self.base_cmd[4]:   # sql
                #if is_changed(dbs): dbs = reload(dbs)
                a = 1
            elif db_cmd == self.base_cmd[5]:   # add
                from pdtool import parse as par
                if db_sub:
                    par.parseFile(db_sub)
                else:
                    par.parseFile('temp.bkp')
            else:                              # close
                #from pdtool import dbsqc as dbs
                ##if is_changed(dbs): dbs = reload(dbs)
                #reload(dbs)
                self.base_idx = False
        elif db_cmd:
            db_res = "Unknown storage command\n\n"
        else:
            db_res = 'Enter storage command\n\n'
        print db_res
    def complete_base(self, text, line, begidx, endidx):
        if not text:
            completions = self.base_cmd[:]
        else:
            completions = [ f
                            for f in self.base_cmd
                            if f.startswith(text)
                          ]
        return completions
		
    def do_greet(self, person):
        if person and person in self.FRIENDS:
            greeting = 'hi, %s!' % person
        elif person:
            greeting = "hello, " + person
        else:
            greeting = 'hello'
        print greeting
    def help_greet(self):
        print '\n'.join([ 'greet [person]',
                          'Greet the named person',
                        ])
    def complete_greet(self, text, line, begidx, endidx):
        if not text:
            completions = self.FRIENDS[:]
        else:
            completions = [ f
                            for f in self.FRIENDS
                            if f.startswith(text)
                          ]
        return completions

    def do_cmps(self, line):
        "  cmps - get CMPS"
        from pdtool import atsend as ats
        #if is_changed(ats): ats = reload(ats)
        reload(ats)
        ats.getCMPS()
    
    def do_EOF(self, line):   # Ctrl-D, ^D$
        return True
    def do_exit(self, line):
        return True
    def do_e(self, line):
        return True
    def do_quit(self, line):
        return True
    def do_q(self, line):
        "  q, quit, e, exit - Выход из программы\n"
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

