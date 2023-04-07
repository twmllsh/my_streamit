

import pandas as pd
import streamlit as st

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

import new_ms

st.set_page_config(
    page_icon="🍋",
    page_title = "과거 추천데이터 분석",
    layout='wide',)


all_data = new_ms.Fnguide.get_ticker_by_fnguide(option = 'db')[2:]
all_data.loc[:,'code'] = all_data['cd'].apply(lambda x :x[1:])
dic  = pd.read_pickle("/home/sean/sean/data/temp_sended_dic.pkl")
date = dic['date'].strftime("%Y-%m-%d")
sended_codes_ls = dic['sended']
current_price_df = new_ms.Sean_func.get_all_current_price()  ## 현재등락율 표시.
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