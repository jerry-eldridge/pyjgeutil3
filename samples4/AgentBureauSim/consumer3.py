import portfolio3 as port_m
import option3 as opts_m

class Consumer:
    def __init__(self,
                 AB,enc_pwd_AB,
                 id_from,
                 id_to,
                 S, Q, O,
                 max_options=1,
                 pwd=""):
        agency_id1, id_from = \
                AB.parse_signature(id_from)
        agency_id2, id_to = \
                AB.parse_signature(id_to)
        self.__AB = AB
        self.__enc_pwd_AB = enc_pwd_AB
        self.__agency_id1 = agency_id1 # account
        self.__id_from = id_from
        self.__agency_id2 = agency_id2 # cash
        self.__id_to = id_to        
        self.__t = 0
        self.__idx = 0
        self.__max_options = max_options
        self.__P = port_m.Portfolio(
                 AB, enc_pwd_AB,
                 agency_id1, id_from,
                 agency_id2, id_to,
                 S,Q,O, pwd)
        self.__account_id = self.__id_from
        self.__name = str(self.__id_from)
        self.__pwd1 = pwd
        return
    def balance(self):
        val = self.__AB.get_user_balance(
                self.__agency_id1,
                self.__id_from)
        return val
    def get_portfolio(self):
        return self.__P
    def __str__(self):
        
        s = f"Consumer_{self.__account_id}:\n"+\
            f"{self.__P}\n"
        for i in range(len(self.__P.stocks())):
            stock = self.__P.stocks()[i]
            qty = self.__P.qtys()[i]
            s = s + f"  {qty} x {stock}\n"
        for i in range(len(self.__P.get_options())):
            option = self.__P.get_options()[i]
            s = s + f"  {option}\n"
        total = self.balance() + \
                self.__P.worth()
        s = s + f"Total: ${total:.2f}\n"
        s = s + "="*30
        return s
    def __repr__(self):
        return str(self)
    def update_options(self):
        O = self.__P.get_options()
        I = range(len(O))
        J = []
        for i in range(len(O)):
            opt = O[i]
            if self.__t >= opt.stop():
                J.append(i)
        K = list(set(I)-set(J))
        self.__P.set_options([O[i] for i in K])
        return
    def sim_step(self):
        self.__t = self.__P.t()
        self.update_options()
        I = [opt.rec().idx for opt in self.__P.get_options()]
        print(f"{self.__name} Options indices: I = {I}")
        self.__P.sim_step()   
        self.__t = self.__P.t()
        return
    def strategize(self, S_names,expires,
                   budget,price_option,
                   wealth_thresh):
        t_now = self.__t
        
        for name in S_names:
            noptions = len(self.__P.get_options())
            if (self.balance() > \
                wealth_thresh and \
                noptions < self.__max_options and \
                budget >= price_option):
                L = [self.__AB,
                         self.__enc_pwd_AB,
                         self.__agency_id1,
                         self.__id_from,
                         self.__agency_id2,
                         self.__id_to,
                         self.__pwd1,
                     ]
                opt1 = opts_m.CreateOption(
                         L,
                        [name,t_now, self.__idx,
                        "buy",price_option,
                        expires])
                self.__P.add_option(opt1)
                self.__idx = self.__idx + 1
                budget = budget - price_option
            noptions = len(self.__P.get_options())
            if (self.balance() <= \
                wealth_thresh and \
                noptions < self.__max_options):
                L = [self.__AB,
                         self.__enc_pwd_AB,
                         self.__agency_id1,
                         self.__id_from,
                         self.__agency_id2,
                         self.__id_to,
                         self.__pwd1,
                     ]
                opt2 = opts_m.CreateOption(
                         L,
                        [name,t_now, self.__idx,
                        "sell",price_option,
                        expires])
                self.__P.add_option(opt2)
                self.__idx = self.__idx + 1
                budget = budget + price_option
        return
