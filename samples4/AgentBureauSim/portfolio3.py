from account3 import micropayment

# L is a list [... [qty, stock]_j ...]

class Portfolio:
    def __init__(self,
                 AB, enc_pwd_AB,
                 agency_id1, id_from,
                 agency_id2, id_to,
                 stocks, qtys, options,
                 pwd,
                 ):
        assert(len(stocks) == len(qtys))
        self.__AB = AB
        self.__enc_pwd_AB = enc_pwd_AB
        self.__stocks = stocks
        self.__qtys = qtys
        self.__t = 0
        self.__amount = 0
        self.__options = options
        self.__agency_id1 = agency_id1 # account
        self.__id_from = id_from
        self.__agency_id2 = agency_id2 # cash
        self.__id_to = id_to
        self.__name = str(agency_id1)
        self.__pwd = pwd
    def t(self):
        return self.__t
    def stocks(self):
        return self.__stocks
    def qtys(self):
        return self.__qtys
    def get_options(self):
        return self.__options
    def set_options(self, options):
        self.__options = options
        return
    def amount(self):
        return self.__amount
    def stock_names(self):
        names = [stock.name() for stock in self.__stocks]
        return names
    def sim_step(self):
        t = self.__t
        I = range(len(self.__stocks))
        # Update qty and earnings and time t
        print("="*30)
        receipt = None
        for j in I:
            stock = self.__stocks[j]
            stock_qty = self.__qtys[j]
            dividend = stock.revenue(self.__qtys[j])
            amount = dividend
            qty = 1
            if abs(amount) > micropayment:
                stock.withdrawal("dividend", amount)
                
                agency_id2 = stock.get_agency_id2()
                id_to = stock.get_id_to()
                agency_id1 = self.__agency_id1
                id_from = self.__id_from
                G = self.__AB.get_signature
                sig1 = G(agency_id2,id_to)
                sig2 = G(agency_id1,id_from)
                s = f'{sig1}!{sig2};'+\
                    f'{amount:.2f};dividend_'+\
                    f'added_to_portfolio'
                receipt = stock.get_receipt()
                self.__AB.transaction_recv(\
                    self.__enc_pwd_AB, receipt, s) 
                
            for i in range(len(self.__options)):
                qty = self.__options[i].process(\
                        t,stock,stock_qty)
                self.__qtys[j] = self.__qtys[j] + qty
        self.__t = self.__t + 1
        print("="*20)
        return
    def worth(self):
        current_value = 0
        for i in range(len(self.__stocks)):
            stock = self.__stocks[i]
            qty = self.__qtys[i]
            value = stock.amount()*qty
            current_value = current_value + value
        return current_value
    def __str__(self):
        name = self.__name
        Z = list(zip(self.__qtys,self.stock_names()))
        s = f"t={self.__t},Portfolio(name='{name}',"+\
            f"stocks={Z}, worth = ${self.worth():.2f})"
        return s
    def __repr__(self):
        return str(self)
    def add_option(self, option):
        flag = True
        for i in range(len(self.__options)):
            idx_i = self.__options[i].rec().idx
            if option.rec().idx == idx_i:
                flag = False
        if flag:
            self.__options.append(option)
        return
    def remove_option(self, idx):
        I = []
        for i in range(len(self.__options)):
            idx_i = self.__options[i].rec().idx
            if idx == idx_i:
                I.append(i)
        del self.__options[i]
        return
