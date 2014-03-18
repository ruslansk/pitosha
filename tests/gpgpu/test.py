import pyopencl as cl

if __name__ == "__main__":

  ctx = cl.create_some_context( interactive = True )

  for found_platform in cl.get_platforms():
    print "name: " + found_platform.name
    print "ext:  " + found_platform.extensions
    print "vend: " + found_platform.vendor
    print "ver:  " + found_platform.version
    print "prof: " + found_platform.profile

    for found_device in found_platform.get_devices():
        #if pyopencl.device_type.to_string(found_device.name) == 'GPU':
        #device = found_device
        print '    name: ' + found_device.name
        print '    vend: ' + found_device.vendor
        print '    ext:  ' + found_device.extensions
        #print '    gmem: ' + found_device.global_mem_size
        #print '    maxw: ' + found_device.max_work_group_size
        #print '    addr: ' + found_device.address_bits
