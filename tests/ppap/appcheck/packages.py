def chkpkg():
    print "hello chkpkg"

def downpack():
    import urllib2
    
    url = "https://pypi.python.org/packages/source/p/pyserial/pyserial-2.7.tar.gz#md5=794506184df83ef2290de0d18803dd11"
    
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    #file_name = int(meta.getheaders("Content-Disposition")[0])
    file_name = url.split('/')[-1].split('#')[0].split('?')[0]
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
    
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    
    f.close()

# http://downloads.sourceforge.net/reactos/ReactOS-0.3.15-REL-live.zip
def down(url):
    import urllib2
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)
    #file_name = int(meta.getheaders("Content-Disposition")[0])
    file_name = url.split('/')[-1].split('#')[0].split('?')[0]
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)
    
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
    
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    
    f.close()
