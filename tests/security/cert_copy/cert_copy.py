#!/usr/bin/env python
# -*- coding: utf-8 -*-

#######################################################################

import cmd

class CertToolCmd(cmd.Cmd):
    """Simple command processor example."""

    prompt = 'cert_tool #: '
    #intro  = "Добро пожаловать в программу копирования сертификатов\n"\
    #         "Для справки по доступным командам наберите: help\n"

    def preloop(self):
        #print 'Welcome to DPU collector :)'
        print ''
        print 'Добро пожаловать в программу копирования сертификатов'.decode("utf-8")
        self.do_readme(None)

    def do_readme(self, line):
        print ''
        print 'Выберите действие:'.decode("utf-8")
        print ''
        print '  1. export - Экспорт контейнеров и ключей'.decode("utf-8")
        print '  2. import - Импорт контейнеров и ключей'.decode("utf-8")
        print '  --------------------------------------------'
        print '  0. quit   - Выход из программы'.decode("utf-8")
        print ''

    #def do_greet(self, person):
    #    if person and person in self.FRIENDS:
    #        greeting = 'hi, %s!' % person
    #    elif person:
    #        greeting = "hello, " + person
    #    else:
    #        greeting = 'hello'
    #    print greeting
    #def help_greet(self):
    #    print '\n'.join([ 'greet [person]',
    #                      'Greet the named person',
    #                    ])
    #def complete_greet(self, text, line, begidx, endidx):
    #    if not text:
    #        completions = self.FRIENDS[:]
    #    else:
    #        completions = [ f
    #                        for f in self.FRIENDS
    #                        if f.startswith(text)
    #                      ]
    #    return completions

    def do_export(self, exp_cmd):
        "  export - Экспорт контейнеров и ключей\n".decode("utf-8")
        import sys
        term_enc = sys.stdout.encoding
        print term_enc
        import capi	
        capi.cryptopro.ListContainers(term_enc)
        self.do_readme(None)

    def do_import(self, imp_cmd):
        "  import - Импорт контейнеров и ключей\n".decode("utf-8")
        import sys
        term_enc = sys.stdout.encoding
        print term_enc
        import capi	
        capi.cryptopro.ListContainers(term_enc)
        self.do_readme(None)

    def do_1(self, line):
        print "Экспорт".decode("utf-8") # print "".decode("utf-8")  - if file as UTF-8 !!!
        self.do_export(line)

    def do_2(self, line):
        print "Импорт".decode("utf-8")
        self.do_import(line)

    def do_0(self, line):
        return True

    def do_h(self, line):
        self.do_help(line)

    def do_EOF(self, line):   # Ctrl-D, ^D$
        return True
    def do_exit(self, line):
        return True
    def do_e(self, line):
        return True
    def do_quit(self, line):
        return True
    def do_q(self, line):
        "  q, quit, e, exit - Выход из программы\n".decode("utf-8")
        return True

    def postloop(self):
        #print "Bye!"
        print ''
        print 'Хорошего дня!'.decode("utf-8")

if __name__ == '__main__':
    CertToolCmd().cmdloop()

exit()

#######################################################################

# http://code.activestate.com/recipes/66011-reading-from-and-writing-to-the-windows-registry/
from _winreg import *

print ""

def RegManipulate():
    print r"*** Reading from SOFTWARE\Microsoft\Windows\CurrentVersion\Run ***"
    aReg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    
    aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run") 
    for i in range(1024):                                           
        try:
            n,v,t = EnumValue(aKey,i)
            print i, n, v, t
        except EnvironmentError:                                               
            print "You have",i," tasks starting at logon..."
            break          
    CloseKey(aKey)
    
    #print r"*** Writing to SOFTWARE\Microsoft\Windows\CurrentVersion\Run ***"
    #aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
    #try:   
    #   SetValueEx(aKey,"MyNewKey",0, REG_SZ, r"c:\winnt\explorer.exe") 
    #except EnvironmentError:                                          
    #    print "Encountered problems writing into the Registry..."
    #CloseKey(aKey)
    #CloseKey(aReg)  

