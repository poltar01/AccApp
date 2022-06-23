from kivy.uix.screenmanager import Screen,SlideTransition
from kivy.app import App
import mysql.connector
from kivymd.uix.screen import MDScreen
import pytz
from datetime import datetime

# con = mysql.connector.connect(
#     user = "sql11500459",
#     password = "hbKelUx9dX",
#     host = "sql11.freemysqlhosting.net",
#     database = "sql11500459",
#     auth_plugin='mysql_native_password'
# )

con = mysql.connector.connect(
    user = "root",
    password = "",
    host = "localhost",
    database = "accounting_db",
    auth_plugin='mysql_native_password'
)

cursor = con.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS araba_customers (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL ,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ekmek_price FLOAT(24) NOT NULL,
        debit FLOAT(24) DEFAULT 0 NOT NULL
        )""")
con.commit()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(255) NOT NULL,
        permission VARCHAR(50) NOT NULL,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        """)
# cursor.execute(f"""
#         INSERT INTO users (username,password,permission) VALUES ("maya01","ma123","maya")
# """)
con.commit()
cursor.close()



class LoginScreen(MDScreen):

       
    def doLogin(self,usernameInput,passwordInput):
        cursor = con.cursor()
        cursor.execute(f"SELECT permission FROM users WHERE username = '{usernameInput}' AND password ='{passwordInput}'")
        user_perm = cursor.fetchone()
        if user_perm != None:
            print(user_perm[0])
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = f'{user_perm[0]}_screen'
        else:
            print("!!! HATALI GİRİŞ !!!")



    def resetForm(self):
        self.ids['username'].text = ""
        self.ids['password'].text = ""
