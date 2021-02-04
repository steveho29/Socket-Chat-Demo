import socket
import threading
import os.path
from os import path
from termcolor import colored
import colorama
# import crypto
import pyodbc
import datetime
from cryptography.fernet import Fernet

class Crypto:
    def __init__(self):
        pass
    def generate_key(self):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        return open("secret.key", "rb").read()

    def encrypt_message(self, message):
        key = self.load_key()
        b_str = message.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(b_str)
        # return encrypted_message
        str = encrypted_message.decode()
        return str

    def decrypt_message(self, str):
        b_str = str.encode()
        key = self.load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(b_str)
        str = decrypted_message.decode()
        return str
sqlserver = input("SQL Server Name: ")
class SQLServer:
    def __init__(self):
        self.driver = '{ODBC Driver 17 for SQL Server}'
        self.database = "Table"
        self.server = sqlserver

class Register(SQLServer):
    def __init__(self, fname, uname, pwd, dob):
        super(Register, self).__init__()
        self.id = 0
        self.getId()
        self.fname = fname
        self.uname = uname
        self.pwd = pwd
        self.dob = dob
        self.status = True
        try:
            self.status = self.reg()
        except:
            self.status = False

    def reg(self):
        conn = pyodbc.connect(Driver=self.driver, Server=self.server, Database=self.database, Trusted_Connection='yes')
        cursor = conn.cursor()
        if self.checkUsernameExist(self.uname):
            return False
        SQLCommand = "INSERT INTO [dbo].[Table] (loginid, fullname, username,password, dob) VALUES (?,?,?,?,?)"
        Values = [self.id, self.fname, self.uname, self.pwd, self.dob]
        cursor.execute(SQLCommand, Values)
        conn.commit()
        return True

    def getId(self):
        conn = pyodbc.connect(Driver=self.driver, Server=self.server, Database=self.database, Trusted_Connection='yes')
        cursor = conn.cursor()
        SQLCommand = "SELECT COUNT(*) FROM [dbo].[Table]"
        cursor.execute(SQLCommand)
        id = cursor.fetchone()[0]
        self.id = id+1
        cursor.commit()

    def checkUsernameExist(self, username):
        conn = pyodbc.connect(Driver=self.driver, Server=self.server, Database=self.database, Trusted_Connection='yes')
        cursor = conn.cursor()
        SQLCommand = "SELECT * FROM [Table] WHERE username = ?"
        res = False
        Value = [username]
        query = cursor.execute(SQLCommand, Value)
        for row in query:
            res = True
        conn.commit()
        return res

class Login(SQLServer):
    def __init__(self, uname, pwd):
        super(Login, self).__init__()
        self.uname = uname
        self.pwd = pwd
        self.status = False
        self.id = -1
        try:
            self.login()
        except:
            self.status = False

    def login(self):
        conn = pyodbc.connect(Driver=self.driver, Server=self.server, Database=self.database, Trusted_Connection='yes')
        cursor = conn.cursor()
        SQLCommand = "SELECT * FROM [Table] WHERE username = ? AND password = ?"
        Values = [self.uname, self.pwd]
        query = cursor.execute(SQLCommand, Values)
        for row in query:
            self.status = True
            self.id = row[0]
        conn.commit()

class GetInfo(SQLServer):
    def __init__(self, id):
        super(GetInfo, self).__init__()
        self.id = int(id)
        self.info = ""
        self.getInfo()
    def getInfo(self):
        conn = pyodbc.connect(Driver=self.driver, Server=self.server, Database=self.database, Trusted_Connection='yes')
        cursor = conn.cursor()
        SQLCommand = "SELECT * FROM [Table] WHERE loginid = ?"
        Values = [self.id]
        query = cursor.execute(SQLCommand, Values)
        username = fullname = password = ""

        for row in query:
            fullname = row[1]
            username = row[2]
            password = row[3]
            dob = row[4].strftime("%Y/%m/%d")
        n_fname = len(fullname.split())
        self.info = str(n_fname) + ' ' + fullname + username + password + dob
        conn.commit()

