import pandas as pd
import yfinance as yf
import numpy as np
import concurrent.futures
import time
from stocks import tickers
start = time.time()

# NOTES for NEXT TIME 

# Should cost of equity and debt be for an aquisition or for the company value?

# Need to create a five year and 10 year FV function. Also get Terminal Value and Value per share. 
# Also add IRR FUNCTION and Return Function for 7 Years.
# Add Carhart 4 Factor model since many companies value is derived from momentum. MOM
# Add Loading Screen


# Calucaltion Varibles for different formulas
 
inf = 0.0620 # The Current Inflation Rate
rr = 0.10 # S&P Historical Return
ap = 0.06 # Aquisition Premium. What the holding company offers to investors for an aquisition. The premium on having the company as an asset. 
gdp = 0.028 # Real GDP not Nominal
# Capitol Asset Pricing Model
equity = 0.70
debt = 0.30
cost_debt = 0.04 # Intrest Paid on the debt 
cost_equity = ('capm') # Cost of equity is the CAPM
tax = (1 - 0.28)

# Capitol Asset Pricing Model (CAPM)
Expected_Return = 0.20
rfr = 0.02 # It is equal to the 10 year Treasury
Beta = 1.1
erm = 0.23 # Expected Market Return aka unknown return of the market
 
# tv is the Terminal value. 


# Dictionary 
col_a = []  
col_b = []
col_b2 = []  
col_c = []  
col_e = []
col_ez = []
col_g = []
col_capm = []
col_wacc = []
col_pv = []
col_tv = []
col_nfv = []
col_roi = []

# Based on a % 70 Equity Transaciton
print('Loading Results...')
def do_something(tickers):
    #print('---', tickers, '---')
    all_info = yf.Ticker(tickers).info
    try:
        a = all_info.get('ebitda')
        b = all_info.get('freeCashflow') 
        b2 = all_info.get('beta') 
        c = all_info.get('enterpriseValue')      
        e = all_info.get('sector')
        ez = (c*equity)  
        g = (c/a)
        capm = ((rfr + b2)*(0.10 - rfr))
        wacc = ( (equity*capm) + (debt*cost_debt)*(1-tax) )

        # should be FV b*(1+rfr)**7 / 
        pv = ( (b*capm + b) / (1 + wacc)**1   +   (b*capm + b)/(1 + wacc)**2  +   (b*capm + b)/(1 + wacc)**3   +   (b*capm + b)/(1 + wacc)**4    +    (b*capm + b)/(1 + wacc)**5  +  (b*capm + b)/(1 + wacc)**6  +  (b*capm + b)/(1 + wacc)**7 )  
        tv = ( pv + c*(1+gdp)**7  ) # Need to have a monte carlo model of possiblilities of returns such as capm, gdp, rfr and other return rates. 
        nfv = (pv + tv - ez)
        roi = (nfv/c*equity) # Need to calculate IRR
        
    except:
        return None, None, None, None, None, None, None, None, None, None, None, None, None  # must return as many tuples as your are calculating
    return a, b, b2, c, e, ez, g, capm, wacc, pv, tv, nfv, roi

with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executer:
    for a, b, b2, c, e, ez, g, capm, wacc, pv, tv, nfv, roi in executer.map(do_something, tickers):
        col_a.append(a)  
        col_b.append(b)
        col_b2.append(b2)
        col_c.append(c)  
        col_e.append(e)
        col_ez.append(ez)  
        col_g.append(g)
        col_capm.append(capm) 
        col_wacc.append(wacc)
        col_pv.append(pv)
        col_tv.append(tv)
        col_nfv.append(nfv)
        col_roi.append(roi)

# Dataframe Set Up
df = pd.DataFrame({
    'Ticker': tickers,
    'Ebitda': col_a,  
    'FCF' :col_b,
    'Beta' :col_b2,  
    'EV': col_c,  
    'Sector': col_e,
    'EV Ratio': col_g,
    'CAPM': col_capm,
    'WACC': col_wacc,
    'DCF FCF': col_pv,
    'TV': col_tv,
    'Cash Return': col_nfv,
    'ROI': col_roi
 
})
pd.set_option("display.max_rows", None)
df.dropna(inplace=True)
filter_criteria = df[ (df['Sector'] == 'Technology') & (df['EV'] <=5000000000) & (df['FCF'] >=100000) & (df['Ebitda'] >=100000) & (df['DCF FCF'] >=0) ]
filter_criteria.to_excel('modified.xlsx', sheet_name='Sheet2', index=False)
print(filter_criteria)
print('It took', time.time()-start, 'seconds.')