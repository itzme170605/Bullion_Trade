#modules
import streamlit as st
import os 
import csv
from datetime import datetime,timedelta
import requests
import yfinance as yf
import pandas as pd
import mysql.connector as sqltor
import random 
import tabulate as tb
from sqlalchemy import create_engine
import pymysql
import numpy as np
from PIL import Image
import tabulate as tb
#connections
mycon=sqltor.connect(user='root',host='localhost',password='170605Vot',database='bullion')
if mycon.is_connected():
    cur=mycon.cursor()
engine=create_engine("mysql+pymysql://root:170605Vot@localhost/bullion", pool_size=30, max_overflow=100)

#page orientation
st.set_page_config(layout='wide')
#containers
homepage=st.container()
loginpage=st.container()
signuppage=st.container()
accounttype=st.container()
dashboardpageofnl=st.container()
dashboardpageonl=st.container()
accinfopage=st.container()
tradepage=st.container()
transactpage=st.container()
logoutpage=st.container()
actionpage=st.container()
adminpage=st.container()
passwdchange=st.container()
downloadpage=st.container()
#functions

#to check internet connection
def check_connection():
    url='https://www.google.com/'
    
    while True:
        try:
            request=requests.get(url,timeout=20)
            return True
        except:
            return False

#unique_transaction id 
def trans_id():
    n=random.randint(1,99999999)
    cur.execute(f"select transaction_id from trans_hist where transaction_id={n}")
    d=cur.fetchall()
    if d:
        trans_id()
    else:
        return n






def ofnl_plt(filename,a1):
    
    f=open(filename,'r')
    r=csv.reader(f)
    global high,low
    high=[]
    low=[]
    vol=[]
    date_list=[]
    openclose=[]
    
    for i in r:
        dtae=datetime.strptime(i[0][:10],'%Y-%m-%d').date()
        openclose+=[[float(i[1]),float(i[4])]]
        date_list+=[dtae]
        high+=[float(i[2])]
        low+=[float(i[3])]
        vol+=[float(i[6])]


    
    randomnumber=random.randint(0,len(high)-5)
    randomdate=date_list[randomnumber]
    randomhigh=high[randomnumber]
    randomlow=low[randomnumber]
    randomvol=vol[randomnumber]
    randomopen=openclose[randomnumber][0]
    randomclose=openclose[randomnumber][1]
    stockdata={'high':high,'low':low}
    coldata={'Volume':vol}
    #high_df=pd.DataFrame(high,date_list)
    df=pd.DataFrame(stockdata,index=date_list)
    vol_df=pd.DataFrame(coldata,date_list)
    #low_df=pd.DataFrame(low,date_list)
    #a1,a2=st.columns((5 ,3))
    with a1:
        
        a1.title("Graph 📉")
        a1.line_chart(df,height=300)
        a1.line_chart(vol_df,width=75,height=250)
        #a1.line_chart(low_df)
        #a1.button("Click")
    

    #
    #st.line_chart(data=high,x=date_list,width=200)
    #st.line_chart(low)
    #st.line_chart(vol)

    
    #plt.plot(date_list[::7],low[::7],label='Low',linewidth=1.0,color='red')
    #plt.plot(date_list[::7],high[::7],label='High',linewidth=1.0,color='green')
    

    #plt.ylabel('rates')    
    #plt.xlabel('Dates')
    #plt.title(filename+' Graph')
    #plt.show()
    #st.pyplot()
    f.close()
    return randomdate,randomhigh,randomlow,randomvol,randomopen,randomclose  


