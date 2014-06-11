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
#LPDWORD = ctypes.POINTER(DWORD)
LPDWORD = PDWORD = ctypes.POINTER(DWORD)
LPTSTR  = ctypes.c_char_p # Map Microsoft LPTSTR to a pointer to a string
LPBYTE  = POINTER(c_ubyte)
#LPTSTR  = POINTER(c_char)
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

#nDll = ctypes.WinDLL('ndll.dll')
#nDll.restype = ctypes.c_double
#nDll.argtypes = [ctypes.c_char_p]
#result = nDll.iptouint("12.345.67.890").value

#if 'unicode' in wx.PlatformInfo:
#  SHGetFolderPath = ctypes.windll.shell32.SHGetFolderPathW
#  LPTSTR = wintypes.LPWSTR
#  pszPath = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
#else:
#  SHGetFolderPath = ctypes.windll.shell32.SHGetFolderPathA
#  LPTSTR = wintypes.LPSTR
#  pszPath = ctypes.create_string_buffer(wintypes.MAX_PATH)

from ctypes import wintypes
advDll          =  ctypes.WinDLL('advapi32.dll')
advDll.CryptEnumProvidersA.restype  =  wintypes.BOOL
advDll.CryptEnumProvidersA.argtypes = [wintypes.DWORD, 
                                       LPDWORD,
                                       wintypes.DWORD,
                                       LPDWORD,
                                       LPTSTR,
                                       LPDWORD]
idx = 0
dwIndex      = wintypes.DWORD(idx)
#dwReserved   = ctypes.c_ulong(0)
pdwReserved  = LPDWORD() #LPDWORD(ctypes.c_ulong(0))
dwFlags      = wintypes.DWORD(0)
dwProvType   = wintypes.DWORD(0)
#pdwProvType =
#szProvName  = 
pszProvName  = ctypes.c_char_p(0) # ctypes.c_void_p
cbProvName   = wintypes.DWORD(0)
#pcbProvName =
print 'error code = {}'.format(windll.kernel32.GetLastError())
result          =  advDll.CryptEnumProvidersA(dwIndex,
                                              pdwReserved,
                                              dwFlags,
                                              ctypes.byref(dwProvType),
                                              pszProvName,
                                              ctypes.byref(cbProvName) \
                                              )#.value
print "result1: " + str(result)
if not result:
    raise RuntimeError('error code = {}'.format(windll.kernel32.GetLastError()))
print "cbProvName: " + str(cbProvName)
#idx += 1
#dwIndex      = wintypes.DWORD(idx)
pszProvName  = ctypes.create_string_buffer(wintypes.MAX_PATH)
result          =  advDll.CryptEnumProvidersA(dwIndex,
                                              pdwReserved,
                                              dwFlags,
                                              ctypes.byref(dwProvType),
                                              pszProvName,
                                              ctypes.byref(cbProvName)
                                              )#.value
print "result2: " + str(result)
print "pszProvName: " + str(pszProvName.value)
#BOOL WINAPI CryptEnumProviders(
#  _In_     DWORD dwIndex,
#  _In_     DWORD *pdwReserved,
#  _In_     DWORD dwFlags,
#  _Out_    DWORD *pdwProvType,
#  _Out_    LPTSTR pszProvName,
#  _Inout_  DWORD *pcbProvName
#);

print "CryptEnumProvidersA: " + hex(windll.advapi32.CryptEnumProvidersA(None))
#print "CryptEnumProvidersA: " + hex(windll.advapi32.CryptEnumProvidersW(None))
print hex(windll.kernel32.GetModuleHandleA(None))
msvcrt = cdll.msvcrt
message = 'Hello world!\n'
msvcrt.printf('Testing: %s', message)
#windll.msvcrt.printf("spam")
#hllApi = hllApiProto (("CryptEnumProvidersW", advapi), hllApiParams)

# This is how you can actually call the DLL function.
# Set up the variables and call the Python name with them.
#
#p1 = ctypes.c_int (1)
#p2 = ctypes.c_char_p (sessionVar)
#p3 = ctypes.c_int (1)
#p4 = ctypes.c_int (0)
#hllApi (ctypes.byref (p1), p2, ctypes.byref (p3), ctypes.byref (p4))

pp2 = ctypes.c_ulong (0)
p1 = ctypes.wintypes.DWORD (0)
p2 = LPDWORD (pp2)
p3 = ctypes.wintypes.DWORD (0)
p4 = ctypes.c_char_p ("0")
p5 = ctypes.c_int (0)
p6 = ctypes.c_char_p ("0")
hllApi (p1, p2, p3, ctypes.byref (p4), ctypes.byref (p5), ctypes.byref (p6))
