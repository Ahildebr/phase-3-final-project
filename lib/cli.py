from helpers import *
from accounts import Account
from transactions import Transaction
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
    input("Press Enter to continue...")
    main_menu()

def main_menu():
    while True:
        clear_screen()
        print("""
        =======================================
        |       WELCOME TO $IMPLE $AVER       |
        =======================================
        | 1. Select Account                   |
        | 2. Create Account                   |
        | 3. Delete Account                   |
        | 4. Manage Transactions              |
        | 5. Find Account by ID               |
        | 6. Find Transaction by ID           |
        | 7. Exit                             |
        =======================================
        """)
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            select_account()
        elif choice == "2":
            create_account()
        elif choice == "3":
            delete_account()
        elif choice == "4":
            manage_transactions()
        elif choice == "5":
            find_account_by_id()  #  Calls new function
        elif choice == "6":
            find_transaction_by_id()  #  Calls new function
        elif choice == "7":
            exit_program()
        else:
            input("Invalid Choice. Press Enter to try again.")

def select_account():
    clear_screen()
    print("--- SELECT AN ACCOUNT ---")

    accounts = Account.get_all()
    if not accounts:
        print("No accounts found. Please create an account first.")
        input("Press Enter to return to the main menu.")
        return

    print("ID | Account Name | Type")
    print("-" * 30)
    for i, account in enumerate(accounts, start=1):
        print(f"{account.id} | {account.account_name} | {account.account_type}")

    while True:
        try:
            choice = int(input("Enter the Account ID you'd like to select (or 0 to return): "))
            
            if choice == 0:
                return  #  Go back to the main menu
            
            selected_account = next((acc for acc in accounts if acc.id == choice), None)

            if selected_account:
                view_account_details(selected_account)
                return
            else:
                print("Invalid Account ID. Please enter a valid ID.")

        except ValueError:
            print("Invalid input. Please enter a number.")

def view_account_details(account):
    clear_screen()
    print("--- ACCOUNT DETAILS ---")
    print(f"Account Name: {account.account_name}")
    print(f"Account Type: {account.account_type}")
    print(f"Target Budget: ${account.target_budget:.2f}")

    transactions = Transaction.get_by_account(account.id)

    if transactions:
        print("--- Transaction History ---")
        for txn in transactions:
            print(f"{txn.transaction_type}: ${txn.amount:.2f}")
    else:
        print("No transactions recorded.")

    print("1. Add Transaction")
    print("2. Return to Main Menu")

    choice = input("Enter your choice: ").strip()
    if choice == "1":
        try:
            amount = float(input("Enter transaction amount: $"))
            trans_type = input("Enter transaction type (Income/Expense): ").strip().capitalize()
            Transaction.add(account.id, amount, trans_type)  #  Call `Transaction.add()` instead of separate function
            print(f" {trans_type} of ${amount:.2f} added to {account.account_name}.")
        except ValueError as e:
            print(f"{e}")
        input("Press Enter to return to account details.")
        view_account_details(account)  #  Refresh account details
    elif choice == "2":
        main_menu()

def create_account():
    clear_screen()
    print("--------[CREATE ACCOUNT]--------")

    while True:
        name = input("Enter the name of the account: ").strip()
        if not name:
            print("Account name cannot be empty. Please enter a valid name.")
            continue

        acc_type = input("Enter the type of account (Checking/Savings/Wallet): ").strip().capitalize()
        if acc_type not in ["Checking", "Savings", "Wallet"]:
            print("Invalid account type. Please enter 'Checking', 'Savings', or 'Wallet'.")
            continue

        target_budget = input("Enter target budget amount: $").strip()
        try:
            target_budget = float(target_budget)
            if target_budget <= 0:
                print("Target budget must be a positive number.")
                continue
        except ValueError:
            print("Invalid budget amount. Please enter a valid number.")
            continue
        
        # If all inputs are valid, create the account
        new_account = Account.create(name, acc_type, target_budget)

        if new_account:
            print(f"Account '{new_account.account_name}' created successfully!")
        input("Press Enter to return to the main menu.")
        break


def delete_account():
    clear_screen()
    print("------- DELETE ACCOUNT -------")

    accounts = Account.get_all()
    if not accounts:
        print("No Accounts found.")
        return

    for i, account in enumerate(accounts, start=1):
        print(f"{i}. {account.account_name}")

    try:
        choice = int(input("Select an account to delete: ")) - 1
        selected_account = accounts[choice]
        if selected_account.delete():
            input("Press Enter to return to the main menu.")
    except (ValueError, IndexError):
        print("Invalid input.")

