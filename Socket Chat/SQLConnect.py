import pandas as pd
import pyodbc
import datetime

class SQLServer:
    def __init__(self):
        self.driver = '{ODBC Driver 17 for SQL Server}'
        self.database = "Table"
        self.server = 'MINHDUC'

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

class GetPassword(SQLServer):
    def __init__(self, id):
        super(GetPassword, self).__init__()
        self.id = int(id)
        self.pwd = self.getPwd()
    def getPwd(self):
        conn = pyodbc.connect(Driver=self.driver, Server=self.server, Database=self.database, Trusted_Connection='yes')
        cursor = conn.cursor()
        SQLCommand = "SELECT * FROM [Table] WHERE loginid = ?"
        Values = [self.id]
        query = cursor.execute(SQLCommand, Values)
        for row in query:
            password = row[3]
        print(password)
        conn.commit()
        return password

getPwd = GetPassword(6)
print(getPwd.pwd)
# date = datetime.date(2001,11,24)
# reg = Register("testLap", "test", "test", date)
# if not reg.status:
#     print("Fail")

# log = Login("test","test")
# if not log.status:
#     print("Fail")

# getinfo = GetInfo(4)
# x = getinfo.info.split()
# for i in x:
#     print(i)
#
# info = "5 vy lun khung kho hieu 2001/10/29"
#
# editinfo = EditInfo(4, info)

# editPassword = EditPassword(4,"vykhung")