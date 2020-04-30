import sqlite3

def search_stock_analysis(scode):
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()

        cmd.execute('''
        select * from stock_analysis where stock_code=?
        ''',(scode,))
        r=list(cmd.fetchone())
    conn.close()
    return r

def search_stock_live(scode):
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()

        cmd.execute('''
        select * from stock_live where stock_code=?
        ''',(scode,))
        r=list(cmd.fetchone())
    conn.close()
    return r

def search_company(scode):
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()

        cmd.execute('''
        select * from company where stock_code=?
        ''',(scode,))
        r=list(cmd.fetchone())
    conn.close()
    return r

def search_stock(scode):
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
                select * from stock_analysis where stock_code=?
                ''', (scode,))
        r=cmd.fetchall()
    conn.close()
    if len(r)==1:
        sa=search_stock_analysis(scode)
        sl=search_stock_live(scode)
        sc=search_company(scode)
        return [scode,[sa[1],sa[2],sa[3],sa[4],sa[6]],[sl[1],sl[2],sl[3]],[sc[1],sc[2],sc[3]]]
    else:
        return False

def search_stock_price(scode):
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select curr_p from stock_live where stock_code=?
        ''',(scode,))
        r=cmd.fetchall()
    conn.close()
    if len(r)==1:
        return r[0][0]
    else:
        return False

def search_stock_curr(scode):
    conn = sqlite3.connect("database.db")
    with conn:
        cmd = conn.cursor()
        cmd.execute('''
        select currency from stock_analysis where stock_code=?
        ''',(scode,))
        r=cmd.fetchall()
    conn.close()
    if len(r)==1:
        return r[0][0]
    else:
        return False