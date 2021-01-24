import mysql.connector
import datetime
from kivy.logger import Logger
import hashlib

con = mysql.connector.connect(user='root', password='sarojini', host='localhost', database='patientDB',
                              port=3306)
dat = datetime.date.today()


class DataBase:

    def get_user(self, phone):
        cur = con.cursor()
        cur.execute("SELECT * FROM patientdata WHERE phone = %s", (phone,))  # CHECKS IF USERNAME EXSIST
        row = cur.fetchone()
        cur.close()
        return row

    def add_user(self, name, password, phone, status, address):
        cur = con.cursor()
        Logger.info("strated query started")
        hash_pass = hashlib.md5(password.encode('utf8')).hexdigest()
        cur.execute("SELECT COUNT(1) FROM patientdata WHERE phone = %s", (phone,)) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            return '<a href="/signup">User already exist. Please add another userrname</a>'
        else:
            # Save edits
            Logger.info("Insert query started")
            cur.execute("""INSERT INTO patientdata(name, password, phone, status, address) VALUES(%s, %s, %s,%s,%s)""",
                (name, hash_pass, phone, status, address))
            con.commit()
        cur.close()

    def validate(self, phone, password):

        hash_pass = hashlib.md5(password.encode('utf8')).hexdigest()
        userdetail = self.get_user(phone)
        if userdetail is not None:
            return userdetail[3] == hash_pass
        else:
            return False

    def getHelpline(self):
        cur = con.cursor()
        cur.execute("SELECT * FROM HelpCenter_List") # Fetch helpcenter list
        rows = cur.fetchall()
        cur.close()
        return rows

