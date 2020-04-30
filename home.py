from PyQt5 import uic,QtWidgets,QtCore
app=QtWidgets.QApplication([])
homeui = uic.loadUi("ui/home.ui")
import login
import register
import user
import searchdb
import profile
import livestock
import dealing
import searchstock

def log():
    if user.userlogcheck():
        user.userlogout()
        user.changeuserbar(homeui)
        homeui.status.setText("logged out successfully")
    else:
        login.login(homeui)

def reg():
    register.reg(homeui)

def prof():
    profile.showprofile(homeui)

def sdata():
    livestock.stocklive(homeui)

def stksearch():
    searchstock.stocksearch(homeui)

def stockdbsearch():
    searchdb.searchdb(homeui)

def deal():
    if user.userlogcheck():
        homeui.status.setText("")
        dealing.dealing(homeui)
    else:
        homeui.status.setText("login to buy and sell stocks")

def hidnotify():
    homeui.status.setText("")

user.changeuserbar(homeui)
homeui.logbutton.clicked.connect(log)
homeui.regbutton.clicked.connect(reg)
homeui.stockdata.clicked.connect(sdata)
homeui.stocksearch.clicked.connect(stksearch)
homeui.profile.clicked.connect(prof)
homeui.searchdbbutton.clicked.connect(stockdbsearch)
homeui.dealbutton.clicked.connect(deal)
homeui.exitbutton.clicked.connect(exit)
homeui.status.setAlignment(QtCore.Qt.AlignCenter)
homeui.userid.setAlignment(QtCore.Qt.AlignCenter)

homeui.show()
app.exec()