#main
with homepage:

    
    if 'homestate' not in st.session_state:
        st.session_state['homestate']=0
        st.experimental_rerun()

    else:

        if st.session_state['homestate']==0:
            h1,h2=st.columns((8,1))
            
            h1.title(":moneybag: itzTRADE :chart: ")
            h1.header(" :euro: :dollar: -BULLION TRADE- :pound: :currency_exchange:")
            h1.write("""
## What is Bullion Trade?

A bullion market is a market through which buyers and sellers trade gold and silver as well as 
associated derivatives.
There are various bullion markets around the world with the London Bullion Market known as the primary global market 
trading platform for gold and silver.

## What does this include?

### Gold
Gold is the oldest precious metal known to man and for thousands of years it has been valued as a global currency, 
a commodity, an investment and simply an object of beauty :ring: 

### Silver 
The main source of silver is lead ore, although it can also be found associated with copper, zinc and gold and produced 
 as a by-product of base metal mining activities.

## :classical_building: :chart_with_upwards_trend: How is the market affected? :chart_with_downwards_trend:

:point_right: Above-ground supply of gold from central bank sales, reclaimed scrap, and official gold loans.

:point_right: Hedging interest of producers and miners.

:point_right: World macroeconomic factors, such as movement in the dollar and interest rate, and economic events.

:point_right: In India, gold demand is also influenced by seasonality, that is, marriage and harvesting.

## what we do?
we help you invest in this everchanging market and make marginal profits
by providing all the information we can

## What you Can Trade here at 'itzTRADE'?

:point_right: Gold

:point_right: GOLD MICRO

:point_right: SILVER

:point_right:  MCX

:point_right: MCXNS

:point_right: Crude OIl

:point_right: Natural Gas

:point_right: INR/USD





*disclaimer- This is a datascience project no real money transaction takes place

""")
            
            #button=h2.selectbox('Welcome!',['log in','Sign up','admin'])
            if h2.button("Log in"):
                st.session_state['homestate']=1
                st.experimental_rerun()
            elif h2.button("Sign up"):
                st.session_state['homestate']=2
                st.experimental_rerun()
            elif h2.button("Admin"):
                st.session_state['homestate']=5
                st.experimental_rerun()
            
        
        elif st.session_state['homestate']==1:

            with loginpage:

                st.title(" :pushpin: LOGIN")

                if 'loggedin' not in st.session_state:
                    st.session_state['loggedin']=False
                    st.experimental_rerun()

                
                else:
                    if st.session_state['loggedin']:
                        st.session_state['homestate']=3
                        del st.session_state['loggedin']
                        st.experimental_rerun()

                    else:
                        def login_check():
                            cur.execute(f'select * from user_basic_ofnl where username="{uname}" and passwd="{passwd}";')
                            d=cur.fetchall()
                            if d:
                                st.session_state['userinfo']=[uname,passwd]
                                st.session_state['loggedin']=True
                                st.success("Logged in",icon="✅")
                            else:

                                st.session_state['loggedin']=False
                                st.error("Invalid username or password",icon="🚨")


                        uname=st.text_input("Username",'',max_chars=15)
                        passwd=st.text_input("Password:","",max_chars=15,type='password')
                        st.button("Log in",on_click=login_check)
                        if st.button("Back(double click)"):
                            st.session_state['homestate']=0
                            del st.session_state['loggedin']
                            st.experimental_rerun()


        elif st.session_state['homestate']==2:

            with signuppage:

                st.title(":pushpin: Create account")

                if 'accountcreated' not in st.session_state:
                    st.session_state['accountcreated']=False
                    st.experimental_rerun()

                else:
                    if st.session_state['accountcreated']:
                        st.session_state['homestate']=1
                        del st.session_state['accountcreated']
                        st.experimental_rerun()

                    else:

                        def check_user():
                            cur.execute(f'select * from user_basic_ofnl where username="{uname}"')
                            d=cur.fetchall()
                            if d or passwd!=cpasswd:
                                st.session_state['accountcreated']=False
                                st.error("Username Not available,or passwords donot match Choose Another",icon="🚨")
                            else:
                                
                                cur.execute(f"insert into user_basic_ofnl(username,passwd,fname,dob) values('{uname}','{passwd}','{fname}','{dob}');")
                                mycon.commit()
                                st.session_state['accountcreated']=True
                                st.success("Accounted Created!",icon="✅")



                        st.write("Enter all details")

                        fname=st.text_input("First Name:",key='firstname',max_chars=15)
                        uname=st.text_input("Username:",key='username',max_chars=15)
                        dob=st.date_input("DOB")
                        passwd=st.text_input("Password",'',max_chars=15,type='password',key='p1')
                        cpasswd=st.text_input("Confirm Password",'',max_chars=15,type='password',key='p2')


                        
                        st.button("Create Account",on_click=check_user)

                        if st.button("Back(double click)"):
                            st.session_state['homestate']=0
                            del st.session_state['accountcreated']
                            st.experimental_rerun()
                
        elif st.session_state['homestate']==3:

            
