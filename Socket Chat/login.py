from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget,QApplication
from PyQt5.QtWidgets import *
import datetime
import sys, os
from os import path
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from client import Client
from cryptography.fernet import Fernet
from PyQt5.QtCore import QDate, QDateTime, Qt
import threading
from threading import Thread
import crypto
myClient = None
server = ""
port = ""

# class Crypto:
#     def __init__(self):
#         pass
#     def generate_key(self):
#         key = Fernet.generate_key()
#         with open("secret.key", "wb") as key_file:
#             key_file.write(key)
#
#     def load_key(self):
#         return open("secret.key", "rb").read()
#
#     def encrypt_message(self, message):
#         key = self.load_key()
#         b_str = message.encode()
#         f = Fernet(key)
#         encrypted_message = f.encrypt(b_str)
#         # return encrypted_message
#         str = encrypted_message.decode()
#         return str
#
#     def decrypt_message(self, str):
#         b_str = str.encode()
#         key = self.load_key()
#         f = Fernet(key)
#         decrypted_message = f.decrypt(b_str)
#         str = decrypted_message.decode()
#         return str
#
# crypto = Crypto()

class RegisterForm(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setUp()

    def setUp(self):
        loadUi("register_form.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.pushButton_3.clicked.connect(self.close)
        self.label.setStyleSheet("image: url(icons/1.png);")
        self.label_2.setStyleSheet("image: url(icons/user_32x32.png);")
        self.label_3.setStyleSheet("image: url(icons/lock_32x32.png);")
        self.label_4.setStyleSheet("image: url(icons/id-icon-png-24.jpg);")
        self.label_6.setStyleSheet("image: url(icons/cld.png);")
        self.signinButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.register)

    def close(self):
        sys.exit()
    def register(self):
        if self.fullname.text() == "":
            self.setStatus("Fullname is Empty!")
        elif self.username.text() == "":
            self.setStatus("Username is Empty!")
        elif self.password.text() == "":
            self.setStatus("Password is Empty!")
        else:

            # reg = Register(self.fullname.text(), self.username.text(), self.password.text())
            date = self.dob.date().toPyDate()
            dob = date.strftime("%Y/%m/%d")
            fname = self.fullname.text().split()
            query = str(len(fname)) + ' '+ self.fullname.text() + ' ' + self.username.text() + ' ' + self.password.text() + ' ' + dob
            if self.checkEncryption.isChecked():
                query = crypto.encrypt_message(query)
                query = "register encrypt " +  query
            else:
                query = "register no_encrypt " + query
            myClient.write(query)
            try:
                res = myClient.receive()
                if res == "true":
                    self.setStatus("Register Succesfully")
                else:
                    self.setStatus("Username is Exist")
            except:
                print("Cannot receive")

    def login(self):
        login_form = LoginForm(self)
        login_form.show()

    def setStatus(self, status):
        self.status.setText(status)

class LoginForm(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setUp()
        self.minimizeButton.clicked.connect(lambda: self.showMinimized())
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
        # self.header.mouseMoveEvent = moveWindow

    def mousePressEvent(self, event):
        # ###############################################
        # Get the current position of the mouse
        self.clickPosition = event.globalPos()
        # We will use this value to move the window
        # ###############################################

    def setUp(self):
        loadUi("login_form.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.closeButton.clicked.connect(close)
        self.label.setStyleSheet("image: url(icons/1.png);")
        self.label_2.setStyleSheet("image: url(icons/user_32x32.png);")
        self.label_3.setStyleSheet("image: url(icons/lock_32x32.png);")
        self.registerButton.clicked.connect(self.register)
        self.signinButton.clicked.connect(self.login)

    def close(self):
        sys.exit()

    def register(self):
        reg_form = RegisterForm(self)
        reg_form.show()

    def login(self):
        query = self.username.text() + ' ' + self.password.text()
        if self.checkEncryption.isChecked():
            query = crypto.encrypt_message(query)
            query = "login encrypt " + query
        else:
            query = "login no_encrypt " + query
        myClient.write(query)

        try:
            res = myClient.receive()
            if res == "true":
                self.setStatus("Login Succesfully")
                window = MainWindow()
                window.show()
                self.hide()
            else:
                self.setStatus("Login Unsuccesfully")
        except:
            print("Cannot receive")

    def setStatus(self, status):
        self.status.setText(status)

class ConnectServerForm(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setUp()

    def setUp(self):
        loadUi("connectServer.ui", self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.pushButton_3.clicked.connect(close)
        self.label.setStyleSheet("image: url(icons/1.png);")
        self.label_2.setText("IP")
        self.label_3.setText("PORT")
        self.connectButton.clicked.connect(self.startclient)

    def close(self):
        sys.exit()
    def startclient(self):
        SERVER = self.ip.text()
        PORT = self.port.text()
        global server, port
        server = SERVER
        port = PORT
        try:
            client = Client(SERVER, int(PORT))
            client.connect()
            if client.connected:
                login_form = LoginForm()
                login_form.show()
                self.hide()
                global myClient
                myClient = client
            else:
                self.status.setText("Server is not Exist!")
                return -1
        except:
            self.status.setText("Server is not Exist!")

class Chat(QtWidgets.QWidget):
    def __init__(self, id, fullname, username, dob):
        super(Chat, self).__init__()
        loadUi("Chat/form.ui", self)
        self.widget = QWidget(self)
        self.layout = QVBoxLayout(self.widget)
        self.area.setWidget(self.widget)
        self.chattext.returnPressed.connect(self.User_Message_Show)
        self.sendButton.clicked.connect(self.User_Message_Show)
        self.info = [id, fullname, username, dob]
        self.Show_Info()
        self.check = QLineEdit()
        self.check.textChanged.connect(self.handle_receiving)
        self.setUpIcon()
    def setUpIcon(self):
        self.logo.setStyleSheet('image: url(UI/user.png);')
        self.dobLogo.setStyleSheet('image: url(icons/cld.png);')
        self.fullnameLogo.setStyleSheet('image: url(icons/fullname.jpg);')
        self.userLogo.setStyleSheet('image: url(icons/user_32x32.png);')
    def User_Message_Show(self):
        msg = self.chattext.text()
        if not msg:
            return
        myClient.write("sendmessage " + str(self.info[0]) + ' ' + msg)
        msg_box = self.create_Msg_Box(self.chattext.text(), "white")

        self.layout.addWidget(msg_box, Qt.AlignLeft, Qt.AlignLeft)
        scroll_bar = self.area.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        self.chattext.setText('')

    def handle_receiving(self):
        msg = self.check.text()
        if msg == "this_user_is_not_active ":
            self.User_Not_Active_Notify()
        elif msg == "this_user_is_offline ":
            self.User_Offline_Notify()
        else:
            self.Friend_Message_Show()

        self.check.setText('')

    def User_Not_Active_Notify(self):
        msg_box = self.create_Msg_Box(self.info[1] + " is Not Active!!", "pink")
        self.layout.addWidget(msg_box, Qt.AlignLeft, Qt.AlignLeft)
        scroll_bar = self.area.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))

    def User_Offline_Notify(self):
        msg_box = self.create_Msg_Box(self.info[1] + " is Offline!!", "red")
        self.layout.addWidget(msg_box, Qt.AlignLeft, Qt.AlignLeft)
        scroll_bar = self.area.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))

    def Friend_Message_Show(self):
        msg = self.check.text()
        self.check.setText('')
        if not msg:
            return
        msg_box = self.create_Msg_Box(msg,"white")
        self.layout.addWidget(msg_box, Qt.AlignRight, Qt.AlignRight)
        scroll_bar = self.area.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))

    def create_Msg_Box(self, msg, color):
        msg_box = QTextEdit(self)
        msg_box.setStyleSheet(
            "border: 1px solid;font: 20px;color:"+color+"; border-radius:10px;background-color: rgb(96, 96, 96);")
        i = 20
        while i < len(msg):
            msg = msg[:i] + '\n' + msg[i:]
            i = i + 21
        # font = msg_box.document().defaultFont()
        font = QFont()
        font.setWeight(20)
        msg_box.document().setPlainText(msg)

        fontMetrics = QFontMetrics(font)
        textSize = 1.6 * fontMetrics.size(0, msg_box.toPlainText())

        w = textSize.width() + 15
        h = textSize.height() + 15
        msg_box.setMinimumSize(w, h)
        msg_box.setMaximumSize(w, h)
        msg_box.resize(w, h)
        msg_box.setReadOnly(True)
        return msg_box

    def Handle_Info(self, info):
        info = info.split()
        n_fname = int(info[0])
        fullname = ""
        for i in range(1, n_fname):
            fullname = fullname + info[i] + ' '
        fullname = fullname + info[n_fname]
        username = info[n_fname + 1]
        dob = info[n_fname+2]
        inf = [fullname, username, dob]
        return inf

    def Show_Info(self):
        self.fullname.setText(self.info[1])
        self.username.setText(self.info[2])
        self.dob.setText(self.info[3])

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        loadUi("UI\main.ui", self)
        self.pushButton.clicked.connect(lambda: self.slideLeftMenu())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.chat_status = 0
        self.chat_frame = {}
        self.id_idx = {}
        self.setUp()
        self.setUp_Icon()
        self.is_chat_listening = False
        self.chatThread = threading.Thread(target=self.handle_chat)
        self.listCheck = QLineEdit()
        self.listCheck.textChanged.connect(self.list_handle)

        def moveWindow(e):
            # Detect if the window is  normal size
            if self.isMaximized() == False:  # Not maximized
                # Move window only when window is normal size
                # if left mouse button is clicked (Only accept left mouse button clicks)
                if e.buttons() == Qt.LeftButton:
                    # Move window
                    self.move(self.pos() + e.globalPos() - self.clickPosition)
                    self.clickPosition = e.globalPos()
                    e.accept()
        self.frame_top.mouseMoveEvent = moveWindow

    def setUp_Icon(self):
        self.account.setStyleSheet("QPushButton\n"
                        "{background-repeat: none;\n"
                        "background-image: url(UI/cil-user.png);\n"
                        "padding-left: 45px;\n"
                        "background-position: center left;\n"
                        "border-left: 24px solid transparent;\n"
                        "background-color:transparent;}\n"

                        "QPushButton:hover { background-color:rgb(13, 13, 39); border-left: 26px solid rgba(255, 255, 255, 190);}\n"
                        "QPushButton:pressed {background-color:rgb(13, 13, 39);border-left: 26px solid rgba(255, 255, 255, 190);}")
        self.chat.setStyleSheet("QPushButton\n"
                        "{background-repeat: none;\n"
                        "background-image: url(UI/cil-comment-bubble.png);\n"
                        "padding-left: 45px;\n"
                        "background-position: center left;\n"
                        "border-left: 24px solid transparent;\n"
                        "background-color:transparent;}\n"

                        "QPushButton:hover { background-color:rgb(13, 13, 39); border-left: 26px solid rgba(255, 255, 255, 190);}\n"
                        "QPushButton:pressed {background-color:rgb(13, 13, 39);border-left: 26px solid rgba(255, 255, 255, 190);}")
        self.file.setStyleSheet("QPushButton\n"
                        "{background-repeat: none;\n"
                        "background-image: url(UI/cil-folder-open.png);\n"
                        "padding-left: 45px;\n"
                        "background-position: center left;\n"
                        "border-left: 24px solid transparent;\n"
                        "background-color:transparent;}\n"

                        "QPushButton:hover { background-color:rgb(13, 13, 39); border-left: 26px solid rgba(255, 255, 255, 190);}\n"
                        "QPushButton:pressed {background-color:rgb(13, 13, 39);border-left: 26px solid rgba(255, 255, 255, 190);}")
        self.logout.setStyleSheet("QPushButton\n"
                        "{background-repeat: none;\n"
                        "background-image: url(UI/cil-power-standby.png);\n"
                        "padding-left: 45px;\n"
                        "background-position: center left;\n"
                        "border-left: 24px solid transparent;\n"
                        "background-color:transparent;}\n"

                        "QPushButton:hover { background-color:rgb(13, 13, 39); border-left: 26px solid rgba(255, 255, 255, 190);}\n"
                        "QPushButton:pressed {background-color:rgb(13, 13, 39);border-left: 26px solid rgba(255, 255, 255, 190);}")

    def browsefiles(self):
      fname = QFileDialog.getOpenFileName(self, 'Open file','.','All Files(*.*)')
      self.upload_link.setText(fname[0])
    def Handel_Progress(self , blocknum , blocksize , totalsize):
        ## calculate the progress
        readed_data = blocknum * blocksize
        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.progressBar.setValue(download_percentage)
            QApplication.processEvents()
    def Handel_Browse(self):
        #save_location = QFileDialog.getSaveFileUrl(self, caption="Save")
        save_location = QFileDialog.getSaveFileName(self, caption="Save as", directory=".", filter="All Files(*.*)")
        self.in_link.setText(str(save_location[0]))
    def Download(self):
        download_url = self.down_link.text()
        save_location = self.in_link.text()

        client = Client(server, int(port))
        client.connect()
        if download_url == '' or save_location == '':
            QMessageBox.warning(self, "Data Error" , "Provide a valid URL or save location")
        else:
            th = DownloadThread(save_location,download_url, client, self)
            th.start()
            th.join()
            if not th.res:
                QMessageBox.information(self, "Download Uncompleted", "File NOT FOUND!")
                pass
            else:
                QMessageBox.information(self, "Download Completed", "The Download Completed Successfully ")

        client.write("close")
        client.close()
        self.down_link.setText('')
        self.in_link.setText('')
        self.progressBar.setValue(0)
    def upload(self):
        upload_url = self.upload_link.text()
        filename = self.upload_link_2.text()
        client = Client(server, int(port))
        client.connect()
        th = UploadThread(upload_url, filename, client, self)
        th.start()
        th.join()
        # if not self.sendFile(upload_url, filename):
        #     QMessageBox.warning(self, "Data Error", "File in server exists!")
        # else:

            # QMessageBox.warning(self, "Upload Successfully", "Upload Successfully!")
        if not th.res:
            QMessageBox.warning(self, "Data Error", "File in server exists!")
            pass
        else:
            QMessageBox.warning(self, "Upload Successfully", "Upload Successfully!")

        self.upload_link_2.setText('')
        self.progressBar.setValue(0)
        self.upload_link.setText('')
    def Save_Browse(self):
        pass
    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()
    def slideLeftMenu(self):
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
        self.animation = QPropertyAnimation(self.frame_left_menu, b"maximumWidth")  # Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)  # Start value is the current menu width
        self.animation.setEndValue(newWidth)  # end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def change_chat_box(self):
        idx = self.listUsers.currentRow()
        self.stackedWidget_2.setCurrentWidget(self.chat_frame[idx])

    def file_clicked(self):
        # if self.is_chat_listening:
        #     myClient.write("stop_receiving_message")
        self.is_chat_listening = True
        self.stackedWidget.setCurrentWidget(self.File_page)

    def account_clicked(self):
        if self.is_chat_listening:
            myClient.write("stop_receiving_message")
        self.stackedWidget.setCurrentWidget(self.Account_page)

    def logout_clicked(self):
        if self.is_chat_listening:
            myClient.write("stop_receiving_message")
    def chat_clicked(self):
        self.stackedWidget.setCurrentWidget(self.Chat_page)
        if self.chat_status == 0:
            self.chat_status = 1
            myClient.write("getuseronlineinfo")
            list = myClient.receive()
            self.listCheck.setText(list)
            self.chatThread.start()
            self.is_chat_listening = True
        else:
            myClient.write("getmoreuseronlineinfo")
            self.is_chat_listening = True
    def list_handle(self):
        list = self.listCheck.text()
        if list != "listuser ":
            list = list.split()
            print("List user: ")
            print(list)
            i = 1
            while i < len(list):
                id = list[i]
                i = i + 1
                n_fname = int(list[i])
                fullname = ""
                i = i + 1
                for j in range(i, i + n_fname - 1):
                    fullname = fullname + list[j] + ' '
                fullname = fullname + list[i + n_fname - 1]
                username = list[i + n_fname]
                dob = list[i + n_fname + 2]
                self.listUsers.addItem(fullname)
                newChat = Chat(id, fullname, username, dob)
                idx = self.listUsers.count() - 1
                self.chat_frame[idx] = newChat
                self.id_idx[id] = idx
                self.stackedWidget_2.addWidget(newChat)
                # self.stackedWidget_2.setCurrentWidget()
                i = i + n_fname + 3
            self.num_user.setText(str(self.listUsers.count()))
    def handle_chat(self):
        while myClient.connected:
            if self.is_chat_listening:
                print("listening")
                msg = myClient.client.recv(2048).decode(myClient.FORMAT)
                print(msg)
                if (msg.split())[0] == "listuser":
                    self.listCheck.setText(msg)
                    continue
                if msg == "stop_receiving_message":
                    print("stop listening")
                    self.is_chat_listening = False
                    continue
                elif msg:
                    id = msg.split()[0]
                    if id not in self.id_idx:
                        continue
                    idx = self.id_idx[id]
                    message = msg.split()
                    msg = ""
                    for i in range (1, len(message)):
                        msg = msg + message[i] + ' '
                    if idx > -1:
                        chat_box = self.chat_frame[idx]
                        chat_box.check.setText(msg)
    def close(self):
        myClient.connected = False
        sys.exit()
    def changePassword(self):
        oldPwd = self.show_password.text()
        newPwd = self.show_newpassword.text()
        cmd = oldPwd + ' ' + newPwd
        if self.checkEncryption.isChecked():
            cmd = crypto.encrypt_message(cmd)
            cmd = "editpassword encrypt " + cmd
        else:
            cmd = "editpassword noencrypt " + cmd
        myClient.write(cmd)
        res = myClient.receive()
        if res == "true":
            self.change_pwd_status.setText("Change Password Successfully")
        else:
            self.change_pwd_status.setText("Old Password is Incorrect")
    def changeInfo(self):
        fullname = self.show_fullname.text()
        d = self.edit_dob.date().toPyDate()
        dob = d.strftime("%Y/%m/%d")
        n_fname = len(fullname.split())
        query = "editinfo" + " " + str(n_fname) + " " + fullname + " " + dob
        print(query)
        myClient.write(query)
        self.edit_status.setText("Information has been updated")
    def sendFile(self, filepath, filename):
        if not path.exists(filepath):
            return False
        f = open(filepath, "rb")
        filesize = os.path.getsize(filepath)
        query = "sendfile " + str(filesize) + " " + filename
        myClient.write(query)
        print(query)
        res = myClient.receive()
        if res == "false":
            return False
        l = f.read(1024)
        i = 1
        while l:
            myClient.sendFile(l)
            self.Handel_Progress(i, 1024, filesize)
            i = i + 1
            l = f.read(1024)
        f.close()
        print("sent")
        return True


    # def downloadFile(self, filepath, filename, myClient):
    #     if path.exists(filepath):
    #         QMessageBox.information(self, "Download Uncompleted", "File save exist!")
    #         return False
    #     print("Send download query to Server")
    #     myClient.write("downloadfile " + filename)
    #
    #     filesize = myClient.receive()
    #     myClient.write("true")
    #
    #     if filesize == "false":
    #         QMessageBox.information(self, "Download Uncompleted", "File NOT FOUND!")
    #         return False
    #     print(filesize)
    #     filesize = int(filesize)
    #     f = open(filepath, 'wb')
    #     total = 0
    #     i = 1
    #     # myClient.receive()
    #     while 1:
    #         if total < filesize:
    #             data = myClient.recFile()
    #             self.Handel_Progress(i,1024,filesize)
    #             i = i + 1
    #             f.write(data)
    #             total = total + len(data)
    #         else:
    #             break
    #     f.close()
    #     print("File received")
    #     return True
    def setUp(self):
        self.exit_but.clicked.connect(close)
        info = getInformation()
        self.show_fullname.setText(str(info[0]))
        self.show_username.setText(str(info[1]))
        self.oldPwd = str(info[2])
        self.change_pwd.clicked.connect(self.changePassword)
        self.edit_dob.setDate(info[3])
        self.edit.clicked.connect(self.changeInfo)
        self.stackedWidget.setCurrentWidget(self.Account_page)
        self.file.clicked.connect(self.file_clicked)
        self.account.clicked.connect(self.account_clicked)
        self.down_but.clicked.connect(self.Download)
        self.search_but.clicked.connect(self.Handel_Browse)
        self.browse.clicked.connect(self.browsefiles)
        self.upload_bt.clicked.connect(self.upload)
        self.chat.clicked.connect(self.chat_clicked)
        self.listUsers.itemClicked.connect(self.change_chat_box)
        self.pushButton_2.clicked.connect(self.mini_chat)
    def mini_chat(self):
        width = self.frame_4.width()
        # If minimized
        if width == 1:
            # Expand menu
            newWidth = 400
        # If maximized
        else:
            # Restore menu
            newWidth = 1

        # Animate the transition
        self.animation = QPropertyAnimation(self.frame_4, b"maximumWidth")  # Animate minimumWidht
        self.animation.setDuration(250)
        self.animation.setStartValue(width)  # Start value is the current menu width
        self.animation.setEndValue(newWidth)  # end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
