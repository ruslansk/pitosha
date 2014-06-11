import ctypes
from ctypes import *
from ctypes import wintypes
from ctypes.wintypes import DWORD

LPDWORD = PDWORD = ctypes.POINTER(DWORD)
LPTSTR  = ctypes.c_char_p # Map Microsoft LPTSTR to a pointer to a string

def CryptEnumProvidersA(idx=0, debug=0):
    advDll          =  ctypes.WinDLL('advapi32.dll')
    advDll.CryptEnumProvidersA.restype  =  wintypes.BOOL
    advDll.CryptEnumProvidersA.argtypes = [wintypes.DWORD, 
                                           LPDWORD,
                                           wintypes.DWORD,
                                           LPDWORD,
                                           LPTSTR,
                                           LPDWORD]
    #idx = 0
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
    if debug:
        print 'error code = {}'.format(windll.kernel32.GetLastError())
    result          =  advDll.CryptEnumProvidersA(dwIndex,
                                                  pdwReserved,
                                                  dwFlags,
                                                  ctypes.byref(dwProvType),
                                                  pszProvName,
                                                  ctypes.byref(cbProvName) \
                                                  )#.value
    if debug:
        print "result1: " + str(result)
    if not result:
        return None
        #raise RuntimeError('error code = {}'.format(windll.kernel32.GetLastError()))
    if debug:
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
    if debug:
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
    if result:
        return str(pszProvName.value)
    else:
        return None
