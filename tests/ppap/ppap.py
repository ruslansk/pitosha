#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Описание модуля.

Подробное описание использования.
"""

import sys
import getopt

def main():
    # Разбираем аргументы командной строки
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
        opts, args = getopt.getopt(sys.argv[1:], "g", ["goto"])
    except getopt.error, msg:
        print msg
        print "для справки используйте --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    # Анализируем
    for arg in args:
        process(arg) # process() определен в другом месте

def test():
    s=unicode("Как дела?","utf-8")
    print s
    print u'Как дела?'
    
    #import this
    
    import cv
    
    # получение кадра и запись его в файл
    #capture = cv.CaptureFromCAM(0)
    #frame = cv.QueryFrame(capture)
    #cv.SaveImage("capture.jpg", frame)
    
    # непрерывная съемка, запись кадров в видеопоток
    capture = cv.CaptureFromCAM(-1)
    #fourcc = cv.CV_FOURCC('M','J','P','G')
    #fourcc = cv.CV_FOURCC('P','I','M','1')   #это сжатие MPEG-1
    fourcc = cv.CV_FOURCC('M','P','4','2')   # MPEG-4
    fps = 16
    w, h = 640, 480
    stream = cv.CreateVideoWriter("test.avi", fourcc, fps, (w, h))
    while True:
        frame = cv.QueryFrame(capture)
        cv.WriteFrame(stream, frame)

if __name__ == '__main__':
    import talktool
    talktool.hello1()
    talktool.hello2()

    import fibo
    fibo.fib(1000)

    main()
    test()