# https://mail.python.org/pipermail/python-win32/2012-September/012541.html
#!/usr/bin/env python
'''This module contains the user() and home() functions that
return the current user's name on Windows, and the given or
current user's home directory on Windows (even if it's been
changed in the registry).
20120911 raf <raf at raf.org>'''
import win32api, win32net, win32netcon, win32security, _winreg, pywintypes
def user(has_domain_controller=True):
    '''Return the current user's name on Windows. If has_domain_controller
    is True when you have no domain controller there may (or may not) be an
    annoying delay so pass False unless you really have a domain controller.'''
    dcname = None
    if has_domain_controller:
        try:
            dctype = win32netcon.SV_TYPE_DOMAIN_CTRL
            dcinfo = win32net.NetServerEnum(None, 100, dctype)
            dcname = r'\\' + dcinfo[0][0]['name']
        except (pywintypes.error, IndexError, KeyError):
            pass
    return win32net.NetUserGetInfo(dcname, win32api.GetUserName(), 1)['name']
def home(username=None, has_domain_controller=True):
    '''Return the given or current user's home directory on Windows
    even if it's been changed it in the registry. If has_domain_controller
    is True when you have no domain controller there may (or may not) be an
    annoying delay so pass False unless you really have a domain controller.'''
    if username is None:
        username = user(has_domain_controller)
    lookup_username = username
    hostname = win32api.GetComputerName()
    if '\\' not in lookup_username:
        lookup_username = hostname + '\\' + lookup_username
    sid = win32security.LookupAccountName(None, lookup_username)[0]
    sid = win32security.ConvertSidToStringSid(sid)
    key = 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\' + sid
    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key)
    val, typ = _winreg.QueryValueEx(key, 'ProfileImagePath')
    if typ == _winreg.REG_EXPAND_SZ: # Which it is
        val = win32api.ExpandEnvironmentStrings(val) # Doesn't return unicode
    return val
def user_sid(username=None, has_domain_controller=True):
    '''Return the given or current user's home directory on Windows
    even if it's been changed it in the registry. If has_domain_controller
    is True when you have no domain controller there may (or may not) be an
    annoying delay so pass False unless you really have a domain controller.'''
    if username is None:
        username = user(has_domain_controller)
    lookup_username = username
    hostname = win32api.GetComputerName()
    if '\\' not in lookup_username:
        lookup_username = hostname + '\\' + lookup_username
    sid = win32security.LookupAccountName(None, lookup_username)[0]
    sid = win32security.ConvertSidToStringSid(sid)
    return sid
#if __name__ == '__main__':
#    print('user = %r' % user())
#    print('user_sid = %r' % user_sid())
#    print('home = %r' % home())

def AnyManipulate():
    #--------
    print ""
    
    # http://python.6.x6.nabble.com/How-do-I-detect-a-64-bit-version-of-Windows-td4483507.html
    import platform 
    print "platform.machine: " + platform.machine()
    print "platform.architecture: " + str(platform.architecture())
    import win32process
    isWow64 = win32process.IsWow64Process()
    print "IsWow64Process: " + str(isWow64)
    
    usrn = user()
    pkey = home() + "\\Application Data\\Microsoft\\SystemCertificates\\My\\Certificates\\"
    print('current user: %r\nprivate key folder is: %r' % (usrn,pkey))
    cont = None
    if isWow64:
      cont = "HKLM\\SOFTWARE\\Wow6432Node\\Crypto Pro\\Settings\\Users\\" + user_sid() + "\\Keys\\"
    else:
      cont = "HKLM\\SOFTWARE\\Crypto Pro\\Settings\\Users\\" + user_sid() + "\\Keys\\"
    print('regkey CryptoPro containers in REGISTRY: %r' % cont)
    
    # http://stackoverflow.com/questions/2374331/python-win32crypt-cryptprotectdata-difference-between-2-5-and-3-1
    import win32crypt
    import win32security
    print ""
    #print " - CryptEnumProviderTypes:"
    #for i in win32security.CryptEnumProviderTypes():
    #    print i
    print " - CryptEnumProviders: "
    for i in win32security.CryptEnumProviders():
        print i
    
    import capi	
    print ""
    idx = 0
    while True:
        n = capi.AdvEnumCSP(idx)
        if n == None:
            print "CSP count: " + str(idx)
            break
        print n
        idx += 1
    
    idx = 5
    while True:
        n = capi.advapi32.CryptEnumProvidersA(idx)
        if n == None:
            print "CSP count: " + str(idx)
            break
        print n
        idx += 1
    
    idx = 0
    while True:
        n = capi.advapi32.CryptEnumProviderTypes(idx)
        if n == None:
            print "CSPTypes count: " + str(idx)
            break
        print n
        idx += 1

import sys
term_enc = sys.stdout.encoding
#print term_enc
import capi	
capi.cryptopro.ListContainers(term_enc)

# -- The End --
print ""
print ""