#def logout():
#   del st.session_state['homestate']
#   del st.session_state['accounttype']
#  st.experimental_rerun()


            with accounttype:

                tb1,tb2=st.columns((9,1))
                #to log out
                if tb2.button('Logout'):
                    for key in st.session_state.keys():
                        del st.session_state[key]

                    st.experimental_rerun()

                st.write("_________________________________________________________________________________")
                if 'accounttype' not in st.session_state:
                    tb1.title(":pushpin: Choose Type")
                    picture=Image.open('image1.jpg')
                    t1,t2,t3=st.columns((1,3,1))
                    
                    t2.image(picture,width=500)

                    if t2.button("Lets Trade"):
                        st.session_state['accounttype']=1
                        st.experimental_rerun()

                    
                else:

                    if st.session_state['accounttype']==1:

                        with dashboardpageofnl:
                            
                            if 'dashboardstate' not in st.session_state:
                                #d1,d2=st.columns((9,1))
                                st.title(" :pushpin: :euro: :dollar: -BULLION TRADE- :pound: :currency_exchange:")
                                st.header(f"Welcome! Signed in as '{st.session_state['userinfo'][0]}' to your account")
                                st.write("____________________________________________________________________________________________")
                                nn,db4,db5,nn=st.columns((1,2,2,1))
                                db2,db3,db1=st.columns(3)
                                
                                with db1:
                                    
                                    img1=Image.open('image5.png')#to change later
                                    db1.image(img1,width=300)
                                    if db1.button(":lock: Account INFORMATION ✅"):
                                        st.session_state['dashboardstate']=1
                                        st.experimental_rerun()


                                with db2:
                                    img2=Image.open('image6.jpg')
                                    db2.image(img2,width=300) 
                                    if st.button(":moneybag: TRADE :chart_with_upwards_trend: "):
                                        st.session_state['dashboardstate']=2
                                        st.experimental_rerun()  
                                
                                with db3:

                                    img3=Image.open("image8.jpg")

                                    db3.image(img3,width=300)
                                    if db3.button(":key: Change Password :lock:"):
                                        st.session_state['dashboardstate']=3
                                        st.experimental_rerun()      
                            else:
                                
                                if st.session_state['dashboardstate']==1:
                                    
                                    def transdetails():
                                        
                                        cur.execute(f"select * from trans_hist where username='{st.session_state['userinfo'][0]}' order by date_time_transaction;")
                                        d=cur.fetchall()
                                        cur.execute(f"select sum(amt) as 'profit/loss' from trans_hist where username='{st.session_state['userinfo'][0]}';")
                                        d1=cur.fetchall()
                                        cur.execute(f"select stock_name, sum(units) from trans_hist where username='{st.session_state['userinfo'][0]}' group by stock_name;")
                                        d2=cur.fetchall()

                                        #print(tabulate(<2d list>,headers=<list of headers>, tablefmt='psql'))
                                        #st.write(tb(d,headers=['Trans id','username','stock name','stock price','units','Type','Amount','Trade type','Date Time'],tablefmt='psql'))
                                        st.table(d)
                                        st.write("# :pushpin: Other details:")
                                        st.write("Profit/loss")
                                        st.table(d1)
                                        st.table(d2)

                                    with accinfopage:
                                        ac0,ac1,ac2=st.columns((2,5,2))
                                        ac1.title(":pushpin: ACCOUNT INFORMATION")
                                        
                                        st.write('______________________________________________________________________________')
                                        inf=st.session_state['userinfo']
                                        p1=ac1.text_input("Verify",max_chars=15,type='password',key='verification')
                                        if ac1.button("Submit"):
                                            st.write("________________________________________________________________________________")
                                            cur.execute(f"select * from user_basic_ofnl where username='{inf[0]}' and passwd='{p1}'")
                                            d=cur.fetchall()
                                            if d:
                                                ac1.success("Verrified",icon='✅')
                                                ac1.header("Account details:")
                                                ac1.table(d)
                                                #makechange to path 
                                                img=Image.open('img10.png')
                                                ac2.image(img,width=75)
                                                ac2.button("Transaction Details",on_click=transdetails)
                                                #img4=Image.open("mk4\images\analytics.jpg")
                                                #ac2.image(img4,width=75)
                                                #ac2.button("Account Analytics", on_click=analyse)
                                                
                                            else:
                                                st.error("Passwords donot match",icon="🚨")
                                        
                                        if ac0.button("Back"):
                                            del st.session_state['dashboardstate']
                                            st.experimental_rerun()



