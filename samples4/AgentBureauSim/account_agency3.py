import account3 as acc_m

class Account_Agency:
    def __init__(self, SA, pwd, account_id, domain):
        self.__accounts = {}
        self.__idx = len(list(self.__accounts.keys()))
        self.__pwds = {}
        self.__names = {}
        self.__encode = SA.get_encode()
        self.__L = []
        self.__pwd = pwd
        self.__account_id = account_id
        self.__balance = 0
        self.__attempts = {}
        self.__locks = {}
        self.__max_attempts = 10
        self.__admin_password = "clear_locks"
        self.__domain = domain
    def get_domain(self):
        return self.__domain
    def clear_lock(self, encoded_pwd, account_id):
        L = list(self.__accounts.keys())
        flag0 = account_id in L
        if not flag0:
            print(f"{account_id} does not exist")
            return False
        pwd = self.__admin_password
        enc_pwd1 = self.__encode(pwd)
        enc_pwd2 = encoded_pwd
        flag = enc_pwd1 == enc_pwd2
        if flag:
            self.__attempts[account_id] = 0
            self.__locks[account_id] = 0        
        return
    def get_id(self):
        return self.__account_id
    def balance(self):
        return self.__balance
    def get_user_balance(self,id_from):
        account = self.__accounts[id_from]
        val = account.balance()
        return val
    def get_number_accounts(self):
        return len(list(self.__accounts.keys()))
    def get_id(self):
        return self.__account_id
    def authenticate_AA(self, encoded_pwd):
        enc_pwd1 = self.__encode(self.__pwd)
        enc_pwd2 = encoded_pwd
        flag = enc_pwd1 == enc_pwd2
        return flag
    def __get_attempts(self, account_id):
        try:
            val = self.__attempts[account_id]
        except:
            print(f"Error: no attempts for {account_id}")
            val = 0
        return val
    def __validate(self,
                encoded_pwd, account_id):
        L = list(self.__accounts.keys())
        flag0 = account_id in L
        if not flag0:
            print(f"{account_id} does not exist")
            return False
        pwd = self.__pwds[account_id]
        enc_pwd1 = self.__encode(pwd)
        enc_pwd2 = encoded_pwd
        flag_valid = False
        if self.__locks[account_id] > 0:
            print(f"Error: Account {account_id} is"+\
                  f" locked")
            flag_valid = False
        else:
            flag1 = enc_pwd1 == enc_pwd2
            val1 = self.__get_attempts(account_id)
            if not flag1:
                print(f"password not valid {account_id}")
                val2 = val1 + 1
                self.__attempts[account_id]= val2
                flag_valid = False
            flag2 = val1 <= self.__max_attempts
            if not flag2:
                print(f"Error: Account {account_id}"+\
                      f" max attempts exceeded")
                self.__locks[account_id] = \
                    self.__locks[account_id] + 1
                flag_valid = False
            if flag1:
                #print(f"password valid")
                self.__attempts[account_id] = 0
                self.__locks[account_id] = 0
                flag_valid = True
        #if not flag_valid:
        #    return 1/0
        return flag_valid
    def authenticate_user(self, encoded_pwd,
                account_id):
        flag = self.__validate(encoded_pwd,
                        account_id)
        return flag
    def get_transactions(self, encoded_pwd):
        if self.authenticate_AA(encoded_pwd): 
            return self.__L
        return []
    def clear_transactions(self, encoded_pwd):
        if self.authenticate_AA(encoded_pwd): 
            self.__L = []
        return     
    def account_to_cash(self,
                          id_from, desc,
                          amount): 
        account_id = id_from
        pwd = self.__pwds[account_id]
        enc_pwd = self.__encode(pwd)
        if self.authenticate_user(enc_pwd,
                        account_id):
            cash = self.__withdrawal(pwd, id_from,
                        desc, amount)
            account = self.__accounts[id_from]
            balance = account.balance()
            s2 = f"{id_from}!cash;account_to_cash;"+\
                 f"\"${amount:.2f}\";"+\
                 f"\"${balance:.2f}\""
            #print(s2)
            self.__L.append(s2)
            return cash
        else:
            return 0
    def cash_to_account(self,id_to,desc,amount):
        account_id = id_to
        pwd = self.__pwds[account_id]
        enc_pwd = self.__encode(pwd)
        if self.authenticate_user(enc_pwd,
                    account_id):
            cash = amount
            self.__deposit(pwd, id_to,
                        desc, cash)
            account = self.__accounts[id_to]
            balance = account.balance()
            s2 = f"{id_to}?cash;cash_to_account;"+\
                 f"\"${amount:.2f}\";"+\
                 f"\"${balance:.2f}\""
            #print(s2)
            self.__L.append(s2)
            return
        else:
            return
    def __transaction(self,enc_pwd_AA,
            id_from,id_to,amount):
        if self.authenticate_AA(enc_pwd_AA):
            idx = self.__account_id
            desc_from = f"{idx}.{id_from}!{id_to}"
            desc_to = f"{idx}.{id_to}?{id_from}"
            cash = self.account_to_cash(
                id_from, desc_from, amount)
            self.cash_to_account(
                id_to,desc_to, cash)
            return
        return
    def transaction(self, enc_pwd_AA, s):
        #print(f"s = \"{s}\"")
        toks = s.split(';')
        toks2 = toks[0].split('!')
        id_from = int(toks2[0])
        id_to = int(toks2[1])
        amount = float(toks[1])
        self.__transaction(enc_pwd_AA,
            id_from,id_to,amount)
        return
    def report(self):
        s = '-'*30 + '\n'
        s = s + f"Account_Agency: {self.get_id()}\n"
        L1 = list(self.__accounts.keys())
        total_balance = 0
        for i in range(len(L1)):
            key = L1[i]
            account_i = self.__accounts[key]
            balance_i = account_i.balance()
            total_balance = total_balance + balance_i
            s = s + f"  {i}) {account_i}\n"
        s = s + f"  Total Balance: \""+\
            f"${total_balance:.2f}\"\n"
        pwd = self.__pwd
        s = s + "  Transactions:\n"
        enc_pwd = self.__encode(pwd)
        T = self.get_transactions(enc_pwd)
        for j in range(len(T)):
            x = T[j]
            t = f"    {j}) {x}\n"
            s = s + t
        s = s + '-'*30
        return s
    def __str__(self):
        s = '-'*30 + '\n'
        s = s + f"Account_Agency: {self.get_id()}\n"
        L1 = list(self.__accounts.keys())
        total_balance = 0
        for i in range(len(L1)):
            key = L1[i]
            account_i = self.__accounts[key]
            balance_i = account_i.balance()
            total_balance = total_balance + balance_i
            s = s + f"  {i}) {account_i}\n"
        s = s + f"  Total Balance: \""+\
            f"${total_balance:.2f}\"\n"
        pwd = self.__pwd
        s = s + '-'*30
        return s        
    def __repr__(self):
        return str(self)            
    def change_password(self,
                enc_pwd_AA,
                old_pwd, new_pwd,
                account_id):
        if self.authenticate_AA(enc_pwd_AA): 
            old_pwd_encoded = self.__encode(old_pwd)
            new_pwd_encoded = self.__encode(new_pwd)

            L1 = list(self.__accounts.keys())
            L2 = list(self.__pwds.keys())
            L3 = list(self.__names.keys())
            L4 = list(self.__attempts.keys())
            L5 = list(self.__locks.keys())
            
            assert(L1 == L2 and L1 == L3 and \
                   L1 == L4 and L1 == L5)
            for key in L1:
                flag1 = (key == account_id)
                flag2 = (self.__pwds[account_id] \
                         == old_pwd_encoded)
                flag = flag1 + flag2
                if flag:
                    self.__pwds[key] = \
                        new_pwd_encoded
                    self.__locks[key] = False
                    self.__attempts[key] = 0
            return "Password changed."
        return "Error: Password not changed."
    def get_account(self, pwd, account_id, name):
        pwd_encoded = self.__encode(pwd)
        L1 = list(self.__accounts.keys())
        L2 = list(self.__pwds.keys())
        L3 = list(self.__names.keys())
        L4 = list(self.__attempts.keys())
        L5 = list(self.__locks.keys())
        
        assert(L1 == L2 and L1 == L3 and \
               L1 == L4 and L1 == L5)
        for key in L1:
            flag1 = (key == account_id)
            flag2 = (self.__pwds[account_id] \
                     == pwd_encoded)
            flag3 = (self.__names[account_id] \
                     == name)
            flag = flag1 + flag2
            if flag:
                account = self.__accounts[key]
        return account
    def set_account(self, pwd_AA, pwd,
                    account_id, name,
                    account):
        pwd_encoded = self.__encode(pwd)
        L1 = list(self.__accounts.keys())
        L2 = list(self.__pwds.keys())
        L3 = list(self.__names.keys())
        L4 = list(self.__attempts.keys())
        L5 = list(self.__locks.keys())
        
        assert(L1 == L2 and L1 == L3 and \
               L1 == L4 and L1 == L5)
        for key in L1:
            flag1 = (key == account_id)
            flag2 = (self.__pwds[account_id] \
                     == pwd_encoded)
            flag3 = (self.__names[account_id] \
                     == name)
            flag = flag1 + flag2
            if flag:
                self.__accounts[key] = account
        return account
    def open_account(self, enc_pwd_AA,
                     pwd, name,
                     balance):
        if not self.authenticate_AA(enc_pwd_AA): 
            print("Error: AA not authenticated")
            return None
        pwd_enc = self.__encode(pwd)
        L1 = list(self.__accounts.keys())
        L2 = list(self.__pwds.keys())
        L3 = list(self.__names.keys())
        L4 = list(self.__attempts.keys())
        L5 = list(self.__locks.keys())
        
        assert(L1 == L2 and L1 == L3 and \
               L1 == L4 and L1 == L5)
        key = self.__idx
        print(f"Opening account \"{name}\"")
        account = acc_m.Account(key, name,balance)
        self.__accounts[key] = account
        self.__pwds[key] = pwd_enc
        self.__names[key] = name
        self.__attempts[key] = 0
        self.__locks[key] = 0
        self.__idx = self.__idx + 1
        if not self.authenticate_user(
                    self.__encode(pwd_enc),
                        key):
            print("Account not validated.")
            del self.__accounts[key]
            del self.__pwds[key]
            del self.__names[key]
            del self.__attempts[key]
            del self.__locks[key]
            self.__idx = self.__idx - 1
        name2 = self.__names[key]
        balance2 = self.__accounts[key].balance()
        print(f"opening account. \"{name2}\", "+\
              f"balance = \"${balance2:.2f}\"")
        return key
    def close_account(self, enc_pwd_AA, pwd,
                      account_id, name):
        if not self.authenticate_AA(enc_pwd_AA): 
            print("Error: AA not authenticated")
            return 0
        enc_pwd = self.__encode(self.__encode(pwd))
        if not self.authenticate_user(enc_pwd,
                        account_id):
            print("Error: User not authenticated")
            return 0
        L1 = list(self.__accounts.keys())
        L2 = list(self.__pwds.keys())
        L3 = list(self.__names.keys())
        L4 = list(self.__attempts.keys())
        L5 = list(self.__locks.keys())
        
        assert(L1 == L2 and L1 == L3 and \
               L1 == L4 and L1 == L5)
        amount = 0 # this must be zero
        for key in L1:
            flag1 = (key == account_id)
            flag3 = (self.__names[key] \
                     == name)
            flag = flag1 + flag3
            if flag:
                n = self.__names[key]
                account = self.__accounts[key]
                amount = account.balance()
                del self.__accounts[key]
                del self.__pwds[key]
                del self.__names[key]
                del self.__attempts[key]
                del self.__locks[key]
                print(f"closing account. \"{n}\", "+\
                      f"balance = \"${amount:.2f}\"")
        return amount
    def __withdrawal(self, pwd, account_id,
                desc, amount):
        enc_pwd = self.__encode(pwd)
        if not self.authenticate_user(enc_pwd,
                        account_id):
            return 0
        L1 = list(self.__accounts.keys())
        L2 = list(self.__pwds.keys())
        L3 = list(self.__names.keys())
        L4 = list(self.__attempts.keys())
        L5 = list(self.__locks.keys())
        
        assert(L1 == L2 and L1 == L3 and \
               L1 == L4 and L1 == L5)
        result = 0 # this must be zero
        for key in L1:
            flag = (key == account_id)
            if flag:
                result = self.__accounts[key].\
                         withdrawal(desc,amount)
        return result
    def __deposit(self, pwd, account_id,
                desc, amount):
        enc_pwd = self.__encode(pwd)
        if not self.authenticate_user(enc_pwd,
                        account_id):
            return 0
        L1 = list(self.__accounts.keys())
        L2 = list(self.__pwds.keys())
        L3 = list(self.__names.keys())
        L4 = list(self.__attempts.keys())
        L5 = list(self.__locks.keys())
        
        assert(L1 == L2 and L1 == L3 and \
               L1 == L4 and L1 == L5)
        result = 0 # this must be zero
        for key in L1:
            flag = (key == account_id)
            if flag:
                result = self.__accounts[key].\
                         deposit(desc,amount)
        return result
