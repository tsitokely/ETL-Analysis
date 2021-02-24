# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 10:05:20 2017

@author: toe
"""

import sys
import datetime as dt
import sqlite3 as lite

now = dt.datetime.now()
previous_date = now - dt.timedelta(days = 1)
deleteTable_prevDay = "DROP TABLE purge%s;" % previous_date.strftime("%Y%m%d")

currDate = now.strftime("%Y%m%d")
orig_stdout = sys.stdout

allTablesQuery = "SELECT name FROM sqlite_master WHERE type='table';"
dbcon = lite.connect(r"WORK_PATH\\Purge\\suivi_purge.db")
cur = dbcon.cursor()
cur.execute(allTablesQuery)
tables = cur.fetchall()

createTable_today = """CREATE TABLE purge%s (
    msisdn_9                   TEXT,
    plan_tarifaire             TEXT,
    imsi                       TEXT,
    serial_number              TEXT,
    plan_tarifaire_desc        TEXT,
    Statut_FT                  TEXT,
    Statut_MarketShare         TEXT,
    Statut_ChargedBase         TEXT,
    Statut_Data30j             TEXT,
    Statut_Sortant7j           TEXT,
    Statut_Data7j              TEXT,
    KYC                        TEXT,
    Statut_IN                  TEXT,
    main_account               REAL,
    date_activation            TEXT,
    anciennete                 TEXT,
    date_inactif               TEXT,
    date_desactivation         TEXT,
    duree_inactivite           INTEGER,
    last_recharge              TEXT,
    stk_flag                   INTEGER,
    user_type_OM_USSD          TEXT,
    Statut_OM_USSD             TEXT,
    Date_creation_OM_USSD      TEXT,
    OM_date_registration       TEXT,
    OM_date_last_transaction   TEXT,
    OM_balance                 REAL,
    OM_last_transaction_type   TEXT,
    OM_last_transaction_amount TEXT,
    OM_user_grade              TEXT,
    Channel_balance            REAL,
    Channel_account_type       TEXT,
    Channel_user_domain        TEXT,
    Channel_user_category      TEXT,
    site_id                    TEXT,
    Flag_priorite1             INTEGER,
    Flag_priorite2             INTEGER,
    Flag_priorite3             INTEGER,
    Flag_priorite4             INTEGER,
    Flag_priorite5             INTEGER,
    Flag_priorite6             INTEGER,
    Flag_priorite7             INTEGER,
	Flag_priorite8             INTEGER
);""" % currDate
filename_sql = "insert_purge.sql"

f = open(r"WORK_PATH\\%s" % filename_sql, 'wb')
sys.stdout = f
print ".mode csv"
print ".separator ';'"

for i in tables:
    deleteTable = "DROP TABLE %s;" % i[0]
    print deleteTable

print "vacuum;"
print createTable_today
print ".import working_file%s.csv purge%s" % (currDate,currDate)
print "vacuum;"

sys.stdout = orig_stdout
f.close()