#tradepage

                                elif st.session_state['dashboardstate']==2:



                                    with tradepage:

                                        def transconfirmedbuy():
                                            cur.execute(f"insert into trans_hist values({trans_id()},'{st.session_state['userinfo'][0]}','{filename}',{rate},{st.session_state['units']},'BUY',{-1*rate*st.session_state['units']},'ofnl', CURRENT_TIMESTAMP);")
                                            cur.execute(f"Update user_basic_ofnl set bal=bal-{amt};")
                                            mycon.commit()
                                            st.success("Transaction sucessful",icon='✅')
                                            st.session_state['tradepagestate'][0]='GOLD'
                                            st.experimental_rerun()

                                        def transconfirmedsell():        
                                            cur.execute(f"Select sum(units) from trans_hist where username='{st.session_state['userinfo'][0]}' and stock_name='{filename}'")
                                            d=cur.fetchall()
                                            for i in d:
                                                owned=i[0]
                                            if owned>=st.session_state['units']:

                                                cur.execute(f"insert into trans_hist values({trans_id()},'{st.session_state['userinfo'][0]}','{filename}',{rate},{-1*st.session_state['units']},'SELL',{rate*st.session_state['units']},'ofnl',CURRENT_TIMESTAMP);")

                                                cur.execute(f"Update user_basic_ofnl set bal=bal+{amt};")
                                                mycon.commit()
                                                st.success("Transaction sucessful",icon='✅')
                                            else:
                                                st.error("Not enough units owned")
                                            
                                            st.experimental_rerun()



                                        if 'tradepagestate'  not in st.session_state:
                                            st.write("LOADING PAGE! Plese wait")
                                            st.session_state['tradepagestate']=0
                                            st.experimental_rerun()
                                        else:
                                            
                                            def rate_reloader(comodity):
                                                
                                            
                                            if st.button("Back"):
                                                del st.session_state['tradepagestate']
                                                del st.session_state['dashboardstate']
                                                st.experimental_rerun()

                                            st.title(":chart_with_downwards_trend: TRADE :chart_with_upwards_trend: ")
                                            st.write("# Choose")
                                            st.write("_________________________________________________________________________________________")
                                            st.sidebar.title('SEARCH :mag:')
                                            st.session_state['tradepagestate']=st.sidebar.selectbox("",options=['GOLD (GC=F)','SILVER (SI=F)','GOLDM (MGC=F)','INR /USD (INR=X)','CRUDEOIL (CL=F)','NATURALGAS (NG=F)','MCXNS (MCX.NS)']).split()
                                            
                                            if st.session_state['tradepagestate']:
                                                
                                                filename=st.session_state['tradepagestate'][0]
                                                filename=filename.lower()+'.csv'
                                                tp1,tp2=st.columns((4,2))
                                                d,h,l,v,open,cl=ofnl_plt(filename,tp1)


                                                rate=random.randrange(int(l)-2,int(h))
                                                
                                                with tp2:
                                                    tp2.title(":moneybag: Quote")
                                                    
                                                    f"""


Rate: {rate}

Open: {open} \t\t

Close: {cl}

high: {h} \t\t 

Low: {l}

sell: {rate*1.1} \t\t 

stoploss: {rate*0.9}


*Data taken from {d} from database


*Can only buy and sell 50 units

                                                    
                                                    
                                                    """
                                                    st.session_state['units']=int(tp2.text_input("Units(int)",value='0'))
                                                    if tp2.button("BUY :money: "):
                                                        if st.session_state['units']:
                                                            amt=st.session_state['units']*rate
                                                            cur.execute(f"select bal from user_basic_ofnl where username='{st.session_state['userinfo'][0]}';")
                                                            d=cur.fetchall()
                                                            for i in d:
                                                                bal=i[0]
                                                                break

                                                            if float(bal) > (amt+1000):
                                                                tp2.write(f"""Transaction Details:

Total Amount: {float(amt)}

units= {st.session_state['units']}
                                                                
                                                                """)
                                                                
                                                                tp2.button("Confirm",on_click=transconfirmedbuy)
                                                                    

                                                                
                                                                if tp2.button("Cancel"):

                                                                    st.experimental_rerun()

                                                    if tp2.button("Sell"):
                                                        
                                                        if st.session_state['units']:
                                                            amt=st.session_state['units']*rate
                                                            tp2.write(f"""Transaction Details:

Total Amount: {amt}

units= {st.session_state['units']}
                                                                
                                                                """)
                                                            tp2.button("Confirm", on_click=transconfirmedsell)
                                                                
                                                            if tp2.button("Cancel"):

                                                                st.experimental_rerun()

                                            


                                elif st.session_state['dashboardstate']==3:
                                    


                                    with passwdchange:
                                        st.title("Password Change!! :lock: :key:")
                                        
                                        if 'passwordchange' not in st.session_state:
                                            st.session_state['verify']=st.text_input("Password","",max_chars=15,type="password")

                                            if st.button("Verify"):
                                                if(st.session_state['verify']==st.session_state['userinfo'][1]):
                                                    st.success("Account Verified",icon='✅')
                                                    st.session_state['passwordchange']=True
                                                    st.experimental_rerun()
                                                else:
                                                    st.error("Wrong Password",icon="🚨")
                                            

                                        else:
                                            if st.session_state['passwordchange']:
                                                a1,a2,a3=st.columns((1,5,1))
                                                np1=a2.text_input("NEW PASSWORD",max_chars=15,type='password',key='Newpassword')
                                                np2=a2.text_input("Confirm Password","",key='cpasswordnew',max_chars=15,type='password')
                                                if st.button("Confirm"):
                                                    if np1==np2:
                                                        st.session_state['userinfo'][1]=np1
                                                        cur.execute(f"Update user_basic_ofnl set passwd='{st.session_state['userinfo'][1]}' where username='{st.session_state['userinfo'][0]}';")
                                                        mycon.commit()
                                                        st.success("Password changed",icon="✅")
                                                    else:
                                                        st.error("Passwords must match",icon="🚨")


                                        if st.button("Back"):
                                            del st.session_state['dashboardstate']
                                            del st.session_state['passwordchange']
                                            st.experimental_rerun() 



                    elif st.session_state['accounttype']==2:
                        with dashboardpageonl:
                            st.write("Onl out of scope")
                        with dashboardpageofnl:
                            
                            if 'dashboardstate' not in st.session_state:
                                #d1,d2=st.columns((9,1))
                                st.title(" :pushpin: :euro: :dollar: -BULLION TRADE- :pound: :currency_exchange:")
                                st.header(f"Welcome! Signed in as '{st.session_state['userinfo'][0]}' to offlinie account")
                                st.write("____________________________________________________________________________________________")
                                nn,db4,db5,nn=st.columns((1,2,2,1))
                                db2,db3,db1=st.columns(3)
                                
                                with db1:
                                    
                                    img1=Image.open('mk4\image5.png')#to change later
                                    db1.image(img1,width=300)
                                    if db1.button(":lock: Account INFORMATION ✅"):
                                        st.session_state['dashboardstate']=1
                                        st.experimental_rerun()


                                with db2:
                                    img2=Image.open('mk4\image6.jpg')
                                    db2.image(img2,width=300) 
                                    if st.button(":moneybag: OFFLINE TRADE :chart_with_upwards_trend: "):
                                        st.session_state['dashboardstate']=2
                                        st.experimental_rerun()  
                                
                                with db3:

                                    img3=Image.open("mk4\image8.jpg")

                                    db3.image(img3,width=300)
                                    if db3.button(":key: Change Password :lock:"):
                                        st.session_state['dashboardstate']=3
                                        st.experimental_rerun()      
                            else:
                                
                                if st.session_state['dashboardstate']==1:
                                    
                                    def transdetails():
                                        
                                        cur.execute(f"Select * from trans_hist where username='{st.session_state['userinfo'][0]}' order by date_time_transaction;")
                                        d=cur.fetchall()
                                        cur.execute(f"select sum(amt) as 'profit/loss' from trans_hist where username='{st.session_state['userinfo'][0]}';")
                                        d1=cur.fetchall()
                                        cur.execute(f"select stock_name, sum(units) from trans_hist where username='{st.session_state['userinfo'][0]}' group by stock_name;")
                                        d2=cur.fetchall()
                                                                                    
                                        #print(tabulate(<2d list>,headers=<list of headers>, tablefmt='psql'))
                                        #st.write(tb(d,headers=['Trans id','username','stock name','stock price','units','Type','Amount','Trade type','Date Time'],tablefmt='psql'))
                                        st.table(d)
                                        st.write("# :pushpin: Other details:")
                                        st.write("Profit/loss")
                                        st.table(d1)
                                        st.table(d2)

                                    with accinfopage:
                                        ac0,ac1,ac2=st.columns((2,5,2))
                                        ac1.title(":pushpin: ACCOUNT INFORMATION")
                                        
                                        st.write('______________________________________________________________________________')
                                        inf=st.session_state['userinfo']
                                        p1=ac1.text_input("Verify",max_chars=15,type='password',key='verification')
                                        if ac1.button("Submit"):
                                            st.write("________________________________________________________________________________")
                                            cur.execute(f"select * from user_basic_ofnl where username='{inf[0]}' and passwd='{p1}'")
                                            d=cur.fetchall()
                                            if d:
                                                ac1.success("Verrified",icon='✅')
                                                ac1.header("Account details:")
                                                ac1.table(d)
                                                #makechange to path 
                                                img=Image.open('mk4\img10.png')
                                                ac2.image(img,width=75)
                                                ac2.button("Transaction Details",on_click=transdetails)
                                                #img4=Image.open("mk4\images\analytics.jpg")
                                                #ac2.image(img4,width=75)
                                                #ac2.button("Account Analytics", on_click=analyse)
                                                
                                            else:
                                                st.error("Passwords donot match",icon="🚨")
                                        
                                        if ac0.button("Back"):
                                            del st.session_state['dashboardstate']
                                            st.experimental_rerun()



