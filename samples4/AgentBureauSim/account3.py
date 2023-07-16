micropayment = 1e-4

class Account:
    def __init__(self, idx, name, balance):
        self.__idx = idx
        self.__name = name
        self.__balance = balance
        return
    def get_id(self):
        return self.__idx
    def name(self):
        return self.__name
    def balance(self):
        return self.__balance
    def withdrawal(self, desc, amount):
        amount = abs(amount)
        val = self.__balance - amount
        if val >= 0:
            self.__balance = val
            result = amount
##            print(f"withdrawal: desc = '{desc}'\n"+\
##                  f"  amount = ${result:.2f}\n"+\
##                  f"  post_account = {self}")               
        else:
            result = 0
        return result
    def deposit(self, desc, amount):
        amount = abs(amount)
        # if amount is greater than micropayment limit
        if amount < micropayment:
            # amount is loss, micropayment is very small
            return
        val = self.__balance + amount
        self.__balance = val
        result = amount
##        print(f"deposit: desc = '{desc}'\n"+\
##              f"  amount = ${result:.2f}\n"+\
##              f"  post_account = {self}")
        return
    def __str__(self):
        name = self.__name
        balance = self.__balance
        s = f"Account(name='{name}',"+\
            f"balance=${balance:.2f})"
        return s
    def __repr__(self):
        return str(self)
