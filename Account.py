import sys
from AccountError import NegativeError

class Account:
    counter = 0     # declaring class variable

    # variable_name convention      meaning
    # abc           public          accessible by everyone
    # _abc          non-pub         for internal use
    # __abc         name-mangled    avoid accidental name conflict
    def __init__(self, owner, balance=0):
        Account.counter += 1    # reference a class variable by using the class name
        self.__id = Account.counter
        self.__owner = owner
        self.__balance = balance

    # declare @property to enable getter calls without explicit calling to the function
    @property
    def id(self):
        return self.__id

    @property
    def owner(self):
        return self.__owner

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        try:
            amount = int(amount)
        except (ValueError, TypeError):
            # print sends output to standard output stream
            # use sys.stderr.write to send message to error stream
            # this example handles the error within this function in the class.
            sys.stderr.write("Amount must be in numbers")
        else:
            if amount > 0:
                self.__balance += amount
            else:
                # this example forces calling program to handle the error
                raise ValueError("Amount must be greater than 0")

    def withdraw(self, amount):
        try:
            amount = int(amount)
        except (ValueError, TypeError):
            sys.stderr.write("Amount must be in numbers")
        else:
            if self.balance < amount:
                raise NotImplementedError("Overdraft is not implemented")
            elif amount > 0:
                self.__balance -= amount
            else:
                # using custom exception
                raise NegativeError("Amount must be greater than 0")


    def __str__(self):
        return f"Account: {self.id:<5}\tOwner: {self.owner:<10}\tBalance: THB {self.balance:>8}"

    def __eq__(self, other):
        if not isinstance(other, Account):
            return NotImplemented

        return self.id == other.id and self.owner == other.owner

def main():
   user1 = Account("Albert", 100)
   print(user1)

if __name__ == "__main__":
    main()
