from PyQt5 import uic,QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
import sqlite3
import re
import user
registerbool=True
regui=uic.loadUi("ui/reg.ui")
homeui=0
imgname="img/pp.jpg"
def check_email(email):
    if len(email) > 7:
        if re.match("^[a-zA-Z][a-zA-Z0-9._]+@[a-zA-Z]{2,8}[.]+[a-zA-Z.]{2,7}$", email)!=None:
            return True
    return False

def check_phone(phone):
    try:
        phone=int(phone)
    except:
        return False
    else:
        phone=str(phone)
        if len(phone)!=10:
            return False
        if phone[0]=='9' or phone[0]=='8' or phone[0]=='7' or phone[0]=='6':
            return True
        else:
            return False


def validate_reg():
    s=True
    fname=regui.fname.text()
    lname = regui.lname.text()
    email = regui.email.text()
    userid = regui.userid.text()
    pwd = regui.pwd.text()
    repwd=regui.repwd.text()
    phonep=regui.phonep.text()
    phones=regui.phones.text()
    acctype=regui.acctype.currentText()
    phoneperr=regui.phoneperr
    phoneserr=regui.phoneserr
    phoneperr.hide()
    phoneserr.hide()
    ferr=regui.fname_error
    ferr.hide()
    eerr=regui.email_error
    eerr.hide()
    iderr=regui.id_error
    iderr.hide()
    pwderr=regui.pwd_error
    pwderr.hide()


    if len(fname)<2:
        ferr.setText("enter valid name")
        ferr.show()
        s=False
    if check_email(email)==False:
        eerr.setText("enter valid email")
        eerr.show()
        s=False
    if len(userid)<7:
        iderr.setText("userid should be more than 7 character")
        iderr.show()
        s=False
    if pwd!=repwd:
        pwderr.setText("password does not match")
        pwderr.show()
        s = False
    if len(pwd)<8:
        pwderr.setText("password should be more than 8 character")
        pwderr.show()
        s=False
    if check_phone(phonep)==False:
        phoneperr.setText("enter valid phone number")
        phoneperr.show()
        s=False
    if check_phone(phones)==False:
        phoneserr.setText("enter valid phone number")
        phoneserr.show()
        s=False

    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute("select * from users where user_id=?", (userid,))
        u = cmd.fetchall()
        cmd.execute("select * from users where email=?", (email,))
        e=cmd.fetchall()
        cmd.execute("select * from user_phone where phone_number=?",(phonep,))
        p=cmd.fetchall()
        cmd.execute("select * from user_phone where phone_number=?", (phones,))
        pp = cmd.fetchall()
    conn.close()
    if len(u)>0:
        iderr.setText("userid not availaible")
        iderr.show()
        s=False
    if len(e)>0:
        eerr.setText("email already registered")
        eerr.show()
        s=False
    if len(p)>0:
        phoneperr.setText("number already registered")
        phoneperr.show()
        s=False
    if len(pp)>0:
        phoneserr.setText("number already registered")
        phoneserr.show()
        s=False

    if phonep==phones:
        phoneserr.setText("enter another phone number")
        phoneserr.show()
        s = False

    if s:
        t=(userid,fname,lname,email,pwd,acctype)
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute("insert into users values(?,?,?,?,?,?)",t)
            cmd.execute("insert into user_phone values(?,?)",(userid,phonep))
            cmd.execute("insert into user_phone values(?,?)", (userid, phones))

            if acctype=="general":
                cmd.execute('''
                insert into gen_account values(?,?)
                ''',(userid,user.perstockprice))
            elif acctype=="professional":
                cmd.execute('''
                insert into pro_account values(?,?)
                ''', (userid,user.peryearprice))

        conn.close()
        user.userlogout()
        user.userlogin(userid)
        user.changeuserbar(homeui)
        uploadimg(userid)
        homeui.status.setText("registered successfully")
        exitb()

def exitb():
    regui.close()
    homeui.show()

def imgload(e):
    global imgname
    a=QWidget()
    imgname=QFileDialog.getOpenFileName(a, "upload image", "imgoptions/", "JPG IMAGE (*.jpg)")
    imgname=imgname[0]
    if imgname=="":
        imgname="img/pp.jpg"
    regui.imgbox.setStyleSheet("background:url("+imgname+");")

def uploadimg(userid):
    global imgname
    pic=open(imgname,"rb")
    userimgname="userimg/"+str(userid)+".jpg"
    userpic=open(userimgname,"wb")
    userpic.write(pic.read())
    pic.close()
    userpic.close()


def reg(hui):
    global homeui
    homeui=hui
    homeui.hide()
    regui.userid.setText("")
    regui.userid.setPlaceholderText("User id")
    regui.userid.setAlignment(QtCore.Qt.AlignCenter)
    regui.userid.setMaxLength(30)
    regui.email.setPlaceholderText("Email")
    regui.email.setAlignment(QtCore.Qt.AlignCenter)
    regui.email.setMaxLength(30)
    regui.fname.setPlaceholderText("First Name")
    regui.fname.setAlignment(QtCore.Qt.AlignCenter)
    regui.fname.setMaxLength(20)
    regui.lname.setPlaceholderText("Last name")
    regui.lname.setAlignment(QtCore.Qt.AlignCenter)
    regui.lname.setMaxLength(20)
    regui.pwd.setPlaceholderText("Password")
    regui.pwd.setAlignment(QtCore.Qt.AlignCenter)
    regui.pwd.setMaxLength(30)
    regui.repwd.setPlaceholderText("Confirm Password")
    regui.repwd.setAlignment(QtCore.Qt.AlignCenter)
    regui.repwd.setMaxLength(30)
    regui.fname.setText("")
    regui.email.setText("")
    regui.lname.setText("")
    regui.pwd.setText("")
    regui.repwd.setText("")
    regui.phonep.setPlaceholderText("Primary Phone")
    regui.phonep.setAlignment(QtCore.Qt.AlignCenter)
    regui.phonep.setMaxLength(10)
    regui.phones.setPlaceholderText("Secondary Phone")
    regui.phones.setAlignment(QtCore.Qt.AlignCenter)
    regui.phones.setMaxLength(10)

    ferr = regui.fname_error
    ferr.hide()
    eerr = regui.email_error
    eerr.hide()
    iderr = regui.id_error
    iderr.hide()
    pwderr = regui.pwd_error
    pwderr.hide()
    phoneperr = regui.phoneperr
    phoneserr = regui.phoneserr
    phoneperr.hide()
    phoneserr.hide()

    regui.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
    regui.repwd.setEchoMode(QtWidgets.QLineEdit.Password)
    regui.imgbox.setStyleSheet("background:url(img/pp.jpg);")
    regui.imgbox.mousePressEvent=imgload
    global registerbool
    if registerbool:
        regui.reg_button.clicked.connect(validate_reg)
        regui.exitbutton.clicked.connect(exitb)
        registerbool=False
    regui.show()



