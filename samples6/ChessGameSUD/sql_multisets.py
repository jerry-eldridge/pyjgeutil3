import sqlite3
class SQLMultisets:
    def __init__(self,db):
        self.db = db
        self.transactions = []
    def schema(self):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        s = f"SELECT sql from sqlite_master "+\
            f"where type='table';"
        try:
            res = cur.execute(s)
            names = res.fetchall()
            self.transactions.append(s)
        except:
            names = []
        con.close()
        return names
    def create(self, name_type):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        s = f"CREATE TABLE {name_type};"
        try:
            cur.execute(s)
            self.transactions.append(s)
        except:
            a = 1
        con.commit()
        con.close()
        return
    def insert(self, name, data):
        if len(data) == 0:
            return
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        try:
            t = '('+', '.join(["?"]*\
                    len(list(data[0])))+')'
            s = f"INSERT INTO {name} VALUES{t};"
            #print(s)
            #yn = input("pause> ")
            cur.executemany(s,data)
            self.transactions.append(s)
        except:
            a = 1
        con.commit()
        con.close()
        return
    def update(self, name, columns, values, condition):
        name = name.replace(';','')
        columns = [col.replace(';','') for col in columns]
        condition = condition.replace(';','')
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        try:
            s = f"UPDATE {name}\n"+\
                f"SET "+\
            ',\n'.join([f"{columns[i]} = '{values[i]}'" \
          for i in range(len(columns))]) +\
                f"\nWHERE\n"+\
                f"{condition};\n"
            print(s)
            yn = input("pause> ")
            cur.execute(s)
            self.transactions.append(s)
        except:
            a = 1
        con.commit()
        con.close()
        return
    def delete(self, name, condition):
        name = name.replace(';','')
        condition = condition.replace(';','')
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        try:
            s = f"DELETE FROM {name}\n"+\
                f"WHERE\n"+\
                f"{condition};\n"
            print(s)
            yn = input("pause> ")
            cur.execute(s)
            self.transactions.append(s)
        except:
            a = 1
        con.commit()
        con.close()
        return
    def select(self, tables, items, condition):
        tables = tables.replace(";","")
        items = items.replace(";","")
        condition = condition.replace(";","")
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        try:
            s = f"SELECT {items} \n"+\
                f"FROM {tables} \n"+\
                f"{condition};"
            print(s)
            res = cur.execute(s)
            L = res.fetchall()
            self.transactions.append(s)
        except:
            L = []
        con.commit()
        con.close()
        return L
    def drop(self,name):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        try:
            s = f"DROP TABLE {name};"
            cur.execute(s)
            self.transactions.append(s)
        except:
            a = 1
        con.commit()
        con.close()
        return
    def history(self):
        print()
        print("Transaction History:")
        print(f"S"*50)
        for s in self.transactions:
            print(s)
        print(f"S"*50)
        print()
        return
