#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui

    #создание виджета
    # Первый аргумент – текст, который мы хотим увидеть.
    # Воторой аргумент – родительский виджет, 
    # т.к. Hello – единственный виджет, то у него нет родителя
    #hello = QLabel("Hello world!",None)

    #делаем виджет главным
    #a.setMainWidget(hello)

    #показать виджет
    #hello.show()

    #запустить приложение
    #a.exec_loop()

def main_():
    #создадим приложение и передадим аргументы
    app = QtGui.QApplication(sys.argv)

    #widget = QtGui.QWidget()
    #widget.resize(250, 150)
    #widget.setWindowTitle('simple')
    #widget.show()

    trayIcon = QtGui.QSystemTrayIcon(QtGui.QIcon("Bomb.xpm"), app)
    menu = QtGui.QMenu()
    exitAction = menu.addAction("Exit")
    trayIcon.setContextMenu(menu)

    trayIcon.show()
    sys.exit(app.exec_())

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtGui.QMenu(parent)
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)

    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            QtGui.QMessageBox.information(self, "Systray",
                    "The program will keep running in the system tray. To "
                    "terminate the program, choose <b>Quit</b> in the "
                    "context menu of the system tray entry.")
            self.hide()
            event.ignore()

def main():
    app = QtGui.QApplication(sys.argv)

    w = QtGui.QWidget()
    style = app.style()
    icon = QtGui.QIcon(style.standardPixmap(QtGui.QStyle.SP_FileIcon))
    #icon = QtGui.QIcon("Bomb.xpm")
    trayIcon = SystemTrayIcon(icon, w)

    trayIcon.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
