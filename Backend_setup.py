import os 
import mysql.connector as sqltor
from datetime import datetime,timedelta
import yfinance as yf




mycon=sqltor.connect(host='localhost',user='root',password='170605Vot')
curr=mycon.cursor()
if mycon.is_connected():
    print("Connected to server")
try:
    curr.execute("Drop database Bullion")
    curr.execute("Create database Bullion")
except:
    curr.execute("Create database Bullion")
curr.execute("Use Bullion")

curr.execute("Create table user_basic_ofnl(username varchar(20) Primary Key, passwd varchar(20) NOT NULL, fname varchar(20) NOT NULL, DOB Date, Date_Time_account_creation datetime DEFAULT CURRENT_TIMESTAMP,bal float(10,2) default 100000, account_status varchar(10) Default 'Active',status varchar(10) default 'Offline');")
curr.execute("Create table user_basic_onl(username varchar(20) Primary Key, passwd varchar(20) NOT NULL, fname varchar(20) NOT NULL, DOB Date, Date_Time_account_creation datetime DEFAULT CURRENT_TIMESTAMP,bal float(10,2) default 100000, account_status varchar(10) Default 'Active',status varchar(10) default 'online');")
#curr.execute("Create table user_premium(username varchar(20) Primary Key, passwd varchar(20) NOT NULL, fname varchar(20) NOT NULL, DOB Date, Date_Time_account_creation datetime DEFAULT CURRENT_TIMESTAMP,bal float(10,2) default 2000000);")
curr.execute("Create table trans_hist(transaction_id bigint Primary Key,username Varchar(20) Not NULL, stock_name Char(20) Not null,  Stock_price float(10,2) NOT NULL, units int,transaction_type varchar(5),amt float(10,2), app_type varchar(10),date_time_transaction Datetime default CURRENT_TIMESTAMP);")
curr.execute("create table off_g(date date primary key,open float(15,6),high float(15,6),low float(15,6),close_price float(15,6),Adj_close float(15,6),volume bigint);")


mycon.commit()

mycon.close()







