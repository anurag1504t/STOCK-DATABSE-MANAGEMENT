from PyQt5 import uic,QtWidgets,QtCore
import sqlite3
import os
import re
import user
import investment
profilebool=True
profileui=uic.loadUi("ui/profile.ui")

homeui=0

def deluser():

    profileui.confirmdel.setText("confirm delete account")
    profileui.delbutton.hide()
    profileui.confirmdel.show()
    profileui.confirmdelbutton.show()
    profileui.canceldel.show()

def delaccount():
    userid=user.getuser()
    user.userlogout()
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        delete from users where user_id=?
        ''',(userid,))
        cmd.execute('''
            delete from investment where user_id=?
            ''', (userid,))
        cmd.execute('''
                delete from user_status where userid=?
                ''', (userid,))
        cmd.execute('''
                delete from user_phone where user_id=?
                ''', (userid,))
        cmd.execute('''
                delete from gen_account where user_id=?
                ''', (userid,))
        cmd.execute('''
                delete from pro_account where user_id=?
                ''', (userid,))
    conn.close()
    os.remove("userimg/"+str(userid)+".jpg")
    user.changeuserbar(homeui)
    homeui.status.setText("account deleted successfully")
    exitb()


def canceldel():
    profileui.delbutton.show()
    profileui.confirmdel.setText("")
    profileui.confirmdel.hide()
    profileui.confirmdelbutton.hide()
    profileui.canceldel.hide()

def exitb():
    profileui.close()
    homeui.status.setText("")
    homeui.show()
def logb():
    user.userlogout()
    user.changeuserbar(homeui)
    homeui.status.setText("logged out successfully")
    exitb()

def invest():
    investment.userstockdata(profileui)

def hidedel():
    profileui.confirmdel.hide()
    profileui.delbutton.show()
    profileui.confirmdelbutton.hide()
    profileui.canceldel.hide()

def showprofile(hui):
    global homeui
    homeui=hui
    homeui.hide()
    conn = sqlite3.connect("database.db")
    userloggedid=user.getuser()
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select * from users where user_id=?
        ''',(userloggedid,))
        r=cmd.fetchone()
        cmd.execute('''
        select * from user_phone where user_id=?
        ''',(userloggedid,))
        p=cmd.fetchall()
    conn.close()
    profileui.delbutton.setText("delete account")
    profileui.fname.setText(r[1])
    profileui.lname.setText(r[2])
    profileui.email.setText(r[3])
    profileui.userid.setText(r[0])
    profileui.acctype.setText(r[5])

    if r[5]=="general":
        profileui.price.setText(user.perstockprice+" per stock")
    elif r[5]=="professional":
        profileui.price.setText(user.peryearprice + " per year")

    phonep=p[0][1]
    phones=p[1][1]
    profileui.phonep.setText(phonep)
    profileui.phones.setText(phones)

    profileui.confirmdel.hide()
    profileui.delbutton.show()
    profileui.confirmdelbutton.hide()
    profileui.confirmdel.setAlignment(QtCore.Qt.AlignCenter)

    imgname="userimg/"+str(userloggedid)+".jpg"
    profileui.imgbox.setStyleSheet("background:url("+imgname+");")

    profileui.canceldel.hide()
    global profilebool
    if profilebool:
        profileui.confirmdelbutton.clicked.connect(delaccount)
        profileui.canceldel.clicked.connect(canceldel)
        profileui.delbutton.clicked.connect(deluser)
        profileui.logoutbutton.clicked.connect(logb)
        profileui.investment.clicked.connect(invest)
        profileui.homebutton.clicked.connect(exitb)
        profilebool=False
    profileui.show()

