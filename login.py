from PyQt5 import uic,QtWidgets,QtCore
import user
import sqlite3
loginbool=True
loginui=uic.loadUi("ui/login.ui")
homeui=0
def validate_id():
    userid=loginui.userid.text()
    pwd=loginui.pwd.text()
    err=loginui.err
    err.hide()
    s=True
    if len(userid)==0:
        err.setText("enter userid")
        err.show()
        s= False
        return False
    if len(pwd)==0:
        err.setText("enter password")
        err.show()
        s = False
        return False
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select * from users where user_id=?
        ''',(userid,))
        r=cmd.fetchall()
    conn.close()
    if len(r)==0:
        err.setText("no account found.")
        err.show()
        s=False
        return False
    else:
        u=r[0]
        if pwd!=u[4]:
            err.setText("password incorrect.")
            err.show()
            s=False
            return False
    if s:
        user.userlogout()
        user.userlogin(userid)
        user.changeuserbar(homeui)
        homeui.status.setText("logged in successfully")
        exitb()

def exitb():
    loginui.close()
    homeui.show()

def login(hui):
    global homeui
    homeui=hui
    homeui.hide()
    loginui.userid.setText("")
    loginui.userid.setPlaceholderText("User id")
    loginui.pwd.setPlaceholderText("Password")
    loginui.userid.setAlignment(QtCore.Qt.AlignCenter)
    loginui.pwd.setAlignment(QtCore.Qt.AlignCenter)
    loginui.pwd.setText("")
    loginui.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
    err = loginui.err
    err.hide()
    global loginbool
    if loginbool:
        loginui.logbutton.clicked.connect(validate_id)
        loginui.exitbutton.clicked.connect(exitb)
        loginbool=False
    loginui.show()
