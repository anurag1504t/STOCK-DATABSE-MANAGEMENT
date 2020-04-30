from PyQt5 import uic,QtWidgets,QtGui,QtCore
import sqlite3
import user
import stock
import stockdb
import profile
import sqlite3
import smtplib
from email.message import EmailMessage
investmentbool=True
inui=uic.loadUi("ui/userstock.ui")
profileui=0

def loaduserstock():
    u=user.getuser()
    conn = sqlite3.connect("database.db")
    inui.emailmsg.setText("")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select * from investment where user_id=?
        order by count desc
        ''',(u,))
        r=cmd.fetchall()
    conn.close()
    tbl=inui.datatable
    tbl.setRowCount(len(r)+1)
    tbl.setColumnCount(4)

    tbl.setItem(0,0,QtWidgets.QTableWidgetItem("Stock Code"))
    tbl.setItem(0, 1, QtWidgets.QTableWidgetItem("Count"))
    tbl.setItem(0, 2, QtWidgets.QTableWidgetItem("Current Price"))
    tbl.setItem(0, 3, QtWidgets.QTableWidgetItem("Currency"))
    tbl.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
    tbl.item(0, 1).setTextAlignment(QtCore.Qt.AlignCenter)
    tbl.item(0, 2).setTextAlignment(QtCore.Qt.AlignCenter)
    tbl.item(0, 3).setTextAlignment(QtCore.Qt.AlignCenter)
    tbl.item(0, 0).setBackground(QtGui.QColor(181,115,81))
    tbl.item(0, 1).setBackground(QtGui.QColor(181,115,81))
    tbl.item(0, 2).setBackground(QtGui.QColor(181, 115, 81))
    tbl.item(0, 3).setBackground(QtGui.QColor(181, 115, 81))
    tbl.item(0, 0).setForeground(QtGui.QColor(255,255,255))
    tbl.item(0, 1).setForeground(QtGui.QColor(255, 255, 255))
    tbl.item(0, 2).setForeground(QtGui.QColor(255, 255, 255))
    tbl.item(0, 3).setForeground(QtGui.QColor(255, 255, 255))
    for i in range(1,len(r)+1):
        d=r[i-1]
        tbl.setItem(i, 0, QtWidgets.QTableWidgetItem(d[1]))
        tbl.setItem(i, 1, QtWidgets.QTableWidgetItem(str(d[2])))
        tbl.setItem(i, 2, QtWidgets.QTableWidgetItem(str(stockdb.search_stock_price(d[1]))))
        tbl.setItem(i, 3, QtWidgets.QTableWidgetItem(str(stockdb.search_stock_curr(d[1]))))
        tbl.item(i, 0).setTextAlignment(QtCore.Qt.AlignCenter)
        tbl.item(i, 1).setTextAlignment(QtCore.Qt.AlignCenter)
        tbl.item(i, 2).setTextAlignment(QtCore.Qt.AlignCenter)
        tbl.item(i, 3).setTextAlignment(QtCore.Qt.AlignCenter)
        tbl.item(i, 0).setBackground(QtGui.QColor(171,181,164))
        tbl.item(i, 1).setBackground(QtGui.QColor(149,181,157))
        tbl.item(i, 2).setBackground(QtGui.QColor(149, 181, 157))
        tbl.item(i, 3).setBackground(QtGui.QColor(149, 181, 157))

def endp():
    inui.close()
    profile.hidedel()
    profileui.show()

def mailstockdata():
    u=user.getuseremail()
    msg=EmailMessage()
    msg['Subject']='stock investment details'
    msg['From']=user.clientemail
    msg['To']=user.getuseremail()

    userid=user.getuser()
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select * from investment where user_id=?
        ''',(userid,))
        r=cmd.fetchall()
    conn.close()
    m="your stock investment details are :\n\n\n"
    m=m+str("user id : "+userid+"\n\n")
    if len(r)==0:
        m="no stocks owned"
    else:
        for data in r:
            m=m+"stock code : "+str(data[1])+"\n"
            cdetail=stockdb.search_company(data[1])
            cname=cdetail[1]
            m=m+"company : "+cname+"\n"
            m=m+"no. of stock : "+str(data[2])+"\n\n"

    msg.set_content(m)

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:

        smtp.login(user.clientemail,user.clientpassword)

        smtp.send_message(msg)

    inui.emailmsg.setText("details sent to your registered email")


def userstockdata(profui):
    global profileui
    profileui=profui
    profileui.hide()
    global investmentbool
    if investmentbool:
        inui.profile.clicked.connect(endp)
        inui.maildata.clicked.connect(mailstockdata)
        investmentbool=False
    loaduserstock()
    inui.show()