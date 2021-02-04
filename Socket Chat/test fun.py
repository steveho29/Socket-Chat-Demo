# # # import datetime
# # #
# # # d = datetime.date(2001,11,24)
# # # s = d.strftime("%Y/%m/%d")
# # # d2 = datetime.datetime.strptime(s, "%Y/%m/%d").date()
# # # s = d2.strftime("%Y/%m/%d")
# # #
# # # query = "register gdfsg sdfgfds gsdfgfds 2001/10/29"
# # # querry = query.split()
# # #
# # # print(querry)
# #
# # from PyQt5 import QtCore, QtWidgets
# # from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout
# # import sys
# # from PyQt5.QtWidgets import *
# # from PyQt5.QtCore import *
# # from PyQt5.QtGui import *
# # import sys
# # from PyQt5.QtWidgets import QDialog, QApplication, QPushButton
# # from PyQt5.uic import loadUi
# # from PyQt5.QtCore import *
# # from PyQt5.QtGui import *
# # import client
# # from client import Client
# # from SQLConnect import Register, GetInfo
# # from SQLConnect import Login
# # # import icon_rc
# # from PyQt5.QtCore import QDate, QDateTime, Qt
# #
# # from itertools import cycle
# # import base64
# # import base64
# #
# # def xor_crypt_string(data, key='awesomepassword', encode=False, decode=False):
# #
# #
# #     if decode:
# #         data = base64.decodestring(data)
# #         xored = ''.join(chr(ord(x) ^ ord(y)) for (x, y) in zip(data, cycle(key)))
# #
# #     if encode:
# #         return base64.b64encode(xored).strip()
# #     return xored
# #
# #
# # secret_data = "XOR procedure"
# # print("The cipher text is")
# # print( xor_crypt_string(secret_data, encode = True))
# # print("The plain text fetched")
# # print( xor_crypt_string(xor_crypt_string(secret_data, encode = True), decode = True))
# from functools import partial
#
# from PyQt5.QtWidgets import (QWidget, QListWidget, QVBoxLayout, QApplication)
# import sys
#
# # class Example(QWidget):
# #
# #     def __init__(self):
# #         super().__init__()
# #
# #
# #         self.l = QListWidget()
# #         for n in range(10):
# #             self.l.addItem(str(n))
# #
# #         self.l.itemSelectionChanged.connect(self.selectionChanged)
# #
# #         vbox = QVBoxLayout()
# #         vbox.addWidget(self.l)
# #
# #         self.setLayout(vbox)
# #         self.setGeometry(300, 300, 300, 300)
# #         self.show()
# #
# #     def selectionChanged(self):
# #         print("vy heo", self.l.selectedItems())
# # if __name__ == '__main__':
# #
# #     app = QApplication(sys.argv)
# #     ex = Example()
# #     sys.exit(app.exec_())
#
# from PyQt5 import QtGui
# from PyQt5.QtWidgets import QDialog, QApplication, QPushButton
# text = ("The answer is QFontMetrics\n."
#         "\n"
#         "The layout system messes with the width that QTextEdit thinks it\n"
#         "needs to be.  Instead, let's ignore the GUI entirely by using\n"
#         "QFontMetrics.  This can tell us the size of our text\n"
#         "given a certain font, regardless of the GUI it which that text will be displayed.")
#
#
# """ A text editor that automatically adjusts its height to the height of the text
#     in its document when managed by a layout. """
# from PyQt5 import QtCore, QtWidgets
# from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QHBoxLayout
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# import datetime
# import sys, os
# from os import path
# from PyQt5.QtWidgets import QDialog, QApplication, QPushButton
# from PyQt5.uic import loadUi
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import QTextEdit, QSizePolicy
# from PyQt5.QtGui     import QFontMetrics
# from PyQt5.QtCore    import QSize
# from PyQt5.QtWidgets import QWidget, QVBoxLayout
# from auto_resizing_text_edit import AutoResizingTextEdit
# class Example(QWidget):
#     def __init__(self):
#         super(Example, self).__init__()
#         widget = QWidget()
#         editor = AutoResizingTextEdit()
#         editor.setMinimumLines(3)
#         editor.setParent(widget)
#
#         layout = QVBoxLayout(widget)
#         layout.addWidget(editor)
#         layout.addStretch()
#
#         widget.setLayout(layout)
#
#         self.show()
#
# import sys
#
# from PyQt5.QtGui import QFontMetrics
# from PyQt5 import QtCore, QtWidgets
# import sys, os
# from os import path
# from PyQt5.QtWidgets import QDialog, QApplication, QPushButton
# from PyQt5.uic import loadUi
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import QMainWindow, QLineEdit, QWidget, QVBoxLayout, QApplication, QTextEdit, QPushButton, QScrollArea
# class Chat(QtWidgets.QWidget):
#     def __init__(self, id, fullname, username, dob):
#         super(Chat, self).__init__()
#         loadUi("Chat/form.ui", self)
#         self.widget = QWidget(self)
#         self.layout = QVBoxLayout(self.widget)
#         self.area.setWidget(self.widget)
#         self.chattext.returnPressed.connect(self.User_Message_Show)
#         self.sendButton.clicked.connect(self.User_Message_Show)
#         self.info = [id, fullname, username, dob]
#         self.Show_Info()
#
#     def User_Message_Show(self):
#         msg = self.chattext.text()
#         if not msg:
#             return
#         msg_box = self.create_Msg_Box(self.chattext.text())
#         self.area.ensureVisible(0,99999999,0,0)
#
#         self.layout.addWidget(msg_box,Qt.AlignLeft, Qt.AlignLeft)
#
#         scroll_bar = self.area.verticalScrollBar()
#         scroll_bar.rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
#         self.chattext.setText('')
#
#     def Friend_Message_Show(self, msg):
#         if not msg:
#             return
#         msg_box = self.create_Msg_Box(self.chattext.text())
#         self.area.ensureVisible(0, 99999999, 0, 0)
#         self.layout.addWidget(msg_box, Qt.AligntRight, Qt.AlignRight)
#
#     def create_Msg_Box(self, msg):
#         msg_box = QTextEdit(self)
#         msg_box.setStyleSheet(
#             "border: 1px solid;font: 20px;color: white; border-radius:10px;background-color: rgb(96, 96, 96);")
#         i = 27
#         while i < len(msg):
#             msg = msg[:i] + '\n' + msg[i:]
#             i = i + 28
#         font = msg_box.document().defaultFont()
#
#         msg_box.document().setPlainText(msg)
#
#         fontMetrics = QFontMetrics(font)
#         textSize = 1.6 * fontMetrics.size(0, msg_box.toPlainText())
#
#         w = textSize.width() + 15
#
#         h = textSize.height() + 15
#         msg_box.setMinimumSize(w, h)
#         msg_box.setMaximumSize(w, h)
#         msg_box.resize(w, h)
#
#         msg_box.setReadOnly(True)
#
#         return msg_box
#
#     def Handle_Info(self, info):
#         info = info.split()
#         n_fname = int(info[0])
#         fullname = ""
#         for i in range(1, n_fname):
#             fullname = fullname + info[i] + ' '
#         fullname = fullname + info[n_fname]
#         username = info[n_fname + 1]
#         dob = info[n_fname+2]
#         inf = [fullname, username, dob]
#         return inf
#
#     def Show_Info(self):
#         self.fullname.setText(self.info[1])
#         self.username.setText(self.info[2])
#         self.dob.setText(self.info[3])
#
#
#
# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         loadUi("UI\main.ui", self)
#         self.pushButton.clicked.connect(lambda: self.slideLeftMenu())
#         self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
#         self.chat_status = 0
#         self.setUp()
#
#         def moveWindow(e):
#             # Detect if the window is  normal size
#             # ###############################################
#             if self.isMaximized() == False:  # Not maximized
#                 # Move window only when window is normal size
#                 # ###############################################
#                 # if left mouse button is clicked (Only accept left mouse button clicks)
#                 if e.buttons() == Qt.LeftButton:
#                     # Move window
#                     self.move(self.pos() + e.globalPos() - self.clickPosition)
#                     self.clickPosition = e.globalPos()
#                     e.accept()
#             # ###############################################
#         self.frame_top.mouseMoveEvent = moveWindow
#
#     def mousePressEvent(self, event):
#         # ###############################################
#         # Get the current position of the mouse
#         self.clickPosition = event.globalPos()
#     def slideLeftMenu(self):
#         # Get current left menu width
#         width = self.frame_left_menu.width()
#
#         # If minimized
#         if width == 70:
#             # Expand menu
#             newWidth = 200
#         # If maximized
#         else:
#             # Restore menu
#             newWidth = 70
#
#         # Animate the transition
#         self.animation = QPropertyAnimation(self.frame_left_menu, b"maximumWidth")  # Animate minimumWidht
#         self.animation.setDuration(250)
#         self.animation.setStartValue(width)  # Start value is the current menu width
#         self.animation.setEndValue(newWidth)  # end value is the new menu width
#         self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
#         self.animation.start()
#     def setUp(self):
#         self.exit_but.clicked.connect(self.close)
#
#         self.stackedWidget.setCurrentWidget(self.chat)
#         self.chat.clicked.connect(self.chat_clicked)
#
#     def chat_clicked(self):
#         self.stackedWidget.setCurrentWidget(self.Chat_page)
#         # if self.chat_status == 0:
#         #     self.chat_status = 1
#         #     myClient.write("getfullnamesonline")
#         # else:
#         #     myClient.write("getmorefullnamesonline")
#
#         # list = myClient.receive()
#         list = "4 Hồ Ngọc Minh Đức"
#
#         if list != "-1":
#             list = list.split()
#             i = 0
#             while i < len(list):
#                 n_fname = int(list[i])
#                 fullname = ""
#                 i = i + 1
#                 for j in range(i, i + n_fname - 1):
#                     fullname = fullname + list[j] + ' '
#                 fullname = fullname + list[i + n_fname - 1]
#                 print(fullname)
#                 self.listUsers.addItem(fullname)
#                 newChat = Chat(info)
#                 self.stackedWidget_2.addWidget(newChat)
#                 self.stackedWidget_2.setCurrentWidget(newChat)
#                 i = i + n_fname
#
#     def close(self):
#         sys.exit()
#
#
#
# class Main(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.resize(500,500)
#         self.lista = ["one"]
#         self.widget = QWidget(self)
#         self.layout = QVBoxLayout(self.widget)
#         self.area = QScrollArea(self)
#         self.area.resize(400, 300)
#         self.area.setWidget(self.widget)
#         self.area.setWidgetResizable(True)
#
#         self.plainnn = QLineEdit(self)
#         self.plainnn.move(0, 305)
#         self.plainnn.resize(400, 50)
#
#         self.boton = QPushButton(self)
#         self.boton.move(0, 360)
#         self.boton.setText("Press")
#
#         self.boton.clicked.connect(self.Test)
#
#     def Test(self):
#             textt = QTextEdit(self)
#             textt.setStyleSheet("border: 1px solid; color: white; border-radius:10px;background-color: rgb(96, 96, 96);")
#
#             tt = self.plainnn.text()
#             print(tt)
#             textt.document().setPlainText(tt)
#
#             font = textt.document().defaultFont()
#             fontMetrics = QFontMetrics(font)
#             textSize = fontMetrics.size(0, textt.toPlainText())
#
#             w = textSize.width() + 10
#             h = textSize.height() + 10
#             textt.setMinimumSize(w, h)
#             textt.setMaximumSize(w, h)
#             textt.resize(w, h)
#
#             textt.setReadOnly(True)
#
#             self.plainnn.setText('')
#             self.layout.addWidget(textt)
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     m = MainWindow()
#     m.show()
#     sys.exit(app.exec_())
import threading
from threading import Thread
class TestThread(Thread):
    def __init__(self, num):
        super(TestThread, self).__init__()
        self.n = num
        self.id = None

    def run(self):
        self.id = self.n

th = TestThread(29)
th.start()
th.join()
print(th.id)

