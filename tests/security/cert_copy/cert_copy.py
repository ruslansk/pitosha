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
print "IsWow64Process: " + str(win32process.IsWow64Process())

usrn = user()
pkey = home() + "\\Application Data\\Microsoft\\SystemCertificates\\My\\Certificates\\"
print('current user: %r\nprivate key folder is: %r' % (usrn,pkey))
cont = "HKLM\\SOFTWARE\\Wow6432Node\\Crypto Pro\\Settings\\Users\\" + user_sid() + "\\Keys\\"
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

# http://www.xjump.me/content.htm?id=44
#from OpenSSL.crypto import *
#from M2Crypto import Engine, m2, X509
import os
cwd = os.getcwd()
#def test_capi():
#    e = Engine.load_dynamic_engine("capi", os.path.join(cwd, "capi.dll"))
#    capi = Engine.Engine("capi")
#    m2.engine_init(m2.engine_by_id("capi"))
#    capi.ctrl_cmd_string("list_csps",None)
#    #capi.ctrl_cmd_string("csp_name", "Infotecs Cryptographic Service Provider")
#    #capi.ctrl_cmd_string("csp_name", "Infotecs RSA/GOST Cryptographic Service Provider")
#    capi.ctrl_cmd_string("csp_name", "Crypto-Pro GOST R 34.10-2001 Cryptographic Service Provider")
#    b = None
#    capi.ctrl_cmd_string("list_containers", b)
#    print b
#    capi.ctrl_cmd_string("list_certs",None)
#    capi.finish()

#test_capi()
# http://thomascannon.net/public/files/certexport.pdf
# http://osdir.com/ml/python.ctypes/2003-07/msg00091.html
from ctypes import *
from ctypes.wintypes import DWORD

LocalFree = windll.kernel32.LocalFree
# Note that CopyMemory is defined in term of memcpy:
memcpy = cdll.msvcrt.memcpy
CryptProtectData = windll.crypt32.CryptProtectData
CryptUnprotectData = windll.crypt32.CryptUnprotectData

# See http://msdn.microsoft.com/architecture/application/default.aspx?pull=/library/en-us/dnnetsec/html/SecNetHT07.asp 
CRYPTPROTECT_UI_FORBIDDEN = 0x01

class DATA_BLOB(Structure):
  # See d:\vc98\Include\WINCRYPT.H
  # This will not work
  # _fields_ = [("cbData", DWORD), ("pbData", c_char_p)]
  # because accessing pbData will create a new Python string which is
  # null terminated.
  _fields_ = [("cbData", DWORD), ("pbData", POINTER(c_char))]

def getData(blobOut):
  cbData = int(blobOut.cbData)
  print "cbData(%d)" % blobOut.cbData
  pbData = blobOut.pbData
  buffer = c_buffer(cbData)
  memcpy(buffer, pbData, cbData)
  LocalFree(pbData);
  return buffer.raw

def Win32CryptProtectData(plainText, entropy):
  bufferIn = c_buffer(plainText, len(plainText))
  blobIn = DATA_BLOB(len(plainText), bufferIn)
  bufferEntropy = c_buffer(entropy, len(entropy))
  blobEntropy = DATA_BLOB(len(entropy), bufferEntropy)
  blobOut = DATA_BLOB()
  print "%s %s" % (blobOut.cbData, blobOut.pbData)
  # The CryptProtectData function performs encryption on the data
  # in a DATA_BLOB structure.
  # BOOL WINAPI CryptProtectData(
  # DATA_BLOB* pDataIn,
  # LPCWSTR szDataDescr,
  # DATA_BLOB* pOptionalEntropy,
  # PVOID pvReserved,
  # CRYPTPROTECT_PROMPTSTRUCT* pPromptStruct,
  # DWORD dwFlags,
  # DATA_BLOB* pDataOut
  if CryptProtectData(byref(blobIn), u"win32crypto.py", byref(blobEntropy), None, None, CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
    return getData(blobOut)
  else:
    return None

print ""
print "sizeof(DATA_BLOB): %d" % sizeof(DATA_BLOB)
# Note that the plain text can include NULL
testPlainText = "Just testing \0some stuff"
extraEntropy = "cl;ad13 \0al;323kjd #(adl;k$#ajsd"
cipherText = Win32CryptProtectData(testPlainText, extraEntropy)
print "cipherText(%s) cipherTextLen(%d)" % (cipherText, len(cipherText))

#CryptEnumProviders = windll.advapi32.CryptEnumProviders

# http://stackoverflow.com/questions/252417/how-can-i-use-a-dll-from-python
import ctypes
# Load DLL into memory.
advapi = ctypes.WinDLL ("advapi32.dll")
# Set up prototype and parameters for the desired function call.
# HLLAPI
#hllApiProto = ctypes.WINFUNCTYPE (ctypes.c_int,ctypes.c_void_p,
#    ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)
#hllApiParams = (1, "p1", 0), (1, "p2", 0), (1, "p3",0), (1, "p4",0),
LPDWORD = ctypes.POINTER(DWORD)
LPTSTR = ctypes.c_char_p # Map Microsoft LPTSTR to a pointer to a string
hllApiProto = ctypes.WINFUNCTYPE (ctypes.wintypes.DWORD, 
                                  LPDWORD,
                                  ctypes.wintypes.DWORD, 
                                  LPDWORD,
                                  LPTSTR,
                                  ctypes.wintypes.DWORD,
                                  ctypes.wintypes.BOOLEAN)
hllApiParams = (1, "p1", 0), (1, "p2", 0), (1, "p3",0), (1, "p4",0), (1, "p5",0), (1, "p6",0),
# Actually map the call ("CryptEnumProviders(...)") to a Python name.
hllApi = hllApiProto (("CryptEnumProvidersA", advapi), hllApiParams)
#hllApi = hllApiProto (("CryptEnumProvidersW", advapi), hllApiParams)

# This is how you can actually call the DLL function.
# Set up the variables and call the Python name with them.
#
#p1 = ctypes.c_int (1)
#p2 = ctypes.c_char_p (sessionVar)
#p3 = ctypes.c_int (1)
#p4 = ctypes.c_int (0)
#hllApi (ctypes.byref (p1), p2, ctypes.byref (p3), ctypes.byref (p4))

#pp2 = ctypes.c_ulong (0)
#p1 = ctypes.wintypes.DWORD (0)
#p2 = LPDWORD (pp2)
#p3 = ctypes.wintypes.DWORD (0)
#p4 = ctypes.c_char_p ("0")
#p5 = ctypes.c_int (0)
#p6 = ctypes.c_char_p ("0")
#hllApi (p1, p2, p3, ctypes.byref (p4), ctypes.byref (p5), ctypes.byref (p6))
#BOOL WINAPI CryptEnumProviders(
#  _In_     DWORD dwIndex,        - 1
#  _In_     DWORD *pdwReserved,   - 2
#  _In_     DWORD dwFlags,        - 3
#  _Out_    DWORD *pdwProvType,   - 4
#  _Out_    LPTSTR pszProvName,   - 5
#  _Inout_  DWORD *pcbProvName    - 6
#);

# -- The End --
print ""
print ""
