from numpy import exp, cos, linspace
import datetime
#from datetime import datetime
import matplotlib.dates as mdates
import matplotlib
matplotlib.use('Agg')
import os, time, glob
import pandas as ps
import socket
import datetime
from bs4 import BeautifulSoup
import matplotlib.pyplot as plot
from re import sub
from decimal import Decimal
import urllib
import pandas as ps
from bson import json_util, ObjectId
from pandas.io.json import json_normalize
import json
import numpy as np
import requests
from pymongo import MongoClient
import pandas as ps
ps.options.mode.chained_assignment = None  # default='warn'
from io import StringIO
import io
import base64
import random as random

#  activate database
#client = MongoClient('localhost:27017')
#client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'],27017)
#client = MongoClient(‘
#client = MongoClient(‘mongodb://test:test1@ds243085.mlab.com:43085/traderdb’)
#db = client.traderdb
DB_NAME = 'traderdb'
DB_HOST = 'ds243085.mlab.com'
DB_PORT = 43085
DB_USER = 'test'
DB_PASS = 'test1'

client = MongoClient(DB_HOST, DB_PORT)
db = client[DB_NAME]
db.authenticate(DB_USER, DB_PASS)

blotters = db.blotter #Select the collection
d = db.blotter.find().sort('Date', -1)
e = ps.DataFrame(json_normalize(json.loads(json_util.dumps(d))))

#the following section loads all the equities from the CSV file
df1 = ps.read_csv("companylist.csv")
df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]
df2 = df1.set_index("Symbol")

def mylist():
    df1 = ps.read_csv("companylist.csv")
    #drop random unnamed column name
    df1 = df1.loc[:, ~df1.columns.str.contains('^Unnamed')]
    return df1

def datahist(symbol):
    url = quotegrabber(symbol)+'/historical'
    import requests
        #page 1
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    table = soup.find('div', id="historicalContainer")
    header = ['Date','Open','High','Low','Close/Last','Volume']
    body = [[td.text.strip() for td in row.select('td') if td.text.strip() != ' ']
                 for row in table.findAll('tr')]
    body = [x for x in body if x != []]
    cols = zip(*body)
    tbl_d  = {name:col for name, col in zip(header,cols)}
    df = ps.DataFrame(tbl_d, columns = header)
    df = df[1:len(df)]
    h = df.columns.values.tolist()
    df['Volume'] = df['Volume'].replace({',': ''}, regex=True)
    for i in range (1,len(h)-1):
        df[h[i]] = df[h[i]].apply(ps.to_numeric, errors='coerce')
    z = df.describe().loc[['mean','std','mean','max']]
    return z
    
    

def historical(symbol):
    url = quotegrabber(symbol)+'/historical'
    import requests
        #page 1
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    table = soup.find('div', id="historicalContainer")
    header = ['Date','Open','High','Low','Close/Last','Volume']
    body = [[td.text.strip() for td in row.select('td') if td.text.strip() != ' ']
                 for row in table.findAll('tr')]
    body = [x for x in body if x != []]
    cols = zip(*body)
    tbl_d  = {name:col for name, col in zip(header,cols)}
    df = ps.DataFrame(tbl_d, columns = header)
    df = df[1:len(df)]
    x = ps.to_datetime(df['Date'])
    y = df['Close/Last']

#grab page 1  
    url2 = quotegrabber(symbol)+'/time-sales'
        #page 1
    r2 = requests.get(url2)
    data2 = r2.text
    soup2 = BeautifulSoup(data2, "lxml")
    table2 = soup2.find('div', id="quotes_content_left__panelTradeData")
    header2 = ['NLS Time (ET)','NLS Price','NLS Share Volume']
    body2 = [[td.text.strip() for td in row.select('td') if td.text.strip() != ' ']
                 for row in table2.findAll('tr')]
    body2 = [x for x in body2 if x != []]
    cols2 = zip(*body2)
    tbl_d2  = {name:col for name, col in zip(header2,cols2)}
    dft = ps.DataFrame(tbl_d2, columns = header2)