class GetPassword(SQLServer):
    def __init__(self, id):
        super(GetPassword, self).__init__()
        self.id = int(id)
        self.pwd = self.getPwd().split()[0]
    def getPwd(self):
        conn = pyodbc.connect(Driver=self.driver, Server=self.server, Database=self.database, Trusted_Connection='yes')
        cursor = conn.cursor()
        SQLCommand = "SELECT * FROM [Table] WHERE loginid = ?"
        Values = [self.id]
        query = cursor.execute(SQLCommand, Values)
        for row in query:
            password = row[3]
        conn.commit()
        return password

class EditInfo(SQLServer):
    def __init__(self, id, info):
        super(EditInfo, self).__init__()
        self.id = id
        self.info = info.split()
        self.fullname = ""
        n_fname = int(info[0])
        for i in range (1, n_fname):
            self.fullname = self.fullname + self.info[i] + ' '
        self.fullname = self.fullname + self.info[n_fname]
        self.dob = datetime.datetime.strptime(self.info[n_fname+1], "%Y/%m/%d").date()
        self.editinfo()
    def editinfo(self):
        conn = pyodbc.connect(Driver=self.driver, Server=self.server, Database=self.database, Trusted_Connection='yes')
        cursor = conn.cursor()
        SQLCommand = "UPDATE [Table] SET fullname = ?, dob = ? WHERE loginid = ?;"
        Values = [self.fullname, self.dob, self.id]
        query = cursor.execute(SQLCommand, Values)
        conn.commit()

class EditPassword(SQLServer):
    def __init__(self, id, pwd):
        super(EditPassword, self).__init__()
        self.id = id
        self.pwd = pwd
        self.editPassword()

    def editPassword(self):
        conn = pyodbc.connect(Driver=self.driver, Server=self.server, Database=self.database, Trusted_Connection='yes')
        cursor = conn.cursor()
        SQLCommand = "UPDATE [Table] SET password = ? WHERE loginid = ?;"
        Values = [self.pwd, self.id]
        query = cursor.execute(SQLCommand, Values)
        conn.commit()

