from __init__ import CONN, CURSOR

class Transaction:
    def __init__(self, id, account_id, amount, transaction_type):
        self.id = id
        self._account_id = None
        self._amount = None
        self._transaction_type = None

        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type

### Attributes and Properties
    @property
    def account_id(self):
        return self._account_id
    
    @property
    def amount(self):
        return self._amount
    
    @property
    def transaction_type(self):
        return self._transaction_type
    
    @account_id.setter
    def account_id(self, acc_id):
        if not isinstance(acc_id, int) or acc_id <= 0:
            raise ValueError("Error: Account ID must be a positive integer.")
        self._account_id = acc_id 

    @amount.setter
    def amount(self, amt):
        if not isinstance(amt, (int, float)) or amt == 0:
            raise ValueError("Error: Amount must be a non-zero number.")
        self._amount = amt

    @transaction_type.setter
    def transaction_type(self, trans_type):
        valid_types = ["Income", "Expense"]
        if trans_type not in valid_types:
            raise ValueError("Error: Invalid Transaction type, Approved Transaction types are \"Income\" or \"Expense\".")
        self._transaction_type = trans_type    

    #Instance Methods
    def save(self):
        sql = '''
            INSERT INTO Transactions (account_id, amount, transaction_type)
            VALUES (?, ?, ?)
        '''
        CURSOR.execute(sql, (self.account_id, self.amount, self.transaction_type))
        CONN.commit()
        self.id = CURSOR.lastrowid
        print(f"Transaction of ${self.amount:.2f} ({self.transaction_type}) saved successfully.")

    def delete(self):
        sql = '''
            DELETE FROM Transactions WHERE id = ?
        '''    
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        print(f"Transaction of ${self.amount:.2f} ({self.transaction_type}) deleted successfully.")

### Class Methods
    @classmethod
    def get_by_account(cls, account_id):
        sql = "SELECT id, amount, transaction_type FROM Transactions WHERE account_id = ?"
        CURSOR.execute(sql, (account_id,))
        transactions = CURSOR.fetchall()
        return [cls(txn[0], account_id, txn[1], txn[2]) for txn in transactions]

    @classmethod
    def add(cls, account_id, amount, transaction_type):
        sql = "INSERT INTO Transactions (account_id, amount, transaction_type) VALUES (?, ?, ?)"
        CURSOR.execute(sql, (account_id, amount, transaction_type))
        CONN.commit()
        transaction_id = CURSOR.lastrowid

        return cls(transaction_id, account_id, amount, transaction_type)

    @classmethod
    def get_all(cls):
        sql = "SELECT id, account_id, amount, transaction_type FROM Transactions"
        CURSOR.execute(sql)
        transactions = CURSOR.fetchall()
        return [cls(txn[0], txn[1], txn[2], txn[3]) for txn in transactions]

    @classmethod
    def find_by_id(cls, transaction_id):
        sql = "SELECT id, account_id, amount, transaction_type FROM Transactions WHERE id = ?"
        CURSOR.execute(sql, (transaction_id,))
        txn = CURSOR.fetchone()
        return cls(*txn) if txn else None
