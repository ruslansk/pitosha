import sys
import cv,cv2
import numpy
cascade = cv.Load('haarcascade_frontalface_alt.xml')

def detect(image):
    bitmap = cv.fromarray(image)
    faces = cv.HaarDetectObjects(bitmap, cascade, cv.CreateMemStorage(0))
    if faces:
        for (x,y,w,h),n in faces:
            pass
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255),2)
    return image

if __name__ == "__main__":
    cam = cv2.VideoCapture(0)
    while 1:
        _,frame =cam.read()
        frame = numpy.asarray(detect(frame))
        cv2.imshow("features", frame)
        if cv2.waitKey(10) == 0x1b: # ESC
            print 'ESC pressed. Exiting ...'
            break
