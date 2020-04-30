from PyQt5 import uic,QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QPushButton,QButtonGroup
import sqlite3
import user
import stock
import stockdb
import sqlite3

searchdbbool=True

dbsearchui=uic.loadUi("ui/dbsearchstock.ui")
homeui=0

def loaddata(curr,sortparameter,order):
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
            select A.stock_code from stock_analysis as A,stock_live as B ,company as C
            where A.stock_code=B.stock_code and A.stock_code=C.stock_code
            and A.currency=? order by 
            '''+sortparameter+" "+order,(curr,))
        r = cmd.fetchall()
    conn.close()
    tbl = dbsearchui.datatable
    tbl.setRowCount(len(r) + 1)
    tbl.setColumnCount(11)
    for i in range(1,len(r)+1):
        sl=stockdb.search_stock_live(r[i-1][0])
        sa=stockdb.search_stock_analysis(r[i-1][0])
        sc=stockdb.search_company(r[i-1][0])
        tbl.setItem(i,0,QtWidgets.QTableWidgetItem(r[i-1][0]))
        for j in range(0,3):
            tbl.setItem(i,j+1,QtWidgets.QTableWidgetItem(str(sl[j+1])))
            tbl.item(i, j+1).setTextAlignment(QtCore.Qt.AlignCenter)
            tbl.item(i, j+1).setBackground(QtGui.QColor(149, 181, 157))
        tbl.item(i, 0).setBackground(QtGui.QColor(171, 181, 164))
        for j in range(0,4):
            tbl.setItem(i,j+4,QtWidgets.QTableWidgetItem(str(sa[j+1])))
            tbl.item(i, j+4).setTextAlignment(QtCore.Qt.AlignCenter)
            tbl.item(i, j+4).setBackground(QtGui.QColor(149, 181, 157))
        for j in range(0,3):
            tbl.setItem(i,j+8,QtWidgets.QTableWidgetItem(str(sc[j+1])))
            tbl.item(i,j+8).setTextAlignment(QtCore.Qt.AlignCenter)
            tbl.item(i, j+8).setBackground(QtGui.QColor(149, 181, 157))




def endp():
    dbsearchui.close()
    dbsearchui.currvalue.clear()
    homeui.status.setText("")
    homeui.show()


bval = ['stock code', 'current price', 'abs change', 'per change', 'open price', 'high price',
            'low price', 'prev close', 'company',
            'market capital', 'pe ratio']
rval = ['stock_code', 'curr_p', 'abs_change', 'per_change', 'open_p', 'high_p',
            'low_p', 'prev_close', 'name',
            'mkt_cap', 'pe_ratio']
def getcommand(btngrp):
    global bval
    global rval
    btn = btngrp.checkedButton()
    c = btn.text()
    btn.setChecked(False)
    c=c.split(" ")
    i=c[len(c)-1]
    c.remove(i)
    c=" ".join(c)

    for j in range(0,len(bval)):
        if c==bval[j]:

            if c in ['stock code','open price', 'high price','low price', 'prev close']:
                op="A."+rval[j]
            elif c in [ 'current price', 'abs change', 'per change']:
                op="B."+rval[j]
            elif c in ['company','market capital', 'pe ratio']:
                op="C."+rval[j]
            else:
                return False

            if i=="^":
                loaddata(dbsearchui.currvalue.currentText(),op,"desc")
                btn.setText(c+" V")
                return True
            elif i=="V":
                loaddata(dbsearchui.currvalue.currentText(),op,"asc")
                btn.setText(c+" ^")
                return True
        else :
            continue;
    return False

def loadbutton():
    tbl=dbsearchui.datatable
    tbl.setRowCount(1)
    tbl.setColumnCount(11)
    bval = ['stock code ^', 'current price ^', 'abs change ^', 'per change ^', 'open price ^',
            'high price ^', 'low price ^', 'prev close ^', 'company ^',
            'market capital ^', 'pe ratio ^']
    btn_grp = QButtonGroup()
    btn_grp.setExclusive(True)
    for i in range(0,11):
        btn=QPushButton()
        btn.setText(bval[i])
        btn.setCheckable(True)
        btn.setChecked(False)
        btn.setStyleSheet('''
        background-color:rgb(28,130,255);
        font-variant:small-caps;
        font-size:18px;
        ''')

        btn.clicked.connect(lambda: getcommand(btn_grp))
        tbl.setCellWidget(0, i, btn)
        btn_grp.addButton(btn)
    return btn_grp


def currload():
    cbox=dbsearchui.currvalue
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select distinct currency from stock_analysis order by currency
        ''')
        r=cmd.fetchall()
    conn.close()
    for i in range(len(r)):
        c=r[i][0]
        cbox.addItem(c)

def searchdb(hui):
    global homeui
    homeui=hui
    homeui.hide()
    loadbutton()
    currload()
    curr=dbsearchui.currvalue
    loaddata(curr.currentText(), "C.name", "asc")
    global searchdbbool
    if searchdbbool:
        dbsearchui.currvalue.activated.connect(lambda:loaddata(curr.currentText(),"A.stock_code","asc"))
        dbsearchui.homebutton.clicked.connect(endp)
        searchdbbool=False
    dbsearchui.show()
