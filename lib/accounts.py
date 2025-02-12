from __init__ import CONN, CURSOR

class Account:
    
    def __init__(self, account_name, account_type, target_budget):
        self._account_name = None
        self._account_type = None
        self._target_budget = None

        self.account_name = account_name  # Uses setter
        self.account_type = account_type  # Uses setter
        self.target_budget = target_budget  # Uses setter

    # Class Attributes & Properties
    @property
    def account_name(self):
        return self._account_name
    
    @account_name.setter
    def account_name(self, name):
        if isinstance(name, str) and len(name) > 0:
            self._account_name = name
        else:
            raise ValueError("Error: Account name must be a non-empty string.")

    @property
    def account_type(self):
        return self._account_type
    
    @account_type.setter
    def account_type(self, acc_type):
        valid_types = ["Checking", "Savings", "Wallet"]
        if acc_type not in valid_types:
            raise ValueError("Error: Valid account types are 'Wallet', 'Checking', and 'Savings'.")
        self._account_type = acc_type 

    @property
    def target_budget(self):
        return self._target_budget
    
    @target_budget.setter
    def target_budget(self, budget):
        if not isinstance(budget, (int, float)) or budget <= 0:
            raise ValueError("Error: Target budget must be a positive number.")
        self._target_budget = float(budget)

    ### Instance Methods
    def save(self):
        sql = '''
            INSERT INTO Accounts (account_name, account_type, target_budget)
            VALUES (?, ?, ?)
        '''
        CURSOR.execute(sql, (self.account_name, self.account_type, self.target_budget))
        CONN.commit()
        print(f"Account '{self.account_name}' saved successfully.")

    def delete(self):
        sql = '''
            DELETE FROM Accounts WHERE account_name = ? AND account_type = ? AND target_budget = ?
        '''    
        CURSOR.execute(sql, (self.account_name, self.account_type, self.target_budget))
        CONN.commit()
        print(f"Account '{self.account_name}' deleted successfully.")

