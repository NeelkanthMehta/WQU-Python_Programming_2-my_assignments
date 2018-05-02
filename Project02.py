#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  2 14:38:25 2018

@author: neelkanth
"""
# Importing Important Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import quandl as ql
import mpl_finance as mpl
import fix_yahoo_finance as yahoo

# Setting the Start date
startdate = dt.date(2008,4,1)
enddate = dt.date(2018,3,31)

ql.ApiConfig.api_key = '34VkeK5bFLvtaEprKmFX'

# Downloading the data from quandl
#tickers = ['NSE/NIFTY_50.4','BCIW/_HSCE.4','BCIW/_SPXT.4','WFE/INDEXES_LONDONSEFTSE','NIKKEI/INDEX.4']
NIFTY50 = ql.get("NSE/NIFTY_50.4", authtoken="34VkeK5bFLvtaEprKmFX", start_date=startdate, end_date=enddate)
type(NIFTY50)
NIFTY50 = NIFTY50.ffill()

# Fetching Hang Seng data
HANGSENG= ql.get("BCIW/_HSCE.4", authtoken="34VkeK5bFLvtaEprKmFX", start_date = startdate, end_date=enddate)
HSI = yahoo.download('^HSI',start=startdate, end=enddate)
HSI['Adj Close'].head()

# Fetching NIKKEI stock price data
NIKKEI  = ql.get("NIKKEI/INDEX.4", authtoken="34VkeK5bFLvtaEprKmFX", start_date=startdate,end_date=enddate)

# Fetching FTSE data
#FTSE100 = ql.get("WFE/INDEXES_LONDONSEFTSE", authtoken="34VkeK5bFLvtaEprKmFX", start_date=startdate, end_date= enddate)
FTSE100 = yahoo.download('^FTSE',start=startdate, end=enddate)
FTSE100.ix[1:,['Adj Close']].head()
type(FTSE100)

# Fetching S&P 500 data
SP = ql.get("BCIW/_SPXT.4", authtoken="34VkeK5bFLvtaEprKmFX", start_date = startdate, end_date=enddate)
GSPC = yahoo.download('^GSPC',start=startdate, end=enddate)
GSPC.ix[1:,['Adj Close']].head()

# Concatnating 
Indices = pd.concat((NIFTY50,HSI['Adj Close'],NIKKEI,FTSE100.ix[1:,['Adj Close']],GSPC.ix[1:,['Adj Close']]),join='outer',axis=1)
Indices.columns = ['NIFTY50','HANGSENG','NIKKEI','FTSE100','S&P500']
Indices.tail(50)
Indices.fillna(method='ffill', axis=1, inplace=True)
Indices = Indices.ffill(axis=1)
#len(Indices[Indices['NIFTY50'].isna()]['NIFTY50'])

# COmputing correnation coefficients
CorrcMat = Indices.corr(method='pearson')

# Importing Seaborn library - a better library compared to matplotlib
import seaborn as sns

sns.heatmap(CorrcMat,annot=True) # Annotated Heatmap

# Plotting the Indices
dataframe = Indices/ Indices.iloc[0] # Standardizing the indices to make'em comparable
dataframe.head() # Inspecting first few elements

# PLot
plt.plot(dataframe)
plt.xticks(rotation=90)
plt.legend(loc=0)
plt.show()

"""Another approach to design correlation matrix"""
Scatter = pd.scatter_matrix(dataframe)