import mysql.connector

# Establish MySQL connection

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="LuckyAmma@123",
    database="bank_management"
)

# Create a cursor object to interact with the database

cursor = db_connection.cursor() # The cursor() method is used to create a cursor object associated with the MySQL connection.

# Create the 'bank_management' database if it doesn't exist

cursor.execute("CREATE DATABASE IF NOT EXISTS bank_management")
cursor.execute("USE bank_management")

# Create the 'account_table' table if it doesn't exist

cursor.execute('''
    CREATE TABLE IF NOT EXISTS account_table (
        account_number BIGINT PRIMARY KEY,
        name VARCHAR(255),
        dob VARCHAR(20),
        mob_no VARCHAR(15),
        address VARCHAR(255),
        balance FLOAT
    )
''')

import random

def generate_account_number():
    return random.randint(100000000000,999999999999)

def open_account(accounts):                     # Function definition
    name = input("Enter your name: ")
    dob = input("Enter Your Date Of Birth: ")
    mob_no = input("Enter Your mobile number: ")
    add = input("Enter Your address: ")
    account_number =generate_account_number()   # Generate a new account number using the function generate_account_number()
    accounts[account_number] = 0                # Add the new account number to the 'accounts' dictionary with an initial balance of 0
    # Insert account details into the database
    cursor.execute('''
            INSERT INTO account_table (account_number, name, dob, mob_no, address, balance)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (account_number, name, dob, mob_no, add, 0))

    db_connection.commit()  # save the data permanently in the table
    print(f"Account successfully opened. Your Account Number: {account_number}")

def deposit_amount(accounts):
    account_number = int(input("Enter your Account Number: "))
    if account_number in accounts:     # Check if the entered account number exists in the 'accounts' dictionary
        amount = float(input("Enter the amount to deposit: "))
        accounts[account_number] += amount   # Update the account balance by adding the deposited amount
        # Update account balance in the database
        cursor.execute('''
                    UPDATE account_table
                    SET balance = %s
                    WHERE account_number = %s
                ''', (accounts[account_number], account_number))

        db_connection.commit()
        print("Deposit successful. Your new balance is:", accounts[account_number])
    else:
        print("Invalid Account Number. Please try again.")



def withdraw_amount(accounts):
    account_number = int(input("Enter your Account Number: "))
    if account_number in accounts:
        amount = float(input("Enter the amount to withdraw: "))
        if amount <= accounts[account_number]:                  # Check if there are sufficient funds in the account to cover the withdrawal
            accounts[account_number] -= amount         # If there are sufficient funds, subtract the withdrawal amount from the account balance
            # Update account balance in the database
            cursor.execute('''
                            UPDATE account_table
                            SET balance = %s
                            WHERE account_number = %s
                        ''', (accounts[account_number], account_number))

            db_connection.commit()
            print("Withdrawal successful. Your new balance is:", accounts[account_number])
        else:
            print("Insufficient funds. Cannot withdraw.")
    else:
        print("Invalid Account Number. Please try again.")



def balance_enquiry(accounts):
    account_number = int(input("Enter your Account Number: "))
    if account_number in accounts:
        # Retrieve the balance from the database
        cursor.execute('''
            SELECT balance
            FROM account_table
            WHERE account_number = %s
        ''', (account_number,))

        result = cursor.fetchone()

        if result:
            balance = result[0]
            print("Your balance is:", balance)
        else:
            print("Error retrieving balance from the database.")
    else:
        print("Invalid Account Number. Please try again.")


def close_account(accounts):
    account_number = int(input("Enter your Account Number: "))
    if account_number in accounts:
        del accounts[account_number]
        # Delete the account from the database
        cursor.execute('''
                    DELETE FROM account_table
                    WHERE account_number = %s
                ''', (account_number,))

        db_connection.commit()
        print("Your account is successfully closed.")
    else:
        print("Invalid Account Number. Please try again.")


def main():
    accounts = {}  # Creating an empty dictionary to store values

    while True:
        print('''
              1. Open New Account
              2. Deposit Amount
              3. Withdraw Amount
              4. Balance Enquiry
              5. Close An Account
              6. Quit
        ''')

        choice = input("Enter the task you want to perform: ")

        if choice == '1':
            open_account(accounts)
        elif choice == '2':
            deposit_amount(accounts)
        elif choice == '3':
            withdraw_amount(accounts)
        elif choice == '4':
            balance_enquiry(accounts)
        elif choice == '5':
            close_account(accounts)
        elif choice == '6':
            print("Quitting the bank management system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


main()
