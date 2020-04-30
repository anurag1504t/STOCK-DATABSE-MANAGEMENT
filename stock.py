from requests_html import HTML,HTMLSession
import sqlite3
import datetime
def stock_search(ssearch):

    try:
        session = HTMLSession()
        web = session.get("http://www.google.com/finance/search?q=" + ssearch)
        element=web.html.find('div .gsrt',first='true')
        data=element.text
        data=list(data)
        try:
            data.remove("(")
            data.remove(")")
            data.remove("%")
        except:
            pass
        try:
            while 1:
                data.remove(",")
        except:
            pass
        data="".join(data)
        data=data.split(' ')
        try:
            price=float(data[0])
        except:
            price=0
        try:
            curr=data[1]
        except:
            curr=""
        try:
            change=data[2]
        except:
            change=0
        else:
            if change[0]=="−":
                change=-float(change[1:])
            else:
                change=float(change[1:])
        try:
            percent=float(data[3])
        except:
            percent=0

        element = web.html.find('.iyjjgb')
        s=""
        for i in range(0,9):
            s=s+element[i].text+" "
        s=list(s)
        try:
            while 1:
                s.remove(",")
        except:
            pass
        s="".join(s)
        s=s.split(" ")
        try:
            openp=float(s[0])
        except:
            openp=0
        try:
            highp=float(s[1])
        except:
            highp=0
        try:
            lowp=float(s[2])
        except:
            lowp=0
        try:
            mcap=s[3]
        except:
            mcap="0"
        try:
            peratio=float(s[4])
        except:
            peratio=0
        try:
            prev=float(s[6])
        except:
            prev=0
        element = web.html.find('.ZxoDOe')[0]
        data=element.text.split('\n')
        try:
            cname=data[1]
        except:
            cname=""
        try:
            scode=data[2]
        except:
            scode=""
        try:
            scode=scode.replace(": ",":")
        except:
            pass
        return [scode,[openp,highp,lowp,prev,curr],[price,change,percent],[cname,mcap,peratio]]
    except:
        return False

def stock_update(scode):
    data=stock_search(scode)
    if data == False:
        return False
    d=datetime.datetime.now()
    d=str(d)[0:-4]
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('select * from stock_analysis where stock_code=?',(data[0],))
        r=cmd.fetchall()
    conn.close()

    if len(r)==1:
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
            update stock_live
            set curr_p=?,abs_change=?,per_change=?,update_time=?
            where stock_code=?
            ''', (data[2][0], data[2][1], data[2][2], d, data[0]))
            cmd.execute('''
            update stock_analysis
            set open_p=?,high_p=?,low_p=?,prev_close=?,update_time=?,currency=?
            where stock_code=?
            ''',(data[1][0],data[1][1],data[1][2],data[1][3],d,data[1][4],data[0]))
            cmd.execute('''
            update company
            set name=?,mkt_cap=?,pe_ratio=?,update_time=?
            where stock_code=?
            ''', ( data[3][0],data[3][1], data[3][2], d,data[0]))
        conn.close()
        return True
    else:
        pass

def stock_add(scode):
    data = stock_search(scode)
    if data == False:
        return False
    d = datetime.datetime.now()
    d = str(d)[0:-4]
    try:
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
                    insert into stock_analysis(stock_code,open_p,high_p,low_p,prev_close,update_time,currency) values(?,?,?,?,?,?,?)
                    ''', (data[0], data[1][0], data[1][1], data[1][2], data[1][3], d, data[1][4]))
            cmd.execute('''
                    insert into stock_live(stock_code,curr_p,abs_change,per_change,update_time) values(?,?,?,?,?)
                    ''', (data[0], data[2][0], data[2][1], data[2][2], d))
            cmd.execute('''
                    insert into company(stock_code,name,mkt_cap,pe_ratio,update_time) values(?,?,?,?,?)
                    ''', (data[0],data[3][0], data[3][1], data[3][2], d))
            cmd.execute('''
                    insert into deal(stock_code,buy,sell) values(?,1,1)
                    ''',(data[0],))
        conn.close()
    except :
        return False
    else:
        return True



def stock_update_result(scode):
    data=stock_search(scode)
    if data == False:
        return False
    d=datetime.datetime.now()
    d=str(d)[0:-4]
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('select * from stock_analysis where stock_code=?',(data[0],))
        r=cmd.fetchall()
    conn.close()
    if len(r)==1:
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
            update stock_live
            set curr_p=?,abs_change=?,per_change=?,update_time=?
            where stock_code=?
            ''', (data[2][0], data[2][1], data[2][2], d, data[0]))
            cmd.execute('''
            update stock_analysis
            set open_p=?,high_p=?,low_p=?,prev_close=?,update_time=?,currency=?
            where stock_code=?
            ''',(data[1][0],data[1][1],data[1][2],data[1][3],d,data[1][4],data[0]))
            cmd.execute('''
            update company
            set name=?,mkt_cap=?,pe_ratio=?,update_time=?
            where stock_code=?
            ''', ( data[3][0],data[3][1], data[3][2], d,data[0]))
        conn.close()

        return data
    else:
        return False

def stock_search_result(scode):
    data=stock_search(scode)
    if data == False:
        return False
    d=datetime.datetime.now()
    d=str(d)[0:-4]
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('select * from stock_analysis where stock_code=?',(data[0],))
        r=cmd.fetchall()
    conn.close()
    if len(r)==1:
        conn = sqlite3.connect("database.db")
        with conn:
            cmd = conn.cursor()
            cmd.execute('''
            update stock_live
            set curr_p=?,abs_change=?,per_change=?,update_time=?
            where stock_code=?
            ''', (data[2][0], data[2][1], data[2][2], d, data[0]))
            cmd.execute('''
            update stock_analysis
            set open_p=?,high_p=?,low_p=?,prev_close=?,update_time=?,currency=?
            where stock_code=?
            ''',(data[1][0],data[1][1],data[1][2],data[1][3],d,data[1][4],data[0]))
            cmd.execute('''
            update company
            set name=?,mkt_cap=?,pe_ratio=?,update_time=?
            where stock_code=?
            ''', ( data[3][0],data[3][1], data[3][2], d,data[0]))
        conn.close()
        return data
    else:
        return data