#grab page 2
    url3 = quotegrabber(symbol)+'/time-sales?pageno=2'
        #page 1
    r3 = requests.get(url3)
    data3 = r3.text
    soup3 = BeautifulSoup(data3, "lxml")
    table3 = soup3.find('div', id="quotes_content_left__panelTradeData")
    header3 = ['NLS Time (ET)','NLS Price','NLS Share Volume']
    body3 = [[td.text.strip() for td in row.select('td') if td.text.strip() != ' ']
                 for row in table3.findAll('tr')]
    body3 = [x for x in body3 if x != []]
    cols3 = zip(*body3)
    tbl_d3  = {name:col for name, col in zip(header3,cols3)}
    dft2 = ps.DataFrame(tbl_d3, columns = header3)
    dft = dft.append(dft2, ignore_index=True)
    x1 = ps.to_datetime(dft['NLS Time (ET)'])
    y1 = dft['NLS Price']
    
    plot.close()
    plot.clf()
    plot.subplot(1, 2, 1)
    plot.xticks(rotation=45)
    plot.plot(x1,y1)
    plot.subplot(1, 2, 2)
    plot.xticks(rotation=45)
    plot.plot(x, y)
    plot.tight_layout()
    
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
        # Remove old plot files
        for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # Use time since Jan 1, 1970 in filename in order make
    # a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plot.savefig(plotfile)
    return plotfile



def quotegrabber(symbol):
    x = symbol
    url = df2.loc[x,"Summary Quote"]
    return url

#Obtain current prices from stock market for trading menu options
def pricesnow(symbol):
    '''
    symbol passed in, only the prices is passed back
    '''
    url = quotegrabber(symbol)
    r = requests.get(url)
    data = r.text
    soup=BeautifulSoup(data, "lxml")
    money = soup.find('div', {'class' :'qwidget-dollar'}).text
    instantprice = float(Decimal(sub(r'[^\d.]', '', money)))
    #testing random * round(random.random()*100,2) 
    return instantprice


## buy function
def buy(table, symbol, shares):
    #call link and read page for current price
    '''
    table is from the ongoing ledger
    value is the value to call the ticker stock name
    shares are the number of shares in the transaction
    eq is the index of the equity list
    '''
    url = quotegrabber(symbol)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #this lets me capture the time
    r = requests.get(url)
    data = r.text
    soup=BeautifulSoup(data, "lxml")
    money = soup.find('div', {'class' :'qwidget-dollar'}).text
    instantprice = float(Decimal(sub(r'[^\d.]', '', money)))
    symb = symbol
    # Calculate cost of stock purchase and the WAP
    cost = instantprice * shares
    if table.empty == True:
        Bal = 10000000 - cost
    else:
        Bal = cashavail(table) - cost
    
    if table.empty == True:
        WAP = instantprice
    else:
        y = pl(table)
        if y[y.Ticker == symb].empty == True:
            WAP = instantprice
        else:
            y = y[y.Ticker == symb]
            WAP = float(ps.to_numeric(y.iloc[:,4]))
            #WAP = instantprice

    newentry = ['buy', symb, shares, instantprice, time, cost*-1, WAP, Bal] #list to store items related to trade
    return newentry

def sell(table, symbol, shares):
    #call link and read page for current price
    '''
    table is from the ongoing ledger
    value is the value to call the ticker stock name
    shares are the number of shares in the transaction
    eq is the index of the equity list
    '''
    url = quotegrabber(symbol)
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #this lets me capture the time
    r = requests.get(url)
    data = r.text
    soup=BeautifulSoup(data, "lxml")
    money = soup.find('div', {'class' :'qwidget-dollar'}).text
    instantprice = float(Decimal(sub(r'[^\d.]', '', money)))
    symb = symbol
    # Calculate cost of stock purchase and the WAP
    cost = instantprice * shares
    if table.empty == True:
        Bal = 10000000 + cost
    else:
        Bal = cashavail(table) + cost
    
    if table.empty == True:
        WAP = instantprice
    else:
        y = pl(table)
        if y[y.Ticker == symb].empty == True:
            WAP = instantprice
        else:
            y = y[y.Ticker == symb]
            WAP = float(ps.to_numeric(y.iloc[:,3]))
            #WAP = instantprice

    newentry = ['sell', symb, shares, instantprice, time, cost, WAP, Bal] #list to store items related to trade
    return newentry
