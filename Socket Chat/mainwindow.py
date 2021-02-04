import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import sys
import os
import platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        uic.loadUi("UI\main.ui", self)
        self.pushButton.clicked.connect(lambda: self.slideLeftMenu())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setUp()

        def moveWindow(e):
            # Detect if the window is  normal size
            # ###############################################
            if self.isMaximized() == False: #Not maximized
                # Move window only when window is normal size
                # ###############################################
                #if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == Qt.LeftButton:
                    #Move window
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
            # ###############################################
        self.frame_top.mouseMoveEvent = moveWindow
    def mousePressEvent(self, event):
        # ###############################################
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
    def slideLeftMenu(self):
        # Get current left menu width
        width = self.frame_left_menu.width()

        # If minimized
        if width == 70:
            # Expand menu
            newWidth = 200
        # If maximized
        else:
            # Restore menu
            newWidth = 70

        # Animate the transition
        self.animation = QPropertyAnimation(self.frame_left_menu, b"maximumWidth")#Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)#Start value is the current menu width
        self.animation.setEndValue(newWidth)#end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
    def setUp(self):
        self.exit_but.clicked.connect(self.close)


    def close(self):
        sys.exit()



