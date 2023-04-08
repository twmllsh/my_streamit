import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import pickle


st.set_page_config(
    page_icon="🍋",
    page_title = "과거 추천데이터 분석",
    layout='wide',)

data_path = './datas/'
filename0 = data_path + "invest_tops_for_0day.pickle"
filename4 = data_path + "invest_tops_for_4day.pickle"
filename7 = data_path + "invest_tops_for_7day.pickle"
filename15 = data_path + "invest_tops_for_15day.pickle"

data0 = pd.read_pickle(filename0)
data4 = pd.read_pickle(filename4)
data7 = pd.read_pickle(filename7)
data15 = pd.read_pickle(filename15)

p_data0 = data0.index.name
p_data4 = data4.index.name
p_data7 = data7.index.name
p_data15 = data15.index.name

data0 = data0.set_index('rank').reset_index(drop=True)
data4 = data4.set_index('rank').reset_index(drop=True)
data7 = data7.set_index('rank').reset_index(drop=True)
data15 = data15.set_index('rank').reset_index(drop=True)



data0.loc[:,'순매수/시총'] = (data0['순매수금/시가총액']/100).map("{:,.2%}".format)
data0.loc[:,"순매수대금_억"] = (data0["순매수거래대금_억"]).map("{:,.0f}".format)
data0.loc[:,"시가총액_억"] = (data0["시가총액_억"]).map("{:,.0f}".format)
data0.loc[:,"순매수거래량"] = (data0["순매수거래량"]).map("{:,.0f}".format)

data4.loc[:,'순매수/시총'] = (data4['순매수금/시가총액']/100).map("{:,.2%}".format)
data4.loc[:,"순매수대금_억"] = (data4["순매수거래대금_억"]).map("{:,.0f}".format)
data4.loc[:,"시가총액_억"] = (data4["시가총액_억"]).map("{:,.0f}".format)
data4.loc[:,"순매수거래량"] = (data4["순매수거래량"]).map("{:,.0f}".format)

data7.loc[:,'순매수/시총'] = (data7['순매수금/시가총액']/100).map("{:,.2%}".format)
data7.loc[:,"순매수대금_억"] = (data7["순매수거래대금_억"]).map("{:,.0f}".format)
data7.loc[:,"시가총액_억"] = (data7["시가총액_억"]).map("{:,.0f}".format)
data7.loc[:,"순매수거래량"] = (data7["순매수거래량"]).map("{:,.0f}".format)

data15.loc[:,'순매수/시총'] = (data15['순매수금/시가총액']/100).map("{:,.2%}".format)
data15.loc[:,"순매수대금_억"] = (data15["순매수거래대금_억"]).map("{:,.0f}".format)
data15.loc[:,"시가총액_억"] = (data15["시가총액_억"]).map("{:,.0f}".format)
data15.loc[:,"순매수거래량"] = (data15["순매수거래량"]).map("{:,.0f}".format)



col = ["종목명","순매수/시총","현재등락율","순매수대금_억","순매수거래량","시가총액_억"]

#### express
st.write(f"### 기간 : {p_data0}")
st.write("### 1일간 시가총액대비 기관외인 매수비율")
data0[col]

st.write(f"### 기간 : {p_data4}")
st.write("### 4일간 시가총액대비 기관외인 매수비율")
data4[col]

st.write(f"### 기간 : {p_data7}")
st.write("### 7일간 시가총액대비 기관외인 매수비율")
data7[col]

st.write(f"### 기간 : {p_data15}")
st.write("### 15일간 시가총액대비 기관외인 매수비율")
data15[col]
