from helpers import *
from accounts import *
from transactions import *
import sys







def start_cli():
    clear_screen()
    print("""
          
     /$$    /$$                         /$$                          
  /$$$$$$ |__/                        | $$                          
 /$$__  $$ /$$ /$$$$$$/$$$$   /$$$$$$ | $$  /$$$$$$                 
| $$  \__/| $$| $$_  $$_  $$ /$$__  $$| $$ /$$__  $$                
|  $$$$$$ | $$| $$ \ $$ \ $$| $$  \ $$| $$| $$$$$$$$                
 \____  $$| $$| $$ | $$ | $$| $$  | $$| $$| $$_____/                
 /$$  \ $$| $$| $$ | $$ | $$| $$$$$$$/| $$|  $$$$$$$                
|  $$$$$$/|__/|__/ |__/ |__/| $$____/ |__/ \_______/                
 \_  $$_/                   | $$                                    
   \__/                     | $$                                    
                            |__/                                    
                      /$$                                           
                    /$$$$$$                                         
                   /$$__  $$  /$$$$$$  /$$    /$$ /$$$$$$   /$$$$$$ 
                  | $$  \__/ |____  $$|  $$  /$$//$$__  $$ /$$__  $$
                  |  $$$$$$   /$$$$$$$ \  $$/$$/| $$$$$$$$| $$  \__/
                   \____  $$ /$$__  $$  \  $$$/ | $$_____/| $$      
                   /$$  \ $$|  $$$$$$$   \  $/  |  $$$$$$$| $$      
                  |  $$$$$$/ \_______/    \_/    \_______/|__/      
                   \_  $$_/                                         
                     \__/                                                                                     
""")
    input("\nPress Enter to continue...")
    main_menu()


def main_menu():
    while True:
        clear_screen()
        print(r"""
        =======================================
        |       WELCOME TO $IMPLE $AVER       |
        =======================================
        | 1. Select Account                   |
        | 2. Create Account                   |
        | 3. Delete Account                   |
        | 4. Veiw All Transactions            |
        | 5. View Transactions By Account     |
        | 6. Search Transactions              |
        | 7. Exit                             |
        =======================================
        """)
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            select_account()
        elif choice == "2":
            create_account()
        elif choice == "3":
            delete_account()
        elif choice == "4":
            view_all_transactions()
        elif choice == "5":
            find_transactions_by_account()
        elif choice == "6":
            search_transactions()
        elif choice == "7":
            exit_program()
        else:
            input("Invalid Choice. Press Enter to try again.")


def select_account():
    clear_screen()
    print("\n--- SELECT AN ACCOUNT ---\n")

    CURSOR.execute("SELECT id, account_name, account_type, target_budget FROM Accounts")
    accounts = CURSOR.fetchall()

    if not accounts:
        print("No accounts found. Please create an account first.")
        input("\nPress Enter to return to the main menu.")
        return

    
    print("Available Accounts:")
    i = 0
    while i < len(accounts):
        account = accounts[i]  # Each `account` is a tuple: (id, name, type, budget)
        print(f"{i + 1}. {account[1]} ({account[2]}) - Target Budget: ${account[3]:.2f}")
        i += 1 

    while True:
        try:
            choice = int(input("Enter the number of the account you'd like to select: "))
            if 1 <= choice <= len(accounts):
                selected_account = accounts[choice - 1]  # Get chosen account tuple
                view_account_details(selected_account)  # Show account details
                return
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def view_account_details(account):
    clear_screen()
    print("\n--- ACCOUNT DETAILS ---\n")

    # Display account information
    print(f"Account Name: {account[1]}")
    print(f"Account Type: {account[2]}")
    print(f"Target Budget: ${account[3]:.2f}\n")

    # Fetch and display transaction history
    CURSOR.execute("SELECT amount, transaction_type FROM Transactions WHERE account_id = ?", (account[0],))
    transactions = CURSOR.fetchall()

    if transactions:
        print("--- Transaction History ---")
        for txn in transactions:
            print(f"{txn[1]}: ${txn[0]:.2f}")
    else:
        print("No transactions recorded for this account.")

    # Add option to record a transaction
    print("\n1. Add Transaction")
    print("2. Return to Main Menu")
    
    choice = input("Enter your choice: ")

    if choice == "1":
        add_transaction(account)
    elif choice == "2":
        main_menu()
    else:
        print("Invalid choice. Returning to Main Menu.")
        main_menu()


