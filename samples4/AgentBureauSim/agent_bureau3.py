import account_agency3 as aca

import time
from datetime import datetime

from pint import UnitRegistry

ureg = UnitRegistry("./myunits3.txt")
Q_ = ureg.Quantity

class Agent_Bureau:
    def __init__(self, account_id, SA, pwd, amount, domain):
        self.__account_id = account_id
        self.__SA = SA
        self.__agencies = {}
        self.__pwds = {}
        self.__names = {}
        self.__idx = len(list(self.__agencies.keys()))
        self.__encode = SA.get_encode()
        self.__pwd = self.__encode(pwd)
        self.__balance = amount
        self.__receipts = {}
        self.__sig_idx = 0
        self.__signatures = {}
        self.__domains = {}
        self.__mydomain = domain
        return
    def __currency_exchange(self, agency_id1, cash1,
                agency_id2):
        xx1 = Q_(cash1,
            self.__agencies[agency_id1].get_domain())
        xx2 = xx1.to(self.__agencies[agency_id2].get_domain())
        cash2 = xx2.magnitude        
        return cash2
    def get_mydomain(self):
        return self.__mydomain
    def get_domain(self, agency_id, account_id):
        agent = self.__agencies[agency_id]
        domain = agent.get_domain()
        return domain
    def create_signature(self, agency_id, account_id):
        key = (agency_id, account_id)
        val = self.__sig_idx
        val_s = f"{val:09.0f}" # sign_len = 8
        self.__signatures[key] = val_s
        self.__sig_idx = val + 1
        return val_s
    def get_signature(self, agency_id, account_id):
        key = (agency_id, account_id)
        L = list(self.__signatures.keys())
        if key in L:
            val = self.__signatures[key]
        else:
            val = 0
        return val
    def parse_signature(self, sig):
        L = list(self.__signatures.keys())
        for key in L:
            if str(self.__signatures[key]) == str(sig):
                return key
        return None
    def __make_receipt(self, pwd, agency_id, account_id):
        s = str(time.time())
        key1 = '-'.join([pwd,s,str(agency_id),str(account_id)])
        key2 = self.__encode(key1)
        return key2
    def __send_receipt(self,key,val):
        L = list(self.__receipts.keys())
        if key not in L:
            self.__receipts[key] = val
        return
    def __recv_receipt(self, key):
        L = list(self.__receipts.keys())
        val = None
        if key in L:
            val = self.__receipts[key]
            del self.__receipts[key]
        return val
    def get_id(self):
        return self.__account_id
    def __str__(self):
        s = f'\nAgent Bureau: {self.get_id()}\n'
        L1 = list(self.__agencies.keys())
        for i in range(len(L1)):
            key = L1[i]
            agent = self.__agencies[key]
            s = s + str(agent)            
        return s
    def report(self):
        s = f'\nAgent Bureau: {self.get_id()}\n'
        L1 = list(self.__agencies.keys())
        for i in range(len(L1)):
            key = L1[i]
            agent = self.__agencies[key]
            s = s + agent.report()            
        return s        
    def __repr__(self):
        return str(self)
    def balance(self):
        return self.__balance
    def get_user_balance(self,agent_id,account_id):
        agent = self.__agencies[agent_id]
        val = agent.get_user_balance(account_id)
        return val
    def __authenticate_AB(self, encoded_pwd):
        enc_pwd1 = self.__encode(self.__pwd)
        enc_pwd2 = encoded_pwd
        flag = enc_pwd1 == enc_pwd2
        return flag
    def __authenticate_user(self, encoded_pwd,
                account_id):
        K = list(self.__agencies.keys())
        if account_id in K:
            pwd = self.__pwds[account_id]
            enc_pwd1 = self.__encode(pwd)
            enc_pwd2 = encoded_pwd
            flag = enc_pwd1 == enc_pwd2
            return flag
        else:
            return False
    def open_agency(self, pwd_AB,
            pwd, name, domain):
        enc_pwd_AB = self.__encode(pwd_AB)
        if not self.__authenticate_AB(enc_pwd_AB): 
            print("Error: AB not authenticated")
            return None
        pwd_enc = self.__encode(pwd)
        L1 = list(self.__agencies.keys())
        L2 = list(self.__pwds.keys())
        L3 = list(self.__names.keys())
        assert((L1 == L2) and (L1 == L3))
        key = self.__idx
        print(f"Opening agency \"{name}\"")
        AA = aca.Account_Agency(self.__SA, pwd, key,
                    domain)
        self.__agencies[key] = AA
        self.__pwds[key] = pwd_enc
        self.__names[key] = name
        self.__domains[key] = domain
        self.__idx = self.__idx + 1
        if not self.__authenticate_user(
                    self.__encode(pwd_enc),
                        key):
            print("Agency not validated.")
            del self.__agencies[key]
            del self.__pwds[key]
            del self.__names[key]
            del self.__domains[key]
            self.__idx = self.__idx - 1
        name2 = self.__names[key]
        balance2 = self.__agencies[key].balance()
        print(f"opening agency. \"{name2}\", "+\
              f"balance = \"${balance2:.2f}\"")
        return key     
    def close_agency(self, pwd, name):
        if not self.__authenticate_AB(enc_pwd_AB): 
            print("Error: AB not authenticated")
            return None
    def open_account(self, enc_pwd_AB,enc_pwd_AA,
                     agent_id, pwd, name, balance):
        enc2_pwd_AB = self.__encode(enc_pwd_AB)
        if not self.__authenticate_AB(enc2_pwd_AB):
            print("Error: AB not authenticated")
            return None
        enc2_pwd_AA = self.__encode(enc_pwd_AA)
        if not self.__authenticate_user(enc2_pwd_AA,
                agent_id):
            print("Error: AA not authenticated")
            return None
        key = self.__agencies[agent_id].open_account(
            enc_pwd_AA, pwd, name, balance)
        sig = self.create_signature(agent_id,key)        
        return sig
    def close_account(self, enc_pwd_AB,enc_pwd_AA,
                     sig, pwd, name):
        enc2_pwd_AB = self.__encode(enc_pwd_AB)
        if not self.__authenticate_AB(enc2_pwd_AB):
            print("Error: AB not authenticated")
            return None
        enc2_pwd_AA = self.__encode(enc_pwd_AA)
        if not self.__authenticate_user(enc2_pwd_AA,
                agent_id):
            print("Error: AA not authenticated")
            return None
        agent_id,account_id = self.parse_signature(sig)
        amount = self.__agencies[agent_id].close_account(
            enc_pwd_AA, pwd, account_id, name)
        return amount
    def Date(self,seconds):
         return datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')
    def YYMMDD(self,seconds):
         return datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d')
    def Seconds(self,year,month,day):
         sec = (datetime(year,month,day)-datetime(1970,1,1)).total_seconds()
         return sec
    def __transaction(self,enc_pwd_AB,pwd,
            agency_id1,id_from,
            agency_id2,id_to,
            amount, get_receipt):

        flag1 = enc_pwd_AB == self.__pwd
        enc_AA_pwd = self.__pwds[agency_id1]
        agency = self.__agencies[agency_id1]
        
        enc_pwd = self.__encode(pwd)
        enc2_pwd = self.__encode(enc_pwd)
        flag3 = agency.authenticate_user(
            enc2_pwd, id_from)
        #print(flag1,flag3)
        
        flag = flag1 and flag3
        key = None
        if flag:
            idx1 = agency_id1
            idx2 = agency_id2
            desc_from = f"{idx1}.{id_from}!{id_to}"
            desc_to = f"{idx2}.{id_to}?{id_from}"
            
            cash1 = self.__agencies[agency_id1].\
                   account_to_cash(
                    id_from, desc_from, amount)

            cash2 = self.__currency_exchange(
                agency_id1, cash1, agency_id2)
            
            self.__agencies[agency_id2].cash_to_account(
                id_to,desc_to, cash2)
            
            if get_receipt:
                key = self.__make_receipt(pwd, \
                            agency_id1, id_from)
                self.__send_receipt(key,cash2)
        return key
    def transaction(self,enc_pwd_AB, pwd, s,
                    get_receipt):
        print(f"transaction: msg = {s}")
        #msg = f"{key_AA1}:{key1}!{key_AA2}:{key2};{amount}"
        toks1 = s.split(';')
        hdr = toks1[0]
        toks2 = hdr.split('!')
        sig1 = toks2[0]
        sig2 = toks2[1]

        P = self.parse_signature
        agency_id1,id_from  = P(sig1)
        agency_id2,id_to = P(sig2)

        amount = float(toks1[1])
        key = self.__transaction(enc_pwd_AB,pwd,
            agency_id1,id_from,
            agency_id2,id_to,
            amount,get_receipt)
        return key
    def __transaction_recv(self,enc_pwd_AB,key,
            agency_id1,id_from,
            agency_id2,id_to):
        flag = enc_pwd_AB == self.__pwd
        enc_AA_pwd = self.__encode(self.__pwd)
        val = self.__recv_receipt(key)
        if val is None:
            return
        if flag:
            idx1 = agency_id1
            idx2 = agency_id2
            desc_from = f"{idx1}.{id_from}!{id_to}"
            desc_to = f"{idx2}.{id_to}?{id_from}"
            cash1 = self.__agencies[agency_id1].\
                       account_to_cash(id_from,
                            desc_from, val)

            cash2 = self.__currency_exchange(
                agency_id1, cash1, agency_id2)
            
            self.__agencies[agency_id2].cash_to_account(
                id_to,desc_to, cash2)
        return
    def transaction_recv(self,enc_pwd_AB, key, s):
        print(f"transaction: msg = {s}")
        #msg = f"{key_AA1}:{key1}!{key_AA2}:{key2};{amount}"
        toks1 = s.split(';')
        hdr = toks1[0]
        toks2 = hdr.split('!')

        sig1 = toks2[0]
        sig2 = toks2[1]

        P = self.parse_signature
        agency_id1,id_from  = P(sig1)
        agency_id2,id_to = P(sig2)

        amount = float(toks1[1])
        self.__transaction_recv(enc_pwd_AB,key,
            agency_id1,id_from,
            agency_id2,id_to)
        return    


