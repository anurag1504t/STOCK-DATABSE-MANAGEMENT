from PyQt5 import uic,QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QButtonGroup
import sqlite3
import user
homeui=False
dealui=uic.loadUi("ui/dealing.ui")
dealingbool=True
def hid():
    dealui.dealbutton.hide()
    dealui.amount.hide()

    dealui.detail.hide()
def show():
    dealui.dealbutton.show()
    dealui.amount.setText("")
    dealui.amount.show()
    dealui.detail.show()
    dealui.notify.setText("")

scode=0
task=0

def deal():
    global task
    if task==1:
        buy()
    elif task==2:
        sell()

def getcommand(btngrp):
    global scode
    global task
    btn=btngrp.checkedButton()
    c=btn.toolTip()
    btn.setChecked(False)
    userid=user.getuser()
    t=c.split(" ")
    scode=t[1]
    dealui.detail.setText(c)
    if t[0]=="buy":
        show()
        task=1
    elif t[0]=="sell":
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
                select * from investment where user_id=? and stock_code=?
                ''', (userid, scode))
            r = cmd.fetchall()
        conn.close()
        if len(r)!=0:
            show()
            task=2
        else :
            dealui.notify.setText("no stocks to sell")
            task=0
            hid()



def buy():
    global scode
    userid=user.getuser()
    try:
        num=int(dealui.amount.text())
    except:
        num=0
        dealui.notify.setText("enter value.")
        return False
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select * from investment where user_id=? and stock_code=?
        ''',(userid,scode))
        r=cmd.fetchall()
        if len(r)==0:
            cmd.execute('''
            insert into investment(user_id,stock_code,count) values(?,?,?)
            ''',(userid,scode,num))

        else:
            count=int(r[0][2])
            cmd.execute('''
            update investment
            set count=? where user_id=? and stock_code=?
            ''',(count+num,userid,scode))
    conn.close()

    hid()
    dealui.notify.setText("successfully bought stocks")
    loadtable()
    return True

def sell():
    global scode
    userid=user.getuser()
    try:
        num=int(dealui.amount.text())
    except:
        num=0
        dealui.notify.setText("enter valid value.")
        return False
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select * from investment where user_id=? and stock_code=?
        ''',(userid,scode))
        r=cmd.fetchall()
        if len(r)==0:
            return False
        else:
            count=int(r[0][2])
            if num>count:
                dealui.notify.setText("not enough stock to sell")
                return False
            elif num<count:
                cmd.execute('''
                update investment
                set count=? where user_id=? and stock_code=?
                ''',(count-num,userid,scode))
                conn.commit()
            elif num==count:
                cmd.execute('''
                delete from investment
                where user_id=? and stock_code=?
                ''',(userid,scode))
    conn.close()

    hid()
    dealui.notify.setText("successfully sold stocks")
    loadtable()
    return True

def loadtable():
    tbl=dealui.stocktable
    userid=user.getuser()
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select * from stock_live
        order by stock_code
        ''')
        d=cmd.fetchall()
    conn.close()
    n=len(d)

    tbl.setRowCount(n+1)
    tbl.setColumnCount(7)
    tbl.setItem(0,0,QtWidgets.QTableWidgetItem("stock code"))
    tbl.setItem(0, 1, QtWidgets.QTableWidgetItem("current price"))
    tbl.setItem(0, 2, QtWidgets.QTableWidgetItem("abs change"))
    tbl.setItem(0, 3, QtWidgets.QTableWidgetItem("per change"))
    tbl.setItem(0, 4, QtWidgets.QTableWidgetItem("buy"))
    tbl.setItem(0, 5, QtWidgets.QTableWidgetItem("sell"))
    tbl.setItem(0, 6, QtWidgets.QTableWidgetItem("own"))
    for i in range(0,7):
        tbl.item(0, i).setTextAlignment(QtCore.Qt.AlignCenter)
        tbl.item(0, i).setBackground(QtGui.QColor(181, 115, 81))
        tbl.item(0, i).setForeground(QtGui.QColor(255, 255, 255))
    btn_grp = QButtonGroup()
    btn_grp.setExclusive(True)
    for i in range(0,n):
        for j in range(0,4):
            tbl.setItem(i+1, j, QtWidgets.QTableWidgetItem(str(d[i][j])))
            tbl.item(i+1, j).setTextAlignment(QtCore.Qt.AlignCenter)
            tbl.item(i+1, j).setBackground(QtGui.QColor(149, 181, 157))
        tbl.item(i+1, 0).setBackground(QtGui.QColor(171, 181, 164))

        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
                select * from deal where stock_code=?
                ''',(d[i][0],))
            option=cmd.fetchall()
        conn.close()
        buyoption=option[0][1]
        selloption=option[0][2]

        btn = QPushButton()
        btn.setText('buy')
        btn.setStyleSheet("background-color: rgb(255, 87, 98);font-size:20px;font-variant:small-caps;")
        btn.setToolTip("buy "+d[i][0])
        btn.setCheckable(True)
        btn.setChecked(False)
        btn.clicked.connect(lambda: getcommand(btn_grp))
        if buyoption==1:
            tbl.setCellWidget(i+1, 4, btn)
        else:
            tbl.setCellWidget(i+1, 4, btn)
            btn.setDisabled(True)
        btn_grp.addButton(btn)

        btn = QPushButton()
        btn.setText('sell')
        btn.setStyleSheet("background-color:rgb(90, 181, 70);font-size:20px;font-variant:small-caps;")
        btn.setToolTip("sell "+d[i][0])
        btn.setCheckable(True)
        btn.setChecked(False)
        btn.clicked.connect(lambda: getcommand(btn_grp))
        if selloption==1:
            tbl.setCellWidget(i+1, 5, btn)
        else:
            tbl.setCellWidget(i + 1, 5, btn)
            btn.setDisabled(True)
        btn_grp.addButton(btn)

        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
            select count from investment where user_id=? and stock_code=?
            ''',(userid,d[i][0]))
            c=cmd.fetchall()
        conn.close()
        if len(c)==0:
            scount=0
        else:
            scount=c[0][0]
        tbl.setItem(i + 1, 6, QtWidgets.QTableWidgetItem(str(scount)))
        tbl.item(i + 1, 6).setTextAlignment(QtCore.Qt.AlignCenter)
        tbl.item(i + 1, 6).setBackground(QtGui.QColor(253,174,95))



def endp():
    dealui.close()
    homeui.status.setText("")
    homeui.show()


def dealing(hui):
    global homeui
    homeui=hui
    homeui.hide()
    dealui.notify.setText("")
    dealui.detail.setAlignment(QtCore.Qt.AlignRight)
    hid()
    loadtable()
    global dealingbool
    if dealingbool:
        dealui.dealbutton.clicked.connect(deal)
        dealui.homebutton.clicked.connect(endp)
        dealingbool=False
    dealui.show()