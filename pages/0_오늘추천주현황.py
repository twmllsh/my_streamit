import pandas as pd
import streamlit as st
from pykrx import stock as pystock
import os
import sys
import requests
from datetime import datetime

# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

def get_ticker_by_fnguide():
    
    all_ls = []
    
        ## 레버리지, 인버스 추가. 
    dic = {"cd":["A122630","A252670"] , "nm" : ["KODEX 레버리지","KODEX 200선물인버스2X"],"gb":["ETF","ETF"]}
    # df = pd.DataFrame(dic).append(df).reset_index(drop=True)
    all_ls.append(pd.DataFrame(dic))
    
    for mkt_gb in [2,3]:
        url = f"http://comp.fnguide.com/SVO2/common/lookup_data.asp?mkt_gb={mkt_gb}&comp_gb=1"
        resp = requests.get(url)
        data = resp.json()
        all_ls.append(pd.DataFrame(data))
        # df = df.append(pd.DataFrame(data))
        # df = df[df['nm'].str.contains('스팩') == False] # 스팩 제외
    
    df = pd.concat(all_ls)
    df = df.reset_index(drop=True)
    df = df[df['nm'].str.contains('스팩') == False] # 스팩 제외
    
    ## 관리종목 거래정지종목 제외하기 
    try:
        url = "https://finance.naver.com/sise/trading_halt.naver" # 거래정지
        거래정지 = pd.read_html(url,encoding='cp949')[0].dropna()
        url = "https://finance.naver.com/sise/management.naver" #관리종목
        관리종목 = pd.read_html(url,encoding='cp949')[0].dropna()
        stop_ls = list(관리종목['종목명']) + list(거래정지['종목명']) # 관리종목 정지종목 리스트 
        print(f'총 {len(stop_ls)}개의 거래정지 관리종목을 제외')
        df =  df[~df['nm'].isin(stop_ls)]           ## 제외하기.
    except:
        pass
    
    df = df.reset_index(drop=True)
    return df


def get_all_current_price():
        
    date = datetime.today()
    str_today = date.strftime("%Y%m%d")
    
    df_all = pystock.get_market_ohlcv_by_ticker(str_today,market='ALL')

    df_all  = df_all.loc[df_all['시가']!=0]
    df_all['Date'] = date
    # df_all.index  = "A" + df_all.index
    df_all.rename(columns = {'시가' : 'Open',
                    '고가' : 'High',
                    '저가' : 'Low',
                    '종가' : 'Close',
                    '거래량' : 'Volume',
                    '거래대금' : 'Amount' ,
                    '등락률' : 'Change' }, inplace = True)
    df_all.index.name = 'Code'
    df_all  = df_all.reset_index()   ## 
    ##
    df_all['code'] = df_all['Code']  
    df_all = df_all.set_index('code',drop=True)
    return df_all

st.set_page_config(
    page_icon="🍋",
    page_title = "과거 추천데이터 분석",
    layout='wide',)


all_data = get_ticker_by_fnguide()[2:]
all_data.loc[:,'code'] = all_data['cd'].apply(lambda x :x[1:])
dic  = pd.read_pickle("../datas/temp_sended_dic.pkl")
date = dic['date'].strftime("%Y-%m-%d")
sended_codes_ls = dic['sended']
current_price_df = get_all_current_price()  ## 현재등락율 표시.
recommended_df = all_data[all_data['code'].isin(sended_codes_ls)]
result_df  = pd.merge(recommended_df,current_price_df,how="left",left_on="code",right_on='Code')
col = ['nm', 'Change','Volume','Close','gb', 'Open', 'High','Low','Amount','cd', ]
result_df = result_df[col]
result_df = result_df.sort_values('Change',ascending= False)

## 단위 지정.
result_df.loc[:,"Change"] = (result_df["Change"]).map("{:,.1f}".format)
result_df.loc[:,"Volume"] = (result_df["Volume"]).map("{:,.0f}".format)
result_df.loc[:,"Close"] = (result_df["Close"]).map("{:,.0f}".format)
추천주개수 = len(result_df)

st.write(f"### {date} 추천주 현황 ({추천주개수} 종목)")
result_df
