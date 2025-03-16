import json

class Account:
    def __init__(self, account_number, name, initial_deposit):
        self.account_number = account_number
        self.name = name
        self.balance = initial_deposit

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return "Insufficient funds...!"
        else:
            self.balance -= amount
            return self.balance

    def get_balance(self):
        return self.balance

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'name': self.name,
            'balance': self.balance
        }

    @staticmethod
    def from_dict(data):
        return Account(data['account_number'], data['name'], data['balance'])


class BankSystem:
    def __init__(self, filename='accounts.json'):
        self.accounts = {}
        self.filename = filename
        self.load_accounts()

    def load_accounts(self):
        try:
            with open(self.filename, 'r') as file:
                accounts_data = json.load(file)
                for account_data in accounts_data:
                    account = Account.from_dict(account_data)
                    self.accounts[account.account_number] = account
        except FileNotFoundError:
            pass

    def save_accounts(self):
        with open(self.filename, 'w') as file:
            accounts_data = [account.to_dict() for account in self.accounts.values()]
            json.dump(accounts_data, file, indent=4)

    def create_account(self, account_number, name, initial_deposit):
        if account_number in self.accounts:
            return "Account already exists...!"
        else:
            self.accounts[account_number] = Account(account_number, name, initial_deposit)
            self.save_accounts()
            return "Account created successfully  :-)"

    def login(self, account_number):
        if account_number in self.accounts:
            return self.accounts[account_number]
        else:
            return "Account does not exist :-("


def main():
    bank = BankSystem()
    while True:
        print("\nWelcome to the Bank System :-)")
        print("1. Create Account")
        print("2. Log In")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            account_number = input("Enter account number: ")
            name = input("Enter account holder's name: ")
            initial_deposit = float(input("Enter initial deposit: "))
            print(bank.create_account(account_number, name, initial_deposit))

        elif choice == '2':
            account_number = input("Enter account number: ")
            account = bank.login(account_number)
            if isinstance(account, Account):
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Balance Enquiry")
                    print("4. Log Out")
                    user_choice = input("Enter your choice: ")

                    if user_choice == '1':
                        amount = float(input("Enter amount to deposit: "))
                        print(f"New balance: {account.deposit(amount)}")
                        bank.save_accounts()

                    elif user_choice == '2':
                        amount = float(input("Enter amount to withdraw: "))
                        print(account.withdraw(amount))
                        bank.save_accounts()

                    elif user_choice == '3':
                        print(f"Current balance: {account.get_balance()}")

                    elif user_choice == '4':
                        break

                    else:
                        print("Invalid choice, Please try again...!")

            else:
                print(account)

        elif choice == '3':
            print("Thank you for using the Bank System...! :-)")
            break

        else:
            print("Invalid choice,Please try again...!")

if __name__ =="__main__":
    main()
