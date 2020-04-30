import sqlite3
clientid="pystockclient1"
clientemail="pythonstockproject@gmail.com"
clientpassword="DBMStockSProject"
adminid='admin'

perstockprice="2 USD"
peryearprice="50 USD"

def userlogcheck():
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select * from user_status where clientid=?
        ''',(clientid,))
        r=cmd.fetchall()
    conn.close()
    if len(r)==1:
        return True
    else:
        return False


def userlogin(userid):
    if not userlogcheck():
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
            insert into user_status(clientid,userid)
            values(?,?)
            ''',(clientid,userid))
        conn.close()
        return True
    else:
        return False

def changeuserbar(homeui):
    if userlogcheck():
        homeui.logbutton.setText("logout")
        homeui.regbutton.hide()
        homeui.profile.show()
        #homeui.dealbutton.show()
        homeui.userid.setText(getuser())
    else:
        homeui.regbutton.show()
        homeui.userid.setText("guest")
        homeui.logbutton.setText("login")
        homeui.profile.hide()
        #homeui.dealbutton.hide()

def userlogout():
    if userlogcheck():
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
            delete from user_status
            where clientid=?
            ''',(clientid,))
        conn.close()
        return True
    else:
        return False

def getuser():
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
            select * from user_status where clientid=?
            ''', (clientid,))
        r = cmd.fetchall()
    conn.close()
    if len(r) == 1:
        r=r[0]
        return r[1]
    else:
        return False

def getuserdetail(userid):
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select * from users where user_id=?
        ''',(userid,))
        r=cmd.fetchone()
    conn.close()
    return list(r)

def getuseremail():
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
                select * from user_status where clientid=?
                ''', (clientid,))
        r = cmd.fetchall()
    conn.close()
    if len(r) == 1:
        r = r[0][1]
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''select * from users where user_id=?''',(r,))
            r=cmd.fetchall()
        conn.close()
        r=r[0][3]
        return r
    else:
        return False

def admincheck():
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select * from user_status where clientid=? and userid=?
        ''',(clientid,adminid))
        r=cmd.fetchall()
    conn.close()
    if len(r)==1:
        return True
    else:
        return False