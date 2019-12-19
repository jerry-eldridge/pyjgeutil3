import sqlite3
import re
import time
import os
import fnmatch
import os.path

db = r"C:\_sqlite_dbs\dirlist.db"
fn_all = "All-files-C.csv"

def CreateFile(fn0):
    f = open(fn0,'w')
    for root, dire, files in os.walk("c:/"):
        for fn in fnmatch.filter(files, "*.*"):
            try:
                filename = root + '\\' + fn
                mtime = int(os.path.getmtime(filename))
                size = os.stat(filename).st_size
                fnl,ext = os.path.splitext(filename)
                s = '%d,%d,\"%s\",\"%s\",\"%s\"\n' % (mtime, size, ext, root, fn)
                #dirname = os.path.dirname(filename)
                #basename = os.path.basename(filename)
                f.write(s)
            except:
                continue
    f.close()
    return

def DropTable():
    con = sqlite3.connect(db)
    cur = con.cursor()
    q = """
drop table dirlist;
"""
    print q
    try:
        cur.execute(q)
    except:
        i = 1
    con.commit()
    con.close()
    return

def CreateTable():
    con = sqlite3.connect(db)
    cur = con.cursor()
    q = """
create table DIRLIST (
   modified	int,
   size         int,
   ext          varchar(10),
   root		varchar(1000),
   fn		varchar(1000),
   primary key (root,fn,ext,modified)
);
"""
    print q
    cur.execute(q)
    con.commit()
    con.close()
    return

def PopulateTable(fn0):
    con = sqlite3.connect(db)
    cur = con.cursor()
    f = open(fn0,"r")
    print "Inserting into table"
    for line in f:
        vals = line.split(",")
        modified = int(vals[0])
        size = int(vals[1])
        ext = vals[2]
        root = vals[3]
        fn = vals[4]
        q = """
insert into DIRLIST values (%d,%d,%s,%s,%s);
""" % (modified,size,ext,root,fn)
        try:
            cur.execute(q)
        except:
            continue
    f.close()
    con.commit()
    con.close()
    return

def SelectTable(n):
    con = sqlite3.connect(db)
    cur = con.cursor()
    q = """
select * from DIRLIST limit %d;
""" % n
    print q
    cur.execute(q)
    for row in cur:
        print row
    return

def Find(field,val):
    con = sqlite3.connect(db)
    cur = con.cursor()
    q = """
select * from DIRLIST where
%s LIKE \"%s\";
""" % (field,val)
    print q
    cur.execute(q)
    for row in cur:
        print row
    return

#DropTable() # deletes/drops dirlist table
#CreateTable() # creates the dirlist table
#CreateFile(fn_all) # create txt file
#PopulateTable(fn_all) # populate with txt file

#Find("fn","%golfball%") # find files on computer via dirlist