def create_account():
    clear_screen()
    print("--------[CREATE ACCOUNT]--------")
    
    name = input("Enter the name of the account: ")
    while not name:
        print("Error: Account name cannot be empty.")
        name = input("Enter the name of the account: ")
    clear_screen()

    print("--------[CREATE ACCOUNT]--------")
    print("Account Types: Wallet, Checking, Savings")
    acc_type = input("Enter the type of account: ")
    while acc_type not in ["Checking", "Savings", "Wallet"]:
        print("Error: Invalid account type.")
        acc_type = input("Enter the type of account: ")
    clear_screen()

    print("--------[CREATE ACCOUNT]--------")
    while True:
        try:
            target_budget = float(input("Enter target budget amount: $"))
            if target_budget <= 0:
                print("Error: Target budget must be greater than zero.")
            else:
                break
        except ValueError:
            print("Error: Please enter a valid number.")
    clear_screen()

    print("--------[CREATE ACCOUNT]--------")
    new_account = Account(name, acc_type, target_budget)
    new_account.save()
    print("Account created successfully!")
    input("\nPress Enter to return to the main menu.")
    

def delete_account():
    clear_screen()
    print("------- DELETE ACCOUNT -------")

    # Fetch all accounts
    sql = "SELECT id, account_name FROM Accounts"
    CURSOR.execute(sql)
    accounts = CURSOR.fetchall()

    if not accounts:
        print("No Accounts found.")
        input("Press Enter to return to the main menu.")
        return
    
    print("Select an account to delete: ")
    i = 0 
    while i < len(accounts):
        print(f"{i + 1}. {accounts[i][1]}")
        i += 1 

    while True:
        try: 
            choice = int(input("Enter the number of the account to delete: "))
            if 1 <= choice <= len(accounts):
                selected_account = accounts[choice - 1]
                account_id = selected_account[0]  # Assign account_id properly
                break
            else:
                print("Invalid choice. Please select a valid account number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    #Check if the account has transactions
    sql = "SELECT COUNT(*) FROM Transactions WHERE account_id = ?"
    CURSOR.execute(sql, (account_id,))
    transaction_count = CURSOR.fetchone()[0]

    if transaction_count > 0:
        print(f"Account '{selected_account[1]}' cannot be deleted because it has transactions.")
        input("Press Enter to return to the main menu.")
        return

    #Confirm deletion
    confirm = input(f"Are you sure you want to delete '{selected_account[1]}'? (yes/no): ").lower()
    if confirm != "yes":
        print("Account deletion canceled.")
        input("Press Enter to return to the main menu.")
        return

    #Delete account
    sql = "DELETE FROM Accounts WHERE id = ?"
    CURSOR.execute(sql, (account_id,))
    CONN.commit()

    print(f"Account '{selected_account[1]}' has been successfully deleted.")
    input("Press Enter to return to the main menu.")


def view_all_transactions():
    clear_screen()
    print("--- ALL TRANSACTIONS ---")

    sql = """
    SELECT * FROM Transactions 
    JOIN Accounts ON Transactions.account_id = Accounts.id
    ORDER BY Transactions.id DESC
    """

    CURSOR.execute(sql)
    transactions = CURSOR.fetchall()

    if not transactions: 
        print("No Transactions Found.")
    else: 
        for txn in transactions:
            print(f"{txn[1]} ({txn[6]}): ${txn[2]:.2f} ({txn[3]})")

    input("Press Enter to return to the main menu.")


def exit_program():
    clear_screen()
    print("Goodbye! Thanks for using Simple Saver.")
    sys.exit()


def find_transactions_by_account():
    clear_screen()
    print("--- FIND TRANSACTIONS BY ACCOUNT ---")

    # Fetch all accounts
    sql = ("SELECT id, account_name FROM Accounts")
    CURSOR.execute(sql)
    accounts = CURSOR.fetchall()

    if not accounts:
        print("No accounts found. Please create an account first.")
        input("Press Enter to return to the main menu.")
        return

    # Display account choices using a while loop
    print("Select an account:")
    i = 0  # Initialize counter
    while i < len(accounts):
        print(f"{i + 1}. {accounts[i][1]}")
        i += 1  # Increment counter

    # User selects an account
    while True:
        try:
            choice = int(input("Enter the number of the account to view transactions: "))
            if 1 <= choice <= len(accounts):
                selected_account = accounts[choice - 1]
                account_id = selected_account[0]
                break
            else:
                print("Invalid choice. Please select a valid account number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Fetch transactions for the selected account
    sql = """
        SELECT amount, transaction_type 
        FROM Transactions 
        WHERE account_id = ?
        ORDER BY id DESC
    """
    CURSOR.execute(sql, (account_id,))
    transactions = CURSOR.fetchall()

    clear_screen()
    print(f"--- TRANSACTIONS FOR {selected_account[1]} ---")

    if transactions:
        print(f"{'Amount':<10} {'Type':<10}")
        print("-" * 30)
        i = 0  # Reset counter for transactions
        while i < len(transactions):
            print(f"${transactions[i][0]:<10.2f} {transactions[i][1]:<10}")
            i += 1  # Increment counter
    else:
        print("No transactions recorded for this account.")

    input("Press Enter to return to the main menu.")


def add_transaction(account):
    clear_screen()
    print(f"\n--- ADD TRANSACTION FOR {account[1]} ({account[2]}) ---\n")

    # Ask transaction type
    print("Transaction Types: Income | Expense")
    trans_type = input("Enter transaction type: ").strip().capitalize()
    while trans_type not in ["Income", "Expense"]:
        print("Error: Invalid transaction type. Choose 'Income' or 'Expense'.")
        trans_type = input("Enter transaction type: ").strip().capitalize()

    # Get transaction amount (must be positive)
    while True:
        try:
            amount = float(input("Enter transaction amount: $"))
            if amount <= 0:
                print("Error: Transaction amount must be greater than zero.")
            else:
                break
        except ValueError:
            print("Error: Please enter a valid number.")

    # Create and save transaction using `Transaction` class
    new_transaction = Transaction(account[0], amount, trans_type)
    new_transaction.save()  # Saves to database

    # Confirmation message
    print(f"\n✅ {trans_type} of ${amount:.2f} successfully added to {account[1]}.")

    input("\nPress Enter to return to account details.")
    view_account_details(account)  # Return to account details after adding a transaction


def search_transactions():
    clear_screen()
    print("\n--- SEARCH TRANSACTIONS ---\n")

    # User selects search type
    print("Search by:")
    print("1. Transaction Type (Income/Expense)")
    print("2. Transaction Amount (Greater Than)")
    print("3. Transaction Amount (Less Than)")
    print("4. Return to Main Menu")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        search_value = input("\nEnter transaction type (Income/Expense): ").strip().capitalize()
        sql = "SELECT amount, transaction_type, account_id FROM Transactions WHERE transaction_type = ?"
        CURSOR.execute(sql, (search_value,))
    elif choice == "2":
        try:
            amount = float(input("\nEnter the minimum amount to search for: $"))
            sql = "SELECT amount, transaction_type, account_id FROM Transactions WHERE amount >= ?"
            CURSOR.execute(sql, (amount,))
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")
            return
    elif choice == "3":
        try:
            amount = float(input("\nEnter the maximum amount to search for: $"))
            sql = "SELECT amount, transaction_type, account_id FROM Transactions WHERE amount <= ?"
            CURSOR.execute(sql, (amount,))
        except ValueError:
            print("\nInvalid input. Please enter a valid number.")
            return
    elif choice == "4":
        return
    else:
        print("Invalid choice. Returning to main menu.")
        return

    transactions = CURSOR.fetchall()

    if transactions:
        print("\nMatching Transactions:\n")
        for txn in transactions:
            print(f"🔹 {txn[1]}: ${txn[0]:.2f} (Account ID: {txn[2]})")
    else:
        print("\nNo matching transactions found.")

    input("\nPress Enter to return to the main menu.")


