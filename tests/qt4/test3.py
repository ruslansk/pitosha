#! /usr/bin/env python
from PyQt4 import QtGui, QtCore

class RightClickMenu(QtGui.QMenu):
    def __init__(self, parent=None):
        QtGui.QMenu.__init__(self, "Edit", parent)

        icon = QtGui.QIcon.fromTheme("edit-cut")
        self.addAction(QtGui.QAction(icon, "&Cut", self))

        icon = QtGui.QIcon.fromTheme("edit-copy")
        self.addAction(QtGui.QAction(icon, "Copy (&X)", self))

        icon = QtGui.QIcon.fromTheme("edit-paste")
        self.addAction(QtGui.QAction(icon, "&Paste", self))
    
class LeftClickMenu(QtGui.QMenu):
    def __init__(self, parent=None):
        QtGui.QMenu.__init__(self, "File", parent)

        icon = QtGui.QIcon.fromTheme("document-new")
        self.addAction(QtGui.QAction(icon, "&New", self))

        icon = QtGui.QIcon.fromTheme("document-open")
        self.addAction(QtGui.QAction(icon, "&Open", self))

        icon = QtGui.QIcon.fromTheme("document-save")
        self.addAction(QtGui.QAction(icon, "&Save", self))


class SystemTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
        self.setIcon(QtGui.QIcon.fromTheme("document-save"))

        self.right_menu = RightClickMenu()
        self.setContextMenu(self.right_menu)

        self.left_menu = LeftClickMenu()
    
        self.activated.connect(self.click_trap)

    def click_trap(self, value):
        if value == self.Trigger: #left click!
            self.left_menu.exec_(QtGui.QCursor.pos())

    def welcome(self):
        self.showMessage("Hello", "I should be aware of both buttons")
        
    def show(self):
        QtGui.QSystemTrayIcon.show(self)
        QtCore.QTimer.singleShot(100, self.welcome)

if __name__ == "__main__":
    app = QtGui.QApplication([])

    tray = SystemTrayIcon()
    tray.show()
    
    #set the exec loop going
    app.exec_()

