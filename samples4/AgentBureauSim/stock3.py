import random
        
# fix random seed for this
seed0 = 12345
random.seed(seed0)

class Stock:
    def __init__(self,
                 AB, enc_pwd_AB,
                 key_from,
                 key_to,
                 t,
                 ticker_symbol,
                 stock_price,
                 period, current_yield, p,
                 volatility=1, pwd=""):
        key_AA_from,key_from = \
                AB.parse_signature(key_from)
        key_AA_to, key_to = \
                AB.parse_signature(key_to)
        self.__key_AA_from = key_AA_from
        self.__key_from = key_from
        self.__key_AA_to = key_AA_to
        self.__key_to = key_to
        
        self.__AB = AB
        self.__enc_pwd_AB = enc_pwd_AB
        
        self.__name =  ticker_symbol
        self.__value = stock_price
        self.__p = p
        self.__volatility = volatility # one unit of change
        self.__t = t
        self.__dt = 1
        self.__graph = []
        # self.period is amount of years
        self.__period = period # dividend period
        # dividend interest rate
        self.__percent = current_yield
        self.__cost = 0
        self.__receipt = None
        self.__receipt2 = None
        self.__pwd = pwd
    def transaction(self, s):
        receipt = self.__AB.transaction(\
                self.__enc_pwd_AB, self.__pwd,
                s, get_receipt=True)
        self.set_receipt(receipt)
    def set_receipt(self,receipt):
        self.__receipt2 = receipt
        return
    def get_receipt(self):
        return self.__receipt2
    def get_agency_id1(self):
        return self.__key_AA_from
    def get_agency_id2(self):
        return self.__key_AA_to
    def get_id_from(self):
        return self.__key_from
    def get_id_to(self):
        return self.__key_to
    def deposit(self, desc, amount):
        key_AA1 = self.__key_AA_from
        key1 = self.__key_from
        key_AA2 = self.__key_AA_to
        key2 = self.__key_to
        G = self.__AB.get_signature
        sig1 = G(key_AA2, key2)
        sig2 = G(key_AA1, key1)
        s = f"{sig1}!{sig2};"+\
            f"{amount:.2f};{desc}_deposit_"+\
            f"{key_AA1}:{key1}"
        receipt = self.__AB.transaction(\
                self.__enc_pwd_AB,
                self.__pwd, s, get_receipt=True)
        self.__receipt = receipt
        return
    def withdrawal(self, desc, amount):
        key_AA1 = self.__key_AA_from
        key1 = self.__key_from
        key_AA2 = self.__key_AA_to
        key2 = self.__key_to
        G = self.__AB.get_signature
        sig1 = G(key_AA1, key1)
        sig2 = G(key_AA2, key2)
        s = f"{sig1}!{sig2};"+\
            f"{amount:.2f};{desc}_withdrawal_"+\
            f"{key_AA1}:{key1}"
        self.__AB.transaction_recv(self.__enc_pwd_AB,
                    self.__receipt, s)

        return 0
    def name(self):
        return self.__name
    def amount(self):
        return self.__value
    def sim_step(self):
        p = random.uniform(0,1)
        if p <= self.__p:
            X = 1
        else:
            X = -1
        self.__value = self.__value + X*self.__volatility
        # clamp self.value to a positive value
        self.__value = max(0,self.__value)
        pt = (self.__t,self.__value)
        self.__graph.append(pt)
        self.__t = self.__t + self.__dt
        return
    def __str__(self):
        s = f"Stock:{self.__name}:${self.__value:.2f}"
        return s
    def __repr__(self):
        return str(self)
    def profit(self, qty):
        # get dividend on at the end of a period
        x = self.__t % self.__period
        y = self.__period - self.__dt
        flag = abs(x - y) < self.__dt
        if flag:
            scale = qty*(self.__percent/100)
            value = self.__value*scale
        else:
            value = 0
        return value
    def revenue(self, qty):
        return self.profit(qty) - qty*self.__cost
