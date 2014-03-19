#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
import sys

print 'QtCore.PYQT_VERSION_STR : ' + QtCore.PYQT_VERSION_STR
print 'QtCore.QT_VERSION_STR   : ' + QtCore.QT_VERSION_STR

def run():
  app     = QtGui.QApplication(sys.argv)
  window  = QtGui.QWidget()
  window.setWindowTitle(u"Первая программа на PyQt")
  window.resize(300, 70)
  #window.setIcon(QtGui.QIcon("/home/dometec/bin/gnomeradio.xpm"))
  #window.setIcon(QtGui.QIcon("ico_16.xpm"))
  label   = QtGui.QLabel(u"<center>Привет, мир!</center>")
  #label  = QtGui.QLabel(u"Привет, мир!")
  btnQuit = QtGui.QPushButton(u"&Закрыть окно")
  vbox    = QtGui.QVBoxLayout()
  vbox.addWidget(label)
  vbox.addWidget(btnQuit)
  window.setLayout(vbox)
  QtCore.QObject.connect(btnQuit,
                         QtCore.SIGNAL("clicked()"),
                         QtGui.qApp,
                         QtCore.SLOT("quit()"))
  #btnQuit.connect.clicked("quit()")
  print "QtGui.qApp.argv():"
  print (QtGui.qApp.argv())
  window.show()
  sys.exit(app.exec_())

if __name__ == "__main__":
  run()