class Server:
    def __init__(self, ip, port):
        self.SERVER = ip
        self.PORT = port
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "close"
        self.clients = []
        self.dict_client_id = {}
        self.dict_id_client = {}
        self.dict_id_username = {}
        self.dict_id_fullname = {}
        self.dict_id_active = {}
        self.nicknames = []

    def broadcast(self, msg, nickname):
        message = '{}: {}'.format(nickname, msg)
        for i in range(0, len(self.clients)):
            if self.nicknames[i] != nickname:
                self.clients[i].send(message.encode(self.FORMAT))

    def handle_client(self, client, adr):
        # index = self.clients.index(client)
        # nickname = self.nicknames[index]
        connected = True
        id = -1
        old_clients = []
        username = ""
        crypto = Crypto()
        while connected:
            try:
                msg = client.recv(2048)
                message = msg.decode(self.FORMAT)
                query = message.split()
                if query[0] == self.DISCONNECT_MESSAGE:
                    print(username + " left!")
                    connected = False
                    self.clients.remove(client)

                elif query[0] == "login":
                    if query[1] == "encrypt":
                        query = crypto.decrypt_message(query[2])
                        query = "login " + query
                    else:
                        tmp = query
                        query = "login"
                        for i in range (2,len(tmp)):
                            query = query + ' ' + tmp[i]

                    query = query.split()
                    username = query[1]
                    pwd = query[2]
                    loginStatus = self.login(username, pwd)
                    if loginStatus:
                        client.send("true".encode(self.FORMAT))
                        print(username + " joined!")
                        id = loginStatus
                        self.dict_id_active[id] = False
                        self.dict_client_id[client] = id
                        self.dict_id_client[id] = client
                        self.dict_id_username[id] = username
                        self.dict_id_fullname[id] = self.getFullNameFromInfo(id)
                        # print(self.getUsernamesOnline(client))
                        # print(self.getFullnamesOnline(client, old_clients))
                    else:
                        client.send("false".encode(self.FORMAT))

                elif query[0] == "register":
                    if query[1] == "encrypt":
                        query = crypto.decrypt_message(query[2])
                        query = "register " + query
                    else:
                        tmp = query
                        query = "register"
                        for i in range (2,len(tmp)):
                            query = query + ' '+ tmp[i]
                    query = query.split()
                    n_fname = int(query[1]) + 1
                    fullname = ""
                    for i in range (2, n_fname):
                        fullname = fullname + query[i] + ' '
                    fullname = fullname + query[n_fname]
                    username = query[n_fname+1]
                    password = query[n_fname+2]
                    dob = datetime.datetime.strptime(query[n_fname+3], "%Y/%m/%d").date()
                    if self.register(fullname, username, password, dob):
                        print("New user: " + username + " created!")
                        client.send("true".encode(self.FORMAT))
                    else:
                        client.send("false".encode(self.FORMAT))

                elif query[0] == "getinfo":
                    self.dict_id_active[id] = False
                    print(username + " Get Info")
                    client.send(self.getInfo(id).encode(self.FORMAT))

                elif query[0] == "getusersonline":
                    list = self.getUsernamesOnline(client)
                    if list == "":
                        list = list + "-1"
                    client.send(list.encode(self.FORMAT))

                elif query[0] == "getfullnamesonline":
                    list = self.getFullnamesOnline(client, old_clients)
                    if list == "":
                        list = "-1"
                    client.send(list.encode(self.FORMAT))


                elif query[0] == "getuseronlineinfo":
                    self.dict_id_active[id] = True
                    print(username + " Get List Users online")
                    list = self.get_useronline_info(client, old_clients)
                    if list == "":
                        list = "-1"
                    client.send(list.encode(self.FORMAT))

                elif query[0] == "getmoreuseronlineinfo":
                    self.dict_id_active[id] = True
                    print(username + " Get List More Users online")
                    list = self.get_more_useronline_info(client, old_clients)
                    if list == "":
                        list = "-1"
                    client.send(list.encode(self.FORMAT))

                elif query[0] == "editpassword":
                    if query[1] == "encrypt":
                        query = crypto.decrypt_message(query[2])
                        query = "editpassword " + query
                    else:
                        query = "editpassword " + query[2] + ' ' + query[3]
                    query = query.split()
                    getPwd = GetPassword(id)
                    oldPwd = getPwd.pwd
                    if oldPwd == query[1]:
                        edit = EditPassword(id, str(query[2]))
                        client.send("true".encode(self.FORMAT))
                        print(username + " Updated Password Successfully")
                    else:
                        client.send("false".encode(self.FORMAT))
                        print(username + " Updated Password Fail")

                elif query[0] == "editinfo":
                    info = ""
                    for i in range(1, len(query)):
                        info = info + query[i] + ' '
                    print(username + " Updated Info")
                    edit = EditInfo(id, info)

                elif query[0] == "sendfile":
                    filesize = int(query[1])
                    filename = query[2]
                    filename = "File\\"+filename

                    if path.exists(filename):
                        print(username + " uploaded File: " + str(query[2]) + " Unsuccesfully")
                        client.send("false".encode(self.FORMAT))
                    else:
                        print(username + " uploaded File: " + str(query[2]) + " Succesfully")
                        client.send("true".encode(self.FORMAT))
                        f = open(filename, 'wb')
                        total = 0
                        while 1:
                            if (total < filesize):
                                data = client.recv(1024)
                                f.write(data)
                                total = total + len(data)
                            else:
                                break
                        f.close()


                elif query[0] == "downloadfile":
                    filename = query[1]
                    filename = "File\\"+filename
                    if self.sendFile(filename, client):
                        # print("User: " + str(self.dict_client_id[client]) + " Download File: " + str(filename) + " Successfully")
                        print("A User Download File: " + str(filename) + " Successfully")
                    else:
                        # print("User: " + str(self.dict_client_id[client]) + " Download File: " + str(filename) + " Unsuccessfully")
                        print("A User: Download File: " + str(filename) + " Unsuccessfully")
                        # print("Download fail")

                elif query[0] == "sendmessage":
                    to_id = int(query[1])
                    print("User " + str(id) + " send a message to User " + str(to_id))

                    if self.dict_id_client[to_id] not in self.clients:
                        client.send((str(to_id) + " this_user_is_offline").encode(self.FORMAT))
                    elif not self.dict_id_active[to_id]:
                        client.send((str(to_id) + " this_user_is_not_active").encode(self.FORMAT))
                    else:
                        msg = str(self.dict_client_id[client]) + ' '
                        for i in range (2,len(query)):
                            msg = msg + query[i] + ' '
                        self.dict_id_client[to_id].send(msg.encode(self.FORMAT))

                elif query[0] == "stop_receiving_message":
                    if id > -1:
                        self.dict_id_active[id] = False
                        client.send("stop_receiving_message".encode(self.FORMAT))
                else:
                    client.send("false".encode(self.FORMAT))
            except:
                connected = False
                self.clients.remove(client)
                # self.nicknames.remove(nickname)
                # self.broadcast(nickname, "Disconnected")
                # client.close()
        # client.close()
    def sendFile(self, filename, client):
        if not path.exists(filename):
            client.send("false".encode(self.FORMAT))
            return False

        f = open(filename, "rb")
        filesize = str(os.path.getsize(filename))
        client.send(filesize.encode(self.FORMAT))
        # res = client.recv().decode(self.FORMAT)
        # if res == "false":
        #     return False
        l = f.read(1024)
        client.recv(1024)
        while l:
            client.send(l)
            l = f.read(1024)
        f.close()
        return True

    def getFile(self, client):
        pass
    def getInfo(self, id):
        getinfo = GetInfo(id)
        return getinfo.info

    def get_useronline_info(self, this_client, old_clients):
        list = "listuser "
        for client in self.clients:
            if client == this_client:
                continue
            id = self.dict_client_id[client]
            list = list + str(id) + ' ' + self.getInfo(id) + ' '
            old_clients.append(client)
        return list
    def get_more_useronline_info(self, this_client, old_clients):
        list = "listuser "
        for client in self.clients:
            flag = 1
            if client == this_client:
                continue
            for old_client in old_clients:
                if client == old_client:
                    flag = 0
                    break
            if flag:
                id = self.dict_client_id[client]
                list = list + str(id) + ' ' + self.getInfo(id) + ' '
                old_clients.append(client)

        return list

    def getFullNameFromInfo(self, id):
        info= self.getInfo(id)
        info = info.split()
        n_fname = int(info[0])
        fullname = ""
        for i in range(1, n_fname):
            fullname = fullname + info[i] + ' '
        fullname = fullname + info[n_fname]
        return fullname

    def getUsernamesOnline(self, client):
        users = ""
        for cnt in self.clients:
            if cnt != client:
                users = users + self.dict_id_username[self.dict_client_id[cnt]] + ' '
        return users

    def getFullnamesOnline(self, client, old_clients):
        users = ""
        for cnt in self.clients:
            if cnt != client:
                old_clients.append(cnt)
                fullname = self.dict_id_fullname[self.dict_client_id[cnt]]
                users = users + str(len(fullname.split())) + ' ' + fullname + ' '
        return users

    def login(self, username, password):
        log = Login(username, password)
        if not log.status:
            return False
        return log.id

    def register(self, fullname, username, password, dob):
        reg = Register(fullname, username, password, dob)
        if not reg.status:
            return False
        return True

    def start(self):
        addr = (self.SERVER, self.PORT)
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(addr)
        colorama.init()
        print(colored("Deverloped by Minh Duc ©2020", 'yellow'))
        print("[STARTING] Server is starting....")
        server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            client, adr = server.accept()
            print("Connected with {}".format(str(adr)))
            self.clients.append(client)

            thread = threading.Thread(target=self.handle_client, args=(client, adr))
            thread.start()
            # thread.join()
            print(f"[ACTIVE CONNECTION] {threading.activeCount()-1}")

def startserver():
    SERVER = socket.gethostbyname(socket.gethostname())
    # IP = input("IP: ")
    while True:
        try:
            PORT = int(input("PORT: "))
            # PORT = 5050
            server = Server(SERVER, PORT)
            th = threading.Thread(server.start(), args=())
            # th.setDaemon(True)
            # th.start()
            # pc = multiprocessing.Process(target=server.start())
            # pc.start()
            # pc.join()
            # print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")
            # _thread.start_new_thread(server.start())
            th.daemon = True
            th.start()

        except:
                pass


SERVER = socket.gethostbyname(socket.gethostname())
# IP = input("IP: ")
PORT = int(input("PORT: "))
server = Server(SERVER, PORT)
server.start()


