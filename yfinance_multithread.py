import pandas as pd
import yfinance as yf
from threading import Thread 
import time

tickers = ['AAPL', 'GOOGL', 'FB', 'TSLA', '']

col_a = []  # <-- list for all resulst
col_b = []  # <-- list for all resulst
col_c = []  # <-- list for all resulst
col_d = []  # <-- list for all resulst
print('Lodaing Data... Please wait for results')
for t in tickers:
    #print('---', t, '---')
    all_info = yf.Ticker(t).info

    a = all_info.get('ebitda', 'NaN')
    b = all_info.get('enterpriseValue', 'NaN')
    c = all_info.get('trailingPE', 'NaN')
    d = all_info.get('sector', 'NaN')
    col_a.append(a)  # <-- list for all resulst
    col_b.append(b)  # <-- list for all resulst
    col_c.append(c)  # <-- list for all resulst
    col_d.append(d)  # <-- list for all results

pd.set_option("display.max_rows", None)    
df = pd.DataFrame({
    'Tickets': tickers,
    'Ebitda': col_a,  # <-- list for all resulst
    'EnterpriseValue' :col_b,  # <-- list for all resulst
    'PE Ratio': col_c,  # <-- list for all resulst
    'Sector': col_d,
})
# df.to_excel('modified.xlsx', sheet_name='Sheet2', index=False)
print(df)


    
    

    


    
    










'''
ebitda
freeCashflow
earningsGrowth
totalCash

enterpriseValue
enterpriseToEbitda
lastFiscalYearEnd': 1609372800 #Last year enterprize value???? 
totalAssets
regularMarketPrice

trailingEps
'''