def getInformation():
    myClient.write("getinfo")
    info = myClient.receive()
    info = info.split()
    n_fname = int(info[0])
    fullname = ""
    for i in range(1, n_fname):
        fullname = fullname + info[i] + ' '
    fullname = fullname + info[n_fname]
    username = info[n_fname + 1]
    pwd = info[n_fname + 2]
    dob = datetime.datetime.strptime(info[n_fname + 3], "%Y/%m/%d").date()
    # dob = info[n_fname+3]
    inf = [fullname, username, pwd, dob]
    return inf


class DownloadThread(Thread):
    def __init__(self, filepath, filename, myClient, window):
        super(DownloadThread, self).__init__()
        self.filename = filename
        self.filepath = filepath
        self.myClient = myClient
        self.res = False
        self.window = window
    def run(self):
        self.res = self.downloadFile(self.filepath,self.filename,self.myClient)
    def downloadFile(self, filepath, filename, myClient):
        if path.exists(filepath):
            return False
        print("Send download query to Server")
        myClient.write("downloadfile " + filename)

        filesize = myClient.receive()
        myClient.write("true")
        print(filesize)

        if filesize == "false":
            return False
        print(filesize)
        filesize = int(filesize)
        f = open(filepath, 'wb')
        total = 0
        i = 1
        # myClient.receive()
        while 1:
            if total < filesize:
                data = myClient.recFile()
                self.window.Handel_Progress(i,1024,filesize)
                i = i + 1
                f.write(data)
                total = total + len(data)
            else:
                break
        f.close()
        print("File received")
        return True
class UploadThread(Thread):
    def __init__(self, filepath, filename, myClient, window):
        super(UploadThread, self).__init__()
        self.filename = filename
        self.filepath = filepath
        self.myClient = myClient
        self.res = False
        self.window = window
    def run(self):
        self.res = self.sendFile(self.filepath, self.filename, self.myClient)
    def sendFile(self, filepath, filename, myClient):
        if not path.exists(filepath):
            return False
        f = open(filepath, "rb")
        filesize = os.path.getsize(filepath)
        query = "sendfile " + str(filesize) + " " + filename
        myClient.write(query)
        print(query)
        res = myClient.receive()
        if res == "false":
            return False
        l = f.read(1024)
        i = 1
        while l:
            myClient.sendFile(l)
            self.window.Handel_Progress(i, 1024, filesize)
            i = i + 1
            l = f.read(1024)
        f.close()
        print("sent")
        return True
def close():
    if myClient != None:
        myClient.connected = False
        myClient.write("stop_receiving_message")
        myClient.write("close")
    sys.exit()
def start():
    app = QtWidgets.QApplication(sys.argv)
    connect_form = ConnectServerForm()
    connect_form.show()
    sys.exit(app.exec_())

start()
