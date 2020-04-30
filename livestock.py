from PyQt5 import uic,QtWidgets,QtCore,QtGui
import sqlite3
import user
import stock
import sqlite3
import datetime

livestockbool=True

stockui=uic.loadUi("ui/livestock.ui")
homeui=False

def stocklive(hui):
    global homeui
    homeui = hui

    homeui.hide()
    global livestockbool
    if livestockbool:
        stockui.homebutton.clicked.connect(endp)
        stockui.updatebutton.clicked.connect(loaddata)
        livestockbool=False
    stockui.show()
    stockui.stocktbl.show()
    loaddata()


def loaddata():
    global homeui
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select stock_code from stock_analysis;
        ''')
        r=cmd.fetchall()
    conn.close()
    tbl=stockui.stocktbl
    tbl.setRowCount(len(r)+1)
    tbl.setColumnCount(12)
    tbl.setItem(0,0,QtWidgets.QTableWidgetItem("stock code"))
    tbl.setItem(0,1, QtWidgets.QTableWidgetItem("current price"))
    tbl.setItem(0,2, QtWidgets.QTableWidgetItem("abs change"))
    tbl.setItem(0,3, QtWidgets.QTableWidgetItem("percent change"))
    tbl.setItem(0,4, QtWidgets.QTableWidgetItem("currency"))
    tbl.setItem(0,5, QtWidgets.QTableWidgetItem("open price"))
    tbl.setItem(0,6, QtWidgets.QTableWidgetItem("high price"))
    tbl.setItem(0,7, QtWidgets.QTableWidgetItem("low price"))
    tbl.setItem(0,8, QtWidgets.QTableWidgetItem("prev closed"))
    tbl.setItem(0,9, QtWidgets.QTableWidgetItem("company"))
    tbl.setItem(0,10, QtWidgets.QTableWidgetItem("market capital"))
    tbl.setItem(0,11, QtWidgets.QTableWidgetItem("P/E ratio"))
    for i in range(0,12):
        tbl.item(0, i).setTextAlignment(QtCore.Qt.AlignCenter)
        tbl.item(0, i).setBackground(QtGui.QColor(181, 115, 81))
        tbl.item(0, i).setForeground(QtGui.QColor(255, 255, 255))

    for i in range(1,len(r)+1):
        d=stock.stock_update_result(r[i-1][0])
        if d != False:
            tbl.setItem(i, 0, QtWidgets.QTableWidgetItem(d[0]))
            tbl.setItem(i, 1, QtWidgets.QTableWidgetItem(str(d[2][0])))
            tbl.setItem(i, 2, QtWidgets.QTableWidgetItem(str(d[2][1])))
            tbl.setItem(i, 3, QtWidgets.QTableWidgetItem(str(d[2][2])))
            tbl.setItem(i, 4, QtWidgets.QTableWidgetItem(d[1][4]))
            tbl.setItem(i, 5, QtWidgets.QTableWidgetItem(str(d[1][0])))
            tbl.setItem(i, 6, QtWidgets.QTableWidgetItem(str(d[1][1])))
            tbl.setItem(i, 7, QtWidgets.QTableWidgetItem(str(d[1][2])))
            tbl.setItem(i, 8, QtWidgets.QTableWidgetItem(str(d[1][3])))
            tbl.setItem(i, 9, QtWidgets.QTableWidgetItem(d[3][0]))
            tbl.setItem(i, 10, QtWidgets.QTableWidgetItem(d[3][1]))
            tbl.setItem(i, 11, QtWidgets.QTableWidgetItem(str(d[3][2])))
            tbl.item(i, 0).setTextAlignment(QtCore.Qt.AlignCenter)
            tbl.item(i, 0).setBackground(QtGui.QColor(171, 181, 164))
            for j in range(1,12):
                tbl.item(i, j).setTextAlignment(QtCore.Qt.AlignCenter)
                tbl.item(i, j).setBackground(QtGui.QColor(149, 181, 157))

    d=datetime.datetime.now()
    stockui.dateshow.setText("update time : "+str(d)[0:-4])


def endp():
    stockui.hide()
    homeui.status.setText("")
    homeui.show()




