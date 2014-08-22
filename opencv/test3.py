import cv

capture = cv.CaptureFromCAM(-1)
fourcc = cv.CV_FOURCC('M','J','P','G')
fps = 16
w, h = 640, 480
stream = cv.CreateVideoWriter("test.avi", fourcc, fps, (w, h))
while True:
    frame = cv.QueryFrame(capture)
    cv.WriteFrame(stream, frame)
