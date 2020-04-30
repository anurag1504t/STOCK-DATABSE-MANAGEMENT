from PyQt5 import uic,QtWidgets,QtCore
from PyQt5.QtGui import QIcon, QPixmap
import sqlite3
import user
import stock
import stockdb
import sqlite3
sadd=False
sdel=False
stockdealcode=False
searchstockbool=True
searchui=uic.loadUi("ui/searchstock.ui")
homeui=0


def showdeal():
    global stockdealcode
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select * from deal where stock_code=?
        ''',(stockdealcode,))
        r=cmd.fetchall()
    conn.close()
    r=r[0]

    b=r[1]
    s=r[2]
    if b==1:
        searchui.buydeal.setText("disable buy")
    elif b==0:
        searchui.buydeal.setText("enable buy")
    searchui.buydeal.show()
    if s==1:
        searchui.selldeal.setText("disable sell")
    elif s==0:
        searchui.selldeal.setText("enable sell")
    searchui.selldeal.show()

def hidedeal():
    searchui.buydeal.setText("")
    searchui.selldeal.setText("")
    searchui.buydeal.hide()
    searchui.selldeal.hide()


def loaddata():
    global sadd
    global sdel
    global stockdealcode
    t1=searchui.stockanalysis
    t2=searchui.stocklive
    t3=searchui.stockcompany
    sname=searchui.stockname.text()
    if len(sname)==0:
        searchui.notify.setText("enter stock name")
        searchui.addbutton.hide()
        searchui.delbutton.hide()
        cleartbl()
        hidedeal()
        hideconfirmdel()
        sadd=False
        sdel=False
        stockdealcode = False
        return False
    opt=searchui.option.currentText()
    if opt=="live":
        d=stock.stock_search_result(sname)
    elif opt=="data":
        d=stockdb.search_stock(sname)
    if d==False:
        cleartbl()
        hidedeal()
        searchui.notify.setText("no stock found")
        sadd=False
        sdel=False
        stockdealcode = False
        searchui.addbutton.hide()
        hideconfirmdel()
        searchui.delbutton.hide()
        return False
    else:
        t1.setColumnCount(2)
        t1.setRowCount(5)
        t2.setColumnCount(2)
        t2.setRowCount(3)
        t3.setColumnCount(2)
        t3.setRowCount(2)
        searchui.cname.setText("company name : " + d[3][0])
        searchui.scode.setText("stock code : "+d[0])
        t2.setItem(0, 0, QtWidgets.QTableWidgetItem("current price"))
        t2.setItem(1, 0, QtWidgets.QTableWidgetItem("abs change"))
        t2.setItem(2, 0, QtWidgets.QTableWidgetItem("percent change"))
        t1.setItem(0, 0, QtWidgets.QTableWidgetItem("currency"))
        t1.setItem(1, 0, QtWidgets.QTableWidgetItem("open price"))
        t1.setItem(2, 0, QtWidgets.QTableWidgetItem("high price"))
        t1.setItem(3, 0, QtWidgets.QTableWidgetItem("low price"))
        t1.setItem(4, 0, QtWidgets.QTableWidgetItem("prev closed"))
        t3.setItem(0, 0, QtWidgets.QTableWidgetItem("market capital"))
        t3.setItem(1, 0, QtWidgets.QTableWidgetItem("P/E ratio"))
        t2.setItem(0, 1, QtWidgets.QTableWidgetItem(str(d[2][0])))
        t2.setItem(1, 1, QtWidgets.QTableWidgetItem(str(d[2][1])))
        t2.setItem(2, 1, QtWidgets.QTableWidgetItem(str(d[2][2])))
        t1.setItem(0, 1, QtWidgets.QTableWidgetItem(d[1][4]))
        t1.setItem(1, 1, QtWidgets.QTableWidgetItem(str(d[1][0])))
        t1.setItem(2, 1, QtWidgets.QTableWidgetItem(str(d[1][1])))
        t1.setItem(3, 1, QtWidgets.QTableWidgetItem(str(d[1][2])))
        t1.setItem(4, 1, QtWidgets.QTableWidgetItem(str(d[1][3])))
        t3.setItem(0, 1, QtWidgets.QTableWidgetItem(d[3][1]))
        t3.setItem(1, 1, QtWidgets.QTableWidgetItem(str(d[3][2])))
        searchui.notify.setText("")
        if neg(d[2][1]):
            searchui.changeimg.setPixmap(QPixmap('img/down.jpg'))
            searchui.changeimg.show()
        else:
            searchui.changeimg.setPixmap(QPixmap('img/up.jpg'))
            searchui.changeimg.show()
        sadd=d[0]
        sdel=d[0]
        stockdealcode = d[0]
        if user.admincheck():
            checkstock(d[0])
        return True

def neg(d):
    if d<0:
        return True
    else:
        return False

def cleartbl():
    searchui.scode.setText("")
    searchui.cname.setText("")
    searchui.changeimg.hide()
    t1 = searchui.stockanalysis
    t2 = searchui.stocklive
    t3 = searchui.stockcompany
    t1.setRowCount(0)
    t1.setColumnCount(0)
    t2.setRowCount(0)
    t2.setColumnCount(0)
    t3.setRowCount(0)
    t3.setColumnCount(0)

def checkstock(sname):
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''select stock_code from stock_analysis 
        where stock_code=?
        ''',(sname,))
        r=cmd.fetchall()
    conn.close()
    if len(r)>0:
        searchui.addbutton.hide()
        showdeal()
        searchui.delbutton.show()
        hideconfirmdel()
    else:
        searchui.addbutton.show()
        searchui.delbutton.hide()
        hideconfirmdel()

