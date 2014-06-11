# http://code.activestate.com/recipes/66011-reading-from-and-writing-to-the-windows-registry/
from _winreg import *

print ""
print ""
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
if __name__ == '__main__':
    print('user = %r' % user())
    print('user_sid = %r' % user_sid())
    print('home = %r' % home())

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
print capi.AdvEnumCSP(0)
print capi.AdvEnumCSP(1)
print capi.AdvEnumCSP(2)
print capi.AdvEnumCSP(3)
print capi.AdvEnumCSP(4)

# -- The End --
print ""
print ""