# Check to see if we have stock to sell or cash
def cashavail(table):
    '''
    This function checks to see if there is cash to buy stock.
    The only item passed is in the ongoing ledger.
    
    '''
    cash = 10000000
    x = table
    #import ledger as dataframe and calculate if cash available to buy
    newcash = float(cash + sum(x.Cost))
    return newcash

def stockavail(table, symb):
    '''
    This function checks to see if there is stock to sell.
    The only item passed is in the ongoing ledger.
    
    '''
    #check to see if stock is available to sell
    x = table
    if x.empty == True:
        stocks = 0
    else:
        l = x[(x.Ticker == symb)]
        stocks = sum(l.Qty)
    return stocks


# insert to MongoDB
def insert(newentry):
    Side= newentry[0]
    Ticker = newentry[1]
    Qty = newentry[2]
    Price =float(newentry[3])
    Date = newentry[4]
    Cost = float(newentry[5])
    TWAP = float(newentry[6])
    Bal = newentry[7]
    
    k = db.blotter.count()
        
    myrecord = {
        "_id": k,
        "Bal": Bal,
        "Cost": Cost,
        "Date": Date,
        "Price": Price,
        "Qty": Qty,
        "Side": Side,
        "Ticker": Ticker,
        "TWAP": TWAP
        }
    record_id = db.blotter.insert_one(myrecord)
    return record_id


#the following set of code defines the blotter
def show_blotter(table):
    '''
    This item shows the blotter to the user.
    '''
    if table.empty == True:
        entries = 1
    else:
        entries = ps.DataFrame(list(db.blotter.find()))
        entries.drop(['_id'], axis = 1, inplace = True)
        entries.to_html(header=True)
    return entries



#the following set of code calculates the P/L

def pl(table):
    '''
    table is from the ongoing ledger
    '''
    x = table
    h = x.Ticker.unique().tolist()
    y = ps.DataFrame(ps.np.empty((len(h),9)), columns = ['Ticker','Position','Market','WAP','UPL','RPL','Total','AllocationShares', 'AllocationDollars'])
    y.Ticker = h
    for i in range(0,len(h)):
        symbol = h[i]
        instant = pricesnow(symbol)
        y['Market'][y.Ticker == symbol] = instant
    
    # Calculate items for WAP
    l = []
    r = []
    for i in range(0,len(h)):
        l = x[(x.Side == 'buy') & (x.Ticker == h[i])]
        r = x[(x.Ticker == h[i])]
        r.loc[r.Side == 'sell', 'Qty'] *= -1
        if sum(l.Qty) == 0:
            y.WAP[i] = 0
            y.Position[i] = sum(r.Qty)
        else:
            l.Cost = l.Qty * l.Price
            y.WAP[i] = sum(l.Cost)/sum(l.Qty)
            y.Position[i] = sum(r.Qty)
    
    # Calculate items for UPL
    for i in range(0,len(h)):
        if y.Position[i] > 0:
            if float((y.Market[i] - y.WAP[i])*y.Position[i])<0.01:
                y.UPL[i] = float((y.Market[i] - y.WAP[i])*y.Position[i]) #html would crash without this
            else:
                y.UPL[i] = float((y.Market[i] - y.WAP[i])*y.Position[i])
            #y.UPL[i] = format((y.Market[i] - y.WAP[i])*y.Position[i], '.2f')
        else:
            y.UPL[i] = 0
        
    #calculate items for RPL
    for i in range(0,len(h)):
        r = x[(x.Side == 'sell') & (x.Ticker == h[i])]
        if r.empty == False:
            r['Profit'] = r.Qty*(r.Price-r.TWAP)
            if sum(r.Qty) == 0:
                y.RPL[i] = format(0, '.2f')
            else:
                y.RPL[i] = format(sum(r.Profit), '.2f')
        else:
            y.RPL[i] = 0
    
    #calcualte total UPL + RPL
    y['Total'] = y['UPL'] + y['RPL']
    y['AllocationShares'] = y['Position'] /  y['Position'].sum()
    y['AllocationDollars'] = y['Market'] /  y['Market'].sum()
    y = y.fillna(0)
    
    return y