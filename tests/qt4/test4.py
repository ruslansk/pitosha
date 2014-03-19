#! /usr/bin/env python
# http://www.utilities-online.info/articles/Create-a-PyQt-tray-icon-to-send-UDP-Datagram/#.UylDF3UW2PQ
from PyQt4 import QtGui, QtCore
import socket
UDP_IP = "192.168.1.1"
UDP_PORT = 20118

class RightClickMenu(QtGui.QMenu):
    def __init__(self, parent=None):
        QtGui.QMenu.__init__(self, "File", parent)

        icon = QtGui.QIcon.fromTheme("system-shutdown")
        offAction = QtGui.QAction(icon, "&Off", self)
        offAction.triggered.connect(lambda : sendudp("s53905\n"))
        self.addAction(offAction)

        icon = QtGui.QIcon.fromTheme("view-statistics")
        fmAction = QtGui.QAction(icon, "&FM", self)
        fmAction.triggered.connect(lambda : sendudp("s32113\n"))
        self.addAction(fmAction)

        icon = QtGui.QIcon.fromTheme("view-split-left-right")
        pcAction = QtGui.QAction(icon, "&PC", self)
        pcAction.triggered.connect(lambda : sendudp("s32401\n"))
        self.addAction(pcAction)

        icon = QtGui.QIcon.fromTheme("text-speak")
        muteAction = QtGui.QAction(icon, "&Mute", self)
        muteAction.triggered.connect(lambda : sendudp("s3641\n"))
        self.addAction(muteAction)

        icon = QtGui.QIcon.fromTheme("go-up")
        volupAction = QtGui.QAction(icon, "Vol &Up", self)
        volupAction.triggered.connect(lambda : sendudp("s51153\n"))
        self.addAction(volupAction)

        icon = QtGui.QIcon.fromTheme("go-down")
        voldownAction = QtGui.QAction(icon, "Vol &Down", self)
        voldownAction.triggered.connect(lambda : sendudp("s53201\n"))
        self.addAction(voldownAction)

        icon = QtGui.QIcon.fromTheme("media-skip-forward")
        chupAction = QtGui.QAction(icon, "Ch U&p", self)
        chupAction.triggered.connect(lambda : sendudp("s3150\n"))
        self.addAction(chupAction)

        icon = QtGui.QIcon.fromTheme("media-skip-backward")
        chdownAction = QtGui.QAction(icon, "Ch D&own", self)
        chdownAction.triggered.connect(lambda : sendudp("s32198\n"))
        self.addAction(chdownAction)

        icon = QtGui.QIcon.fromTheme("application-exit")
        exitAction = QtGui.QAction(icon, "&Exit", self)
        exitAction.triggered.connect(QtGui.qApp.quit)
        self.addAction(exitAction)

class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QtGui.QIcon("/home/dometec/bin/gnomeradio.xpm"))

        self.right_menu = RightClickMenu()
        self.setContextMenu(self.right_menu)

        self.activated.connect(self.onTrayIconActivated)

        class SystrayWheelEventObject(QtCore.QObject):
            def eventFilter(self, object, event):
                if type(event)==QtGui.QWheelEvent:
                    if event.delta() > 0:
                      sendudp("s51153\n")
                    else:
                      sendudp("s53201\n")
                    event.accept()
                    return True
                return False

        self.eventObj=SystrayWheelEventObject()
        self.installEventFilter(self.eventObj)

    def onTrayIconActivated(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            sendudp("s3641\n")

    def welcome(self):
        self.showMessage("Hello", "I should be aware of both buttons")

    def show(self):
        QtGui.QSystemTrayIcon.show(self)
        #QtCore.QTimer.singleShot(100, self.welcome)

def sendudp(value):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.sendto(value, (UDP_IP, UDP_PORT))

if __name__ == "__main__":
    app = QtGui.QApplication([])

    tray = SystemTrayIcon()
    tray.show()

    #set the exec loop going
    app.exec_()

