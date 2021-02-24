# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import datetime
import csv

now = datetime.datetime.now()

currdate = now.strftime("%Y%m%d")
orig_stdout = sys.stdout

dbcon = lite.connect(r"WORK_PATH\\Purge\\suivi_purge.db")

#Analysis of current day turnover
cur = dbcon.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
nomtable = tables[0][0]
nomtable = nomtable.decode("utf-8")
cur.execute("select count(*) from purge%s" % currdate)
rownumber = cur.fetchone()
rownum = rownumber[0]
cur.execute("select msisdn_9 from purge%s group by msisdn_9 having count(*)>1;" % currdate)
duplicate = cur.fetchall()
cur.execute("select count(*) from purge%s where Flag_priorite1 = 1 or Flag_priorite2 = 1 or Flag_priorite3 = 1 or Flag_priorite4 = 1 or Flag_priorite5 = 1 or Flag_priorite6 = 1;" % currdate)
flagnumber = cur.fetchone()

# Priorité 1 
cur.execute("""select count(*) from purge%s 
where
Statut_FT = 'INACTIF'
and
KYC = '' -- KYC
and
Statut_IN = 'Desactive'
and
stk_flag = 0
and
date(OM_date_registration) is null
and
main_account = '0.00'
and
Channel_user_category = '\N'
and
(Channel_balance = '\N' or Channel_balance = 0);""" % currdate)
P1Q = cur.fetchone()
cur.execute("select count(*) from purge%s where Flag_priorite1 = 1;" % currdate)
P1F = cur.fetchone()
P1diff = P1Q[0] - P1F[0]

# Priorité 2 
cur.execute("""select count(*) from purge%s
where
Statut_FT = 'INACTIF'
and
KYC = ''
and
Statut_IN = 'Inactif'
and
stk_flag = 0
and
date(OM_date_registration) is null
and
main_account = '0.00'
and
Channel_user_category = '\N'
and
(Channel_balance = '\N' or Channel_balance = 0)
and 
cast(duree_inactivite as int) >365
and
(date(last_recharge) < date('now','-1 year','-1 day')
or date(last_recharge) is null)""" % currdate)
P2Q = cur.fetchone()
cur.execute("select count(*) from purge%s where Flag_priorite2 = 1;" % currdate)
P2F = cur.fetchone()
P2diff = P2Q[0] - P2F[0]

# Priorité 3 
cur.execute("""select count(*) from purge%s
where
Statut_FT = 'INACTIF'
and
KYC = '' 
and
Statut_IN = 'Inactif'
and
stk_flag = 0
and
OM_date_registration = '\N'
and
(round(main_account,2) <= 50.00 
and round(main_account,2) > 0.00)
and
Channel_user_category = '\N'
and
(Channel_balance = '\N' or Channel_balance = 0)
and 
cast(duree_inactivite as int) >365
and
(date(last_recharge) < date('now','-1 year','-2 day')
or date(last_recharge) is null)""" % currdate)
P3Q = cur.fetchone()
cur.execute("select count(*) from purge%s where Flag_priorite3 = 1" % currdate)
P3F = cur.fetchone()
P3diff = P3Q[0] - P3F[0]

# Priorité 4 
cur.execute("""select count(*) from purge%s
where
Statut_FT = 'INACTIF'
and
KYC = ''
and
Statut_IN = 'Inactif'
and
stk_flag = 0
and
date(OM_date_registration) is null
and
main_account = '0.00'
and
Channel_user_category = '\N'
and
(Channel_balance = '\N' or Channel_balance = 0)
and 
cast(duree_inactivite as int) <= 365 
and
cast(duree_inactivite as int) > 180
and
(date(last_recharge) < date('now','-1 year','-2 day')
or date(last_recharge) is null)""" % currdate)
P4Q = cur.fetchone()
cur.execute("select count(*) from purge%s where Flag_priorite4 = 1" % currdate)
P4F = cur.fetchone()
P4diff = P4Q[0] - P4F[0]

# Priorité 5 
cur.execute("""select count(*) from purge%s
where
Statut_FT = 'INACTIF'
and
KYC = '' 
and
Statut_IN = 'Inactif'
and
stk_flag = 0
and
OM_date_registration = '\N'
and
(round(main_account,2) <= 50.00
and round(main_account,2) > 0.00)
and
Channel_user_category = '\N'
and
(Channel_balance = '\N' or Channel_balance = 0)
and 
cast(duree_inactivite as int) <= 365 
and
cast(duree_inactivite as int) > 180
and
(date(last_recharge) < date('now','-1 year','-2 day')
or date(last_recharge) is null)""" % currdate)
P5Q = cur.fetchone()
cur.execute("select count(*) from purge%s where Flag_priorite5 = 1" % currdate)
P5F = cur.fetchone()
P5diff = P5Q[0] - P5F[0]

