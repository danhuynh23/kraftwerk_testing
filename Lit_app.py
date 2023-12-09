import pandas as pd
import requests
from sklearn.linear_model import LinearRegression
import streamlit as st


def FF5_alpha(ticker):
  data_url="https://raw.githubusercontent.com/danhuynh23/kraftwerk_testing/main/F-F_Research_Data_5_Factors_2x3_daily%20(1).CSV"
  api_key = '1822bea789msh219ec7e462e75a0p1d9a2cjsn7596777f7daf'
  fema_french_5=pd.read_csv(data_url)
  fema_french_5['Unnamed: 0']=pd.to_datetime(fema_french_5['Unnamed: 0'],format='%Y%m%d')
  fema_french_5.set_index(fema_french_5['Unnamed: 0'],inplace=True)

  base_url = 'https://www.alphavantage.co/query'

  req_gm = requests.get(
      base_url,
      params={
          "function": "TIME_SERIES_DAILY",
          "symbol": ticker,
          "apikey": api_key,
          "outputsize":"full"

      }
  )
  data_gm=req_gm.json()
  result_gm = pd.DataFrame.from_dict(data_gm['Time Series (Daily)'], orient= 'index')
  result_gm.index =  pd.to_datetime(result_gm.index, format='%Y-%m-%d')
  result_gm['4. close']=pd.to_numeric(result_gm['4. close'])
  result_gm=result_gm.iloc[::-1]
  result_gm['returns'] = (result_gm['4. close'] - result_gm['4. close'].shift(1))/result_gm['4. close'].shift(1)
  result_gm=result_gm.loc[(result_gm.index >= '2010-11-19')]
  fema_french_5=fema_french_5.loc[(fema_french_5.index>='2010-11-19')]
  FF5=fema_french_5
  FF5['GM']=result_gm['returns']
  FF5['excess_GM']=(FF5['GM']-FF5['RF'])
  y=FF5['excess_GM']
  X=FF5[['Mkt-RF','SMB','HML','RMW','CMA']]
  FF5_GM=LinearRegression()
  FF5_GM.fit(X,y)
  return str(FF5_GM.intercept_)

def main():
    
    st.title("Alpha Giver Web App")
    
    ticker=st.text_input("Please give your ticker ")
    result=""
    if st.button("Result"):
        result=FF5_alpha(ticker)
    st.success(result)

if __name__=='__main__':
    main()
    