def delete_transaction():
    """Allows users to delete a transaction by ID."""
    clear_screen()
    print("--- DELETE TRANSACTION ---")

    try:
        transaction_id = int(input("Enter the Transaction ID to delete: "))
        transaction = Transaction.find_by_id(transaction_id)

        if transaction:
            confirm = input(f"Are you sure you want to delete this transaction? (yes/no): ").strip().lower()
            if confirm == "yes":
                transaction.delete()
                print(" Transaction deleted successfully.")
            else:
                print("Transaction deletion canceled.")
        else:
            print("No transaction found with that ID.")

    except ValueError:
        print("Invalid input. Please enter a valid ID.")

    input("Press Enter to return to transaction management.")

def view_all_transactions():
    clear_screen()
    print("--- ALL TRANSACTIONS ---")

    transactions = Transaction.get_all()

    if not transactions:
        print("No Transactions Found.")
    else:
        print("ID | Transaction Type | Amount | Account ID")
        print("-" * 40)
        for txn in transactions:
            print(f"{txn.id} | {txn.transaction_type} | ${txn.amount:.2f} | {txn.account_id}")

    input("Press Enter to return to the main menu.")

def find_account_by_id():
    """Allows user to find an account using its ID."""
    clear_screen()
    print("--- FIND ACCOUNT BY ID ---")

    try:
        account_id = int(input("Enter the Account ID: "))
        account = Account.find_by_id(account_id)

        if account:
            print(" Account Found:")
            print(f"🔹 Account Name: {account.account_name}")
            print(f"🔹 Account Type: {account.account_type}")
            print(f"🔹 Target Budget: ${account.target_budget:.2f}")
        else:
            print("No account found with that ID.")

    except ValueError:
        print("Invalid input. Please enter a valid ID.")

    input("Press Enter to return to the main menu.")

def find_transaction_by_id():
    """Allows user to find a transaction using its ID."""
    clear_screen()
    print("--- FIND TRANSACTION BY ID ---")

    try:
        transaction_id = int(input("Enter the Transaction ID: "))
        transaction = Transaction.find_by_id(transaction_id)

        if transaction:
            print(" Transaction Found:")
            print(f"🔹 Amount: ${transaction.amount:.2f}")
            print(f"🔹 Type: {transaction.transaction_type}")
            print(f"🔹 Account ID: {transaction.account_id}")
        else:
            print("No transaction found with that ID.")

    except ValueError:
        print("Invalid input. Please enter a valid ID.")

    input("Press Enter to return to the main menu.")

def manage_transactions():
    while True:
        clear_screen()
        print("""
        =======================================
        |         MANAGE TRANSACTIONS         |
        =======================================
        | 1. View All Transactions            |
        | 2. Find Transaction By ID           |
        | 3. Delete a Transaction             |
        | 4. Return to Main Menu              |
        =======================================
        """)
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            view_all_transactions()
        elif choice == "2":
            find_transaction_by_id()  #  Find transactions by ID
        elif choice == "3":
            delete_transaction()  #  Delete a transaction by ID
        elif choice == "4":
            return  #  Goes back to the main menu
        else:
            input("Invalid Choice. Press Enter to try again.")

def exit_program():
    clear_screen()
    print("Goodbye! Thanks for using Simple Saver.")
    sys.exit()

def find_transactions_by_account():
    """Handles user interaction for viewing transactions by account."""
    accounts = Account.get_all()
    if not accounts:
        print("⚠ No accounts found. Please create an account first.")
        input("Press Enter to return to the main menu.")
        return

    print("--- VIEW TRANSACTIONS BY ACCOUNT ---")
    for i, account in enumerate(accounts, start=1):
        print(f"{i}. {account.account_name}")

    print("0. Return to Main Menu")  # Option to go back

    try:
        choice = int(input("Enter the number of the account to view transactions (or 0 to return): ")) - 1

        if choice == -1:  # User selected 0 (Return to Main Menu)
            return
        
        if 0 <= choice < len(accounts):  # Ensure input is within range
            selected_account = accounts[choice]
            transactions = Transaction.get_by_account(selected_account.id)

            clear_screen()
            print(f"--- TRANSACTIONS FOR {selected_account.account_name} ---")

            if transactions:
                for txn in transactions:
                    print(f"{txn.transaction_type}: ${txn.amount:.2f}")
            else:
                print("No transactions recorded for this account.")

        else:
            print("Invalid choice. Please enter a valid number.")
            input("Press Enter to try again.")
            find_transactions_by_account()  # Retry

    except ValueError:
        print("Invalid input. Please enter a number.")
        input("Press Enter to try again.")
        find_transactions_by_account()  # Retry