# Priorité 6 
cur.execute("""select count(*) from purge%s
where
Statut_FT = 'INACTIF'
and
KYC = '' 
and
Statut_IN = 'Inactif'
and
stk_flag = 0
and
OM_date_registration = '\N'
and
(round(main_account,2) <= 2000.00 
and round(main_account,2) > 50.00)
and
Channel_user_category = '\N'
and
(Channel_balance = '\N' or Channel_balance = 0)
and 
cast(duree_inactivite as int) > 365
and
(date(last_recharge) < date('now','-1 year','-2 day')
or date(last_recharge) is null)""" % currdate)
P6Q = cur.fetchone()
cur.execute("select count(*) from purge%s where Flag_priorite6 = 1" % currdate)
P6F = cur.fetchone()
P6diff = P6Q[0] - P6F[0]

# Priorité 7 
cur.execute("""select count(*) from purge%s
where
plan_tarifaire in('5001','5006','5007')
and
Statut_FT = 'INACTIF'
and
KYC = ''
and
Statut_IN = 'Inactif'
and
stk_flag = 0
and
date(OM_date_registration) is null
and
Channel_user_category = '\N'
and
(Channel_balance = '\N' or Channel_balance = 0)""" % currdate)
P7Q = cur.fetchone()
cur.execute("select count(*) from purge%s where Flag_priorite7 = 1" % currdate)
P7F = cur.fetchone()
P7diff = P7Q[0] - P7F[0]

# Priorité 8 
cur.execute("""select count(*) from purge%s
where
Statut_FT = 'INACTIF'
and
KYC = ''
and
Statut_IN = 'Inactif'
and
stk_flag = 0
and
date(OM_date_registration) is null
and
Channel_user_category = '\N'
and
(Channel_balance = '\N' or Channel_balance = 0) 
and
cast(duree_inactivite as int) >= 365""" % currdate)
P8Q = cur.fetchone()
cur.execute("select count(*) from purge%s where Flag_priorite8 = 1" % currdate)
P8F = cur.fetchone()
P8diff = P8Q[0] - P8F[0]

dbcon.close()

filename_log = "log_priority%s.txt" % currdate
f = file(r"WORK_PATH\\Purge\\Result\\%s" % filename_log, 'w')
sys.stdout = f



print "------------------ Analysis of table %s ------------------" % nomtable
print "- The table %s has %s rows" % (nomtable,rownum)
print "- There are %s duplicate in table %s: " % (len(duplicate),nomtable)
for i in duplicate:
    print i[0]

print "- %s MSISDN have a flag in the table %s" % (flagnumber[0],nomtable)
print ""

for x in range(1,9):
    PXQ = "P" + str(x) + "Q"
    PXF = "P" + str(x) + "F"
    PXdiff = "P" + str(x) + "diff"
    print "------------------ Priority %i ------------------" % x
    if eval(PXdiff) == 0 :
        print "Verification of Priority %i OK" % x
        print "Number of MSISDN with a flag priority %i: %i" % (x,eval(PXF)[0])
    else:
        print "The difference is: %i for priority %i " % (eval(PXdiff),x)
        print "Results of query %i" % eval(PXQ)[0]
        print "Results of flag %i" % eval(PXF)[0]
    print ""

sys.stdout = orig_stdout
f.close()

filename_csv = "result_purge_Query%s.csv" % currdate
f = open(r"WORK_PATH\\Purge\\Result\\%s" % filename_csv, 'wb')
try:
    writer = csv.writer(f,delimiter=";")
    writer.writerow( (u'Priority', 'Nombre MSISDN'))
    for i in range(1,9):
        PXQ = "P" + str(i) + "Q"
        priority = "Priority %s" % i
        writer.writerow((priority,eval(PXQ)[0]))
finally:
    f.close()

filename_csv = "result_purge_Flag%s.csv" % currdate
f = open(r"WORK_PATH\\Purge\\Result\\%s" % filename_csv, 'wb')
try:
    writer = csv.writer(f,delimiter=";")
    writer.writerow((u'Priority', 'Number of MSISDN'))
    for i in range(1,9):
        PXF = "P" + str(i) + "F"
        priority = "Priority %s" % i
        writer.writerow( (priority,eval(PXF)[0]))
finally:
    f.close()