#tradepage

                                elif st.session_state['dashboardstate']==2:



                                    with tradepage:

                                        def transconfirmedbuy():
                                            cur.execute(f"insert into trans_hist values({trans_id()},'{st.session_state['userinfo'][0]}','{filename}',{rate},{st.session_state['units']},'BUY',{-1*rate*st.session_state['units']},'ofnl', CURRENT_TIMESTAMP);")
                                            cur.execute(f"Update user_basic_ofnl set bal=bal-{amt};")
                                            mycon.commit()
                                            st.success("Transaction sucessful",icon='✅')
                                            st.session_state['tradepagestate'][0]='GOLD'
                                            st.experimental_rerun()

                                        def transconfirmedsell():        
                                            cur.execute(f"Select sum(units) from trans_hist where username='{st.session_state['userinfo'][0]}' and stock_name='{filename}'")
                                            d=cur.fetchall()
                                            for i in d:
                                                owned=i[0]
                                            if owned>=st.session_state['units']:

                                                cur.execute(f"insert into trans_hist values({trans_id()},'{st.session_state['userinfo'][0]}','{filename}',{rate},{-1*st.session_state['units']},'SELL',{rate*st.session_state['units']},'ofnl',CURRENT_TIMESTAMP);")

                                                cur.execute(f"Update user_basic_ofnl set bal=bal+{amt};")
                                                mycon.commit()
                                                st.success("Transaction sucessful",icon='✅')
                                            else:
                                                st.error("Not enough units owned")
                                            
                                            st.experimental_rerun()



                                        if 'tradepagestate'  not in st.session_state:
                                            st.write("LOADING PAGE! Plese wait")
                                            st.session_state['tradepagestate']=0
                                            st.experimental_rerun()
                                        else:
                                            
                                            
                                            if st.button("Back"):
                                                del st.session_state['tradepagestate']
                                                del st.session_state['dashboardstate']
                                                st.experimental_rerun()

                                            st.title(":chart_with_downwards_trend: OFFLINE TRADE :chart_with_upwards_trend: ")
                                            st.write("# Choose")
                                            st.write("_________________________________________________________________________________________")
                                            st.sidebar.title('SEARCH :mag:')
                                            st.session_state['tradepagestate']=st.sidebar.selectbox("",options=['GOLD (GC=F)','SILVER (SI=F)','GOLDM (MGC=F)','INR /USD (INR=X)','CRUDEOIL (CL=F)','NATURALGAS (NG=F)','MCXNS (MCX.NS)']).split()
                                            
                                            if st.session_state['tradepagestate']:
                                                
                                                filename=st.session_state['tradepagestate'][0]
                                                filename=filename.lower()+'.csv'
                                                tp1,tp2=st.columns((4,2))
                                                d,h,l,v,open,cl=ofnl_plt(filename,tp1)


                                                rate=random.randrange(int(l)-2,int(h))
                                                
                                                with tp2:
                                                    tp2.title(":moneybag: Quote")
                                                    
                                                    f"""


Rate: {rate}

Open: {open} \t\t

Close: {cl}

high: {h} \t\t 

Low: {l}

sell: {rate*1.1} \t\t 

stoploss: {rate*0.9}


*Data taken from {d} from database


*Can only buy and sell 50 units

                                                    
                                                    
                                                    """
                                                    st.session_state['units']=int(tp2.text_input("Units(int)",value='0'))
                                                    if tp2.button("BUY :money: "):
                                                        if st.session_state['units']:
                                                            amt=st.session_state['units']*rate
                                                            cur.execute(f"select bal from user_basic_ofnl where username='{st.session_state['userinfo'][0]}';")
                                                            d=cur.fetchall()
                                                            for i in d:
                                                                bal=i[0]
                                                                break

                                                            if float(bal) > (amt+1000):
                                                                tp2.write(f"""Transaction Details:

Total Amount: {float(amt)}

units= {st.session_state['units']}
                                                                
                                                                """)
                                                                
                                                                tp2.button("Confirm",on_click=transconfirmedbuy)
                                                                    

                                                                
                                                                if tp2.button("Cancel"):

                                                                    st.experimental_rerun()

                                                    if tp2.button("Sell"):
                                                        
                                                        if st.session_state['units']:
                                                            amt=st.session_state['units']*rate
                                                            tp2.write(f"""Transaction Details:

Total Amount: {amt}

units= {st.session_state['units']}
                                                                
                                                                """)
                                                            tp2.button("Confirm", on_click=transconfirmedsell)
                                                                
                                                            if tp2.button("Cancel"):

                                                                st.experimental_rerun()

                                            


                                elif st.session_state['dashboardstate']==3:
                                    


                                    with passwdchange:
                                        st.title("Password Change!! :lock: :key:")
                                        
                                        if 'passwordchange' not in st.session_state:
                                            st.session_state['verify']=st.text_input("Password","",max_chars=15,type="password")

                                            if st.button("Verify"):
                                                if(st.session_state['verify']==st.session_state['userinfo'][1]):
                                                    st.success("Account Verified",icon='✅')
                                                    st.session_state['passwordchange']=True
                                                    st.experimental_rerun()
                                                else:
                                                    st.error("Wrong Password",icon="🚨")
                                            

                                        else:
                                            if st.session_state['passwordchange']:
                                                a1,a2,a3=st.columns((1,5,1))
                                                np1=a2.text_input("NEW PASSWORD",max_chars=15,type='password',key='Newpassword')
                                                np2=a2.text_input("Confirm Password","",key='cpasswordnew',max_chars=15,type='password')
                                                if st.button("Confirm"):
                                                    if np1==np2:
                                                        st.session_state['userinfo'][1]=np1
                                                        cur.execute(f"Update user_basic_ofnl set passwd='{st.session_state['userinfo'][1]}' where username='{st.session_state['userinfo'][0]}';")
                                                        mycon.commit()
                                                        st.success("Password changed",icon="✅")
                                                    else:
                                                        st.error("Passwords must match",icon="🚨")


                                        if st.button("Back"):
                                            del st.session_state['dashboardstate']
                                            del st.session_state['passwordchange']
                                            st.experimental_rerun() 


        elif st.session_state['homestate']==5:

            with loginpage:

                st.title(" :pushpin: ADMIN LOGIN")

                if 'admloggedin' not in st.session_state:
                    st.session_state['admloggedin']=False
                    st.experimental_rerun()

                
                else:
                    if st.session_state['admloggedin']:
                        st.session_state['homestate']=6
                        del st.session_state['admloggedin']
                        st.experimental_rerun()

                    else:
                        def login_check():
                            
                            if uname=='admin' and passwd=='admin':
                                
                                st.session_state['admloggedin']=True
                                st.success("Logged in",icon="✅")
                                st.experimental_rerun()

                            else:

                                st.session_state['admloggedin']=False
                                st.error("Invalid username or password",icon="🚨")
                                


                        uname=st.text_input("Username",'',max_chars=15)
                        passwd=st.text_input("Password:","",max_chars=15,type='password')
                        st.button("Log in",on_click=login_check)
                        if st.button("Back(double click)"):
                            st.session_state['homestate']=0
                            del st.session_state['admloggedin']
                            st.experimental_rerun()

        elif st.session_state['homestate']==6:
            
            ad1,ad2=st.columns((9,1))
            
            
            st.title(":pushpin: Admin")
            if ad2.button("Log out"):
                st.session_state['homestate']=0
                st.experimental_rerun()
            st.write("____________________________________________________________________________________________________________")
            st.header("Logged in as Admin")
            st.write("_____________________________________________________________________________________________________________")

            a0,a1,a2,a3=st.columns((1,2,2,1))

            with a1:
                img5=Image.open("mk4\images\doenload.jpg")
                a1.image(img5)
                
                if a1.button("Add ofline data"):
                    st.session_state['homestate']=7
                    st.experimental_rerun()
        elif st.session_state['homestate']==7:

            with downloadpage:
                ad1,ad2=st.columns((9,1))
                
                
                st.title(":pushpin: Admin")
                if ad2.button("Log out"):
                    st.session_state['homestate']=0
                    st.experimental_rerun()
                if ad2.button("back"):
                    st.session_state['homestate']=6
                    st.experimental_rerun()
                st.write("____________________________________________________________________________________________________________")
                st.header("Logged in as Admin")
                st.write("_____________________________________________________________________________________________________________")

                if check_connection():

                    if 'stockname' not in st.session_state:
                        st.session_state['stockname']=0 #st.selectbox("Select the stock",options=['GOLD (GC=F)','SILVER (Sl=F)','GOLDM (MGC=F)','INR/USD (INR=X)','CRUDEOIL (CL=F)','NATURALGAS (NG=F)','MCX (MCX.DO)','MCXNS (MCX.NS)'],key='select_stock')
                        st.experimental_rerun()
                    else:

                        if st.session_state['stockname']==0:
                            if st.button("GOLD"):
                                st.session_state['stockname']=['GC=F',"GOLD"]
                                
                                st.experimental_rerun()
                            if st.button("SILVER"):
                                st.session_state['stockname']=["SI=F","SILVER"]
                                
                                st.experimental_rerun()

                            if st.button("GOLDM"):
                                st.session_state['stockname']=["MGC=F","GOLDM"]
                                
                                st.experimental_rerun()

                            if st.button("INR/USD"):
                                st.session_state['stockname']=["INR=X","INR"]
                                
                                st.experimental_rerun()

                            if st.button("Crude OIL"):
                                st.session_state['stockname']=["CL=F","CRUDEOIL"]
                                
                                st.experimental_rerun()
                            if st.button("Natural Gas"):
                                st.session_state['stockname']=["NG=F","NATURALGAS"]
                                
                                st.experimental_rerun()
                            if st.button("MCX"):
                                st.session_state['stockname']=["MCX.DO","MCX"]
                                st.experimental_rerun()

                            if st.button("MCXNS"):
                                st.session_state['stockname']=["MCX.NS","MCXNS"]
                                

                                st.experimental_rerun()

                        else:

                            data=yf.download(st.session_state['stockname'][0],datetime.now()-timedelta(days=365),datetime.now())
                            
                            data.to_sql(st.session_state['stockname'][1],con=engine,if_exists='append',chunksize=1000)
                            
                            mycon.commit()
                            filename=st.session_state['stockname'][1].lower()
                            cur.execute("Use bullion;")
                            cur.execute(f"select * from {filename};")

                            d=cur.fetchall()
                            
                            f=open(filename+'.csv','w',newline='')
                            writer=csv.writer(f)

                            writer.writerows(d)
                            f.close()
                            del st.session_state['stockname']
                            
                            st.success("Data downloaded",icon="✅")
                            st.experimental_rerun()
                else:
                    st.error("No network connection",icon='🚨')




            






            











    




