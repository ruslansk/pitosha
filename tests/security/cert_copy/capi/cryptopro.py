# -*- coding: utf-8 -*-

from   _winreg import *
import _winreg
import userenv

def copyDirectory(src, dest):
    import shutil
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

def copy(src, dest):
    import shutil
    import errno
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            print('Directory not copied. Error: %s' % str(e).decode("cp1251"))

def ListContainers(term_enc='cp866', debug=0):
    areg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    
    usrn = userenv.user()
    pkey = userenv.home() + "\\Application Data\\Microsoft\\SystemCertificates\\My\\Certificates\\"
    if debug:
        print('current user: %r\nprivate key folder is: %r' % (usrn,pkey))
    cont = None
    # "HKLM\\SOFTWARE\\Wow6432Node\\Crypto Pro\\Settings\\Users\\" + userenv.user_sid() + "\\Keys\\"
    if userenv.isWow64():
      cont = "SOFTWARE\\Wow6432Node\\Crypto Pro\\Settings\\Users\\" + userenv.user_sid() + "\\Keys\\"
    else:
      cont = "SOFTWARE\\Crypto Pro\\Settings\\Users\\" + userenv.user_sid() + "\\Keys\\"
    if debug:
        print('regkey CryptoPro containers in REGISTRY: %r' % cont)
    
    #akey = OpenKey(areg, cont)
    akey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, cont)
    print ""
    print "—ледующие контейнеры наход€тс€ в реестре текущего пользовател€:".decode("cp1251")
    count = 0
    try:
      i = 0
      while True:
          subkey = EnumKey(akey, i)
          #print subkey.decode(term_enc)
          #print subkey.encode(term_enc, 'ignore')
          print str(i) + ". " + subkey.decode("cp1251")  # chcp 866
          #print subkey.decode("utf-8")
          i += 1
          
    except WindowsError:
        pass
    
    print ""
    print "ѕеречислите номера контейнеров (через пробел или зап€тую)".decode("cp1251")
    print "дл€ экспорта из реестра".decode("cp1251"), 
    haba = raw_input(": ")
    #print haba
    haba = haba.strip()
    haba = haba.replace('.', ' ')
    haba = haba.replace(',', ' ')
    haba = haba.replace('  ', ' ')
    #print haba
    haba = haba.split(' ')
    #print haba
    print ""
    print "Ёкспорт...".decode("cp1251")
    print ""
    
    import os
    directory = "containers"
    if not os.path.exists(directory):
        os.makedirs(directory)
    dir_keys  = directory + "\cryptopro.key"
    if os.path.exists(dir_keys):
        import shutil
        shutil.rmtree(dir_keys)
    os.makedirs(dir_keys)
    #copy(pkey, dir_keys + '\\')
    import distutils.core
    # copy subdirectory example
    fromDirectory = pkey
    toDirectory = dir_keys
    distutils.dir_util.copy_tree(fromDirectory, toDirectory)
    #-
    f = open(directory + '\\cryptopro.cnt','w')
    for k in haba:
        #print str(int(k))
        
        akey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, cont)
        try:
            subkey = EnumKey(akey, int(k))
            print str(int(k)) + ". " + subkey.decode("cp1251") + " : OK" # chcp 866
            f.write('[' + subkey + ']\n')
            
            cnt2 = cont + "\\" + subkey.decode("cp1251")
            bkey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, cnt2.encode("cp1251"), 0, KEY_ALL_ACCESS)
            j = 0
            try:
              while True:
                name, value, type = EnumValue(bkey, j)
                #print repr(name),
                #print value.encode("hex")
                f.write(name + '=' + value.encode("hex") + '\n') # python will convert \n to os.linesep
                j += 1
            except WindowsError:
                # WindowsError: [Errno 259] No more data is available    
                pass
        except WindowsError:
            pass
    
    print ""
    print "экспорт выполнен успешно!".decode("cp1251")
    f.close() # you can omit in most cases as the destructor will call if
    return None
