from collections import namedtuple

OptTup = namedtuple("Option",
        ["name","now","idx","type",
         "price","expires"])

class Option:
    def __init__(self,
            AB, enc_pwd_AB,
            agency_id1, id_from,
            agency_id2, id_to, pwd,
                 rec):
        self.__AB = AB
        self.__enc_pwd_AB = enc_pwd_AB
        self.__agency_id1 = agency_id1
        self.__id_from = id_from
        self.__agency_id2 = agency_id2
        self.__id_to = id_to
        self.__rec = rec
        self.__start = rec.now
        self.__stop = rec.now + rec.expires
        self.__name = rec.name
        self.__pwd = pwd
    def stop(self):
        return self.__stop
    def rec(self):
        return self.__rec
    def __str__(self):
        name = self.__name
        start = self.__start
        stop = self.__stop
        rec = self.__rec
        s = f"Option:{name}:"+\
            f"[{start}:{stop}]:{rec}"
        return s
    def __repr__(self):
        return str(self)
    def process(self,t,stock,stock_qty):
        T = list(range(self.__start,self.__stop+1))

        #if t not in T:
        #    return 0
        
        if stock.name() != self.__name:
            return 0

        G = self.__AB.get_signature

        #print("Option:process")
        amount = self.__rec.price
        # buy or sell if stock.amount() greater than
        # buying price at times
        if (self.__rec.type == "buy"):
            flag = stock.amount() >= self.__rec.price
            if flag:
                print(f"used option = {self.__rec}")                  
                qty = 1
                agency_id1 = self.__agency_id1
                id_from = self.__id_from
                agency_id2 = self.__agency_id2
                id_to = self.__id_to

                sig1 = G(agency_id1,id_from)
                sig2 = G(agency_id2,id_to)
                s = f'{sig1}!{sig2};'+\
                    f'{amount:.2f};option_bought'

                receipt = self.__AB.transaction(\
                    self.__enc_pwd_AB, self.__pwd,
                    s, get_receipt=True)
                
                agency_id2 = stock.get_agency_id2()
                id_to = stock.get_id_to()
                agency_id1 = stock.get_agency_id1()
                id_from = stock.get_id_from()
                sig1 = G(agency_id2,id_to)
                sig2 = G(agency_id1,id_from)
                s = f'{sig1}!{sig2};'+\
                    f'{amount:.2f};option_bought'
                self.__AB.transaction_recv(\
                    self.__enc_pwd_AB, receipt, s)                
            return qty
        elif (self.__rec.type == "sell"):
            flag = stock.amount() >= self.__rec.price
            if flag:
                print(f"used option = {self.__rec}")                  
                qty = -1
                if stock_qty + qty >= 0:
                    agency_id1 = stock.get_agency_id1()
                    id_from = stock.get_id_from()
                    agency_id2 = stock.get_agency_id2()
                    id_to = stock.get_id_to()

                    sig1 = G(agency_id1,id_from)
                    sig2 = G(agency_id2,id_to)
                    s = f'{sig1}!{sig2};'+\
                        f'{amount:.2f};option_sold'
                    stock.transaction(s)
                    agency_id1 = self.__agency_id1
                    id_from = self.__id_from
                    agency_id2 = self.__agency_id2
                    id_to = self.__id_to
                    
                    sig1 = G(agency_id2,id_to)
                    sig2 = G(agency_id1,id_from)
                    s = f'{sig1}!{sig2};'+\
                        f'{amount:.2f};option_sold'
                    self.__AB.transaction_recv(\
                        self.__enc_pwd_AB,
                        stock.get_receipt(), s)
                else:
                    s = f"Error: option not used.."+\
                        f"no shares to sell!"
                    print(s)
                    qty = 0
            return qty
        else:
            return 0

def CreateOption(A,L):
    return Option(*A,OptTup._make(L))
