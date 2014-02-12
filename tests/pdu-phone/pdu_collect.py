#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pdtool.fixes as fixes

# warning: for set bluetooth PIN use command:
#   $> bluetooth-agent 0000 &

import cmd

class PduToolCmd(cmd.Cmd):
    """Simple command processor example."""

    FRIENDS  = [ 'Alice', 'Adam', 'Barbara', 'Bob' ]
    stor_cmd = [ 'priority', 'counts', 'setSM', 'setME' ]

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
            else:                              # setME
                from pdtool import atsend as ats
                #if is_changed(ats): ats = reload(ats)
                reload(ats)
                ats.st_setME()
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

#import pdtool
#import pdtool.dbsqc as sqtool
#from pdtool import dbsqc as sqtool

#def spyder_getpass(prompt='Password: '):
#  set_spyder_echo(False)
#  password = raw_input(prompt)
#  set_spyder_echo(True)
#  return password
#
#print "Oops! Ha-ha! :) Your password is: " + spyder_getpass()

#import getpass
#import sys
#
#ppp = getpass.getpass(stream=sys.stderr,              # где ты была сегодня киска?
#                      prompt='Wath? ')

