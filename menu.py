import os
from Account import Account
from AccountError import NegativeError

# --- Helper Functions ---


def find_account_by_owner(accounts, owner_name):
    """Finds the first account matching the owner's name (case-insensitive)."""
    for acc in accounts:
        if acc.owner.lower() == owner_name.lower():
            return acc
    return None


# --- Menu Action Functions ---


def create_account(accounts):
    owner = input("Enter owner name: ").strip()
    if not owner:
        print("Owner name cannot be empty.")
        return

    try:
        balance = int(input("Enter initial balance (THB): "))
        if balance < 0:
            print("Initial balance cannot be negative.")
            return
    except ValueError:
        print("Invalid balance amount. Please enter a whole number.")
        return

    # Account.__init__ automatically assigns the ID via Account.counter
    new_acc = Account(owner, balance)
    accounts.append(new_acc)
    print(f"Account created successfully!\n{new_acc}")


def delete_account(accounts):
    try:
        acc_id = int(input("Enter account ID to delete: "))
    except ValueError:
        print("Invalid ID format. Please enter a number.")
        return

    owner = input("Enter owner name to confirm: ").strip()

    for acc in accounts:
        if acc.id == acc_id and acc.owner.lower() == owner.lower():
            accounts.remove(acc)
            print(f"Deleted account -> {acc}")
            return

    print("No matching account found with that ID and owner name.")


def handle_deposit(accounts):
    owner = input("Enter owner name to deposit to: ").strip()
    acc = find_account_by_owner(accounts, owner)

    if not acc:
        print(f"Account for '{owner}' not found.")
        return

    try:
        amount = int(input("Enter amount to deposit (THB): "))
        acc.deposit(amount)
        print(f"Deposited THB {amount}. New balance: THB {acc.balance}")
    except ValueError as e:
        # Catches both non-numeric input() and ValueError raised by acc.deposit()
        print(f"Deposit failed: {e}")


def handle_withdraw(accounts):
    owner = input("Enter owner name to withdraw from: ").strip()
    acc = find_account_by_owner(accounts, owner)

    if not acc:
        print(f"Account for '{owner}' not found.")
        return

    try:
        amount = int(input("Enter amount to withdraw (THB): "))
        acc.withdraw(amount)
        print(f"Withdrew THB {amount}. New balance: THB {acc.balance}")
    except ValueError:
        print("Invalid amount. Please enter a whole number.")
    except (NotImplementedError, NegativeError) as e:
        # Catches overdrafts and negative numbers raised by acc.withdraw()
        print(f"Withdrawal failed: {e}")


def load_from_db(accounts, filename="accounts_db.txt"):
    if not os.path.exists(filename):
        print(f"Database file '{filename}' not found.")
        return

    accounts.clear()
    max_id = 0
    loaded_count = 0

    with open(filename, "r") as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            if not line:
                continue

            parts = line.split(":")
            if len(parts) == 3:
                acc_id_str, owner, balance_str = parts
                try:
                    acc_id = int(acc_id_str)
                    balance = int(float(balance_str))

                    # Create account and restore its original saved ID
                    acc = Account(owner, balance)
                    acc._Account__id = acc_id

                    accounts.append(acc)
                    if acc_id > max_id:
                        max_id = acc_id
                    loaded_count += 1
                except ValueError:
                    print(f"Skipping corrupted data on line {line_num}: {line}")
            else:
                print(f"Skipping malformed line {line_num}: {line}")

    # Sync class counter so new accounts continue from the highest loaded ID
    Account.counter = max_id
    print(f"Successfully loaded {loaded_count} account(s) from '{filename}'.")


def save_to_db(accounts, filename="accounts_db.txt"):
    try:
        with open(filename, "w") as file:
            for acc in accounts:
                file.write(f"{acc.id}:{acc.owner}:{acc.balance}\n")
        print(
            f"Successfully saved {len(accounts)} account(s) to '{filename}'."
        )
    except IOError as e:
        print(f"Error saving to file: {e}")


# --- Main Application Loop ---


def main():
    accounts = []
    db_file = "accounts_db.txt"

    while True:
        print("\n--- Bank Account Management ---")
        print("1. Create new account")
        print("2. Delete account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Display Accounts")
        print("6. Load from DB")
        print("7. Save to DB")
        print("8. Exit")

        choice = input("Select an option (1-7): ").strip()

        if choice == "1":
            create_account(accounts)
        elif choice == "2":
            delete_account(accounts)
        elif choice == "3":
            handle_deposit(accounts)
        elif choice == "4":
            handle_withdraw(accounts)
        elif choice == "5":
            for account in accounts:
                print(account)
        elif choice == "6":
            load_from_db(accounts, db_file)
        elif choice == "7":
            save_to_db(accounts, db_file)
        elif choice == "8":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose a number between 1 and 7.")


if __name__ == "__main__":
    main()