def endp():
    searchui.close()
    homeui.status.setText("")
    homeui.show()

def addstock():
    global sadd
    r=stock.stock_add(sadd)
    if r:
        searchui.notify.setText("stock added successfully")
        searchui.addbutton.hide()
    else:
        searchui.notify.setText("error adding stock")
        searchui.addbutton.hide()
    checkstock(sadd)

def delstock():
    searchui.confirmdel.setText("confirm delete stock")
    searchui.delbutton.hide()
    searchui.confirmdel.show()
    searchui.confirmdelbutton.show()
    searchui.canceldel.show()

def deletestock():
    global sdel
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        delete from stock_analysis where stock_code=?
        ''',(sdel,))
        cmd.execute('''
            delete from stock_live where stock_code=?
            ''', (sdel,))
        cmd.execute('''
            delete from company where stock_code=?
            ''', (sdel,))
        cmd.execute('''
                delete from investment where stock_code=?
                ''', (sdel,))
        cmd.execute('''
                delete from deal where stock_code=?
                ''', (sdel,))

    conn.close()
    searchui.notify.setText("stock deleted successfully")
    checkstock(sdel)
    searchui.confirmdel.hide()
    searchui.confirmdelbutton.hide()
    searchui.canceldel.hide()

def hideconfirmdel():
    searchui.confirmdel.setText("")
    searchui.confirmdel.hide()
    searchui.confirmdelbutton.hide()
    searchui.canceldel.hide()


def canceldel():
    searchui.delbutton.show()
    searchui.confirmdel.setText("")
    searchui.confirmdel.hide()
    searchui.confirmdelbutton.hide()
    searchui.canceldel.hide()

def togglebuy():
    global stockdealcode
    conn=sqlite3.connect("database.db")
    if searchui.buydeal.text()=="enable buy":
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
            update deal
            set buy=1 where stock_code=?
            ''',(stockdealcode,))
        conn.close()
        searchui.buydeal.setText("disable buy")
    elif searchui.buydeal.text()=="disable buy":
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
                    update deal
                    set buy=0 where stock_code=?
            ''', (stockdealcode,))
        conn.close()
        searchui.buydeal.setText("enable buy")

def togglesell():
    global stockdealcode
    if searchui.selldeal.text()=="enable sell":
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
            update deal
            set sell=1 where stock_code=?
            ''',(stockdealcode,))

        conn.close()
        searchui.selldeal.setText("disable sell")
    elif searchui.selldeal.text()=="disable sell":
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
                    update deal
                    set sell=0 where stock_code=?
                    ''', (stockdealcode,))
        conn.close()
        searchui.selldeal.setText("enable sell")
def stocksearch(hui):
    global homeui
    homeui=hui
    homeui.hide()
    hidedeal()
    searchui.notify.setAlignment(QtCore.Qt.AlignCenter)
    searchui.confirmdel.setAlignment(QtCore.Qt.AlignCenter)
    searchui.stockname.setPlaceholderText("search stock")
    searchui.stockname.setAlignment(QtCore.Qt.AlignCenter)
    searchui.stockname.setText("")
    searchui.notify.setText("")
    searchui.addbutton.hide()
    searchui.confirmdel.hide()
    searchui.delbutton.hide()
    searchui.buydeal.hide()
    searchui.selldeal.hide()
    searchui.canceldel.hide()
    cleartbl()
    searchui.confirmdelbutton.hide()
    global searchstockbool
    if searchstockbool:
        searchui.selldeal.clicked.connect(togglesell)
        searchui.buydeal.clicked.connect(togglebuy)
        searchui.confirmdelbutton.clicked.connect(deletestock)
        searchui.canceldel.clicked.connect(canceldel)
        searchui.delbutton.clicked.connect(delstock)
        searchui.homebutton.clicked.connect(endp)
        searchui.addbutton.clicked.connect(addstock)
        searchui.searchbutton.clicked.connect(loaddata)
        searchstockbool=False
    searchui.show()