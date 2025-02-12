# lib/__init__.py
import sqlite3

CONN = sqlite3.connect('simple_saver.db')
CURSOR = CONN.cursor()

def accounts_table():
    sql = '''
    CREATE TABLE IF NOT EXISTS Accounts (
    id INTEGER PRIMARY KEY,
    account_name TEXT,
    account_type TEXT,
    target_budget REAL
    )
    '''
    CURSOR.execute(sql)
    CONN.commit()

def transactions_table():
    sql = '''
    CREATE TABLE IF NOT EXISTS Transactions (
    id INTEGER PRIMARY KEY,
    account_id INTEGER,
    amount REAL,
    transaction_type TEXT,
    FOREIGN KEY (account_id) REFERENCES Accounts(id) 
    )
    '''
    CURSOR.execute(sql)
    CONN.commit()
    
