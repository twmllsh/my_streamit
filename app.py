## 스트림
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta

st.set_page_config(
    page_icon="🍋",
    page_title = "과거 추천데이터 분석",
    layout='wide',
)

st.header("지수 현황")


## 데이터가져오기  ### 인덱스데이터 정기적인 데이터 업데이트 30 분.
data_path = "/home/sean/sean/data/"

index_data = pd.read_pickle(f"{data_path}index_df.pickle")
temp_df, df_normal = index_data



current_kospi_value = temp_df['KOSPI'] [temp_df['KOSPI'].notnull()].iloc[-1]
current_kospi_date = temp_df['KOSPI'] [temp_df['KOSPI'].notnull()].index[-1]
current_kospi_change = temp_df['KOSPI'] [temp_df['KOSPI'].notnull()].pct_change().iloc[-1]

current_kosdaq_value = temp_df['KOSDAQ'] [temp_df['KOSDAQ'].notnull()].iloc[-1]
current_kosdaq_date = temp_df['KOSDAQ'] [temp_df['KOSDAQ'].notnull()].index[-1]
current_kosdaq_change = temp_df['KOSDAQ'] [temp_df['KOSDAQ'].notnull()].pct_change().iloc[-1]

current_dji_value = temp_df['DJI'] [temp_df['DJI'].notnull()].iloc[-1]
current_dji_date = temp_df['DJI'] [temp_df['DJI'].notnull()].index[-1]
current_dji_change = temp_df['DJI'] [temp_df['DJI'].notnull()].pct_change().iloc[-1]

current_usdkrw_value = temp_df['USDKRW'] [temp_df['USDKRW'].notnull()].iloc[-1]
current_usdkrw_date = temp_df['USDKRW'] [temp_df['USDKRW'].notnull()].index[-1]
current_usdkrw_change = temp_df['USDKRW'] [temp_df['USDKRW'].notnull()].pct_change().iloc[-1]

current_vix_value = temp_df['VIX'] [temp_df['VIX'].notnull()].iloc[-1]
current_vix_date = temp_df['VIX'] [temp_df['VIX'].notnull()].index[-1]
current_vix_change = temp_df['VIX'] [temp_df['VIX'].notnull()].pct_change().iloc[-1]

current_ixic_value = temp_df['IXIC'] [temp_df['IXIC'].notnull()].iloc[-1]
current_ixic_date = temp_df['IXIC'] [temp_df['IXIC'].notnull()].index[-1]
current_ixic_change = temp_df['IXIC'] [temp_df['IXIC'].notnull()].pct_change().iloc[-1]



c_time = os.path.getctime(f"{data_path}index_df.pickle")
current_time = datetime.fromtimestamp(c_time).strftime('%Y-%m-%d %H:%M')

st.subheader(f"{current_time} 기준")

cols = st.columns( (1,1,2))
cols[0].metric("KOSPI",f"{current_kospi_value:,.1f}",f"{current_kospi_change*100:.2f}")
cols[0].metric("KOSDAQ",f"{current_kosdaq_value:,.1f}",f"{current_kosdaq_change*100:.2f}")
cols[0].metric('DJI',f"{current_dji_value:,.1f}",f"{current_dji_change*100:.2f}")

cols[1].metric('USD/KRW',f"{current_usdkrw_value:,.1f}",f"{current_usdkrw_change*100:.2f}")
cols[1].metric('VIX',f"{current_vix_value:,.1f}",f"{current_vix_change*100:.2f}")
cols[1].metric('IXIC',f"{current_ixic_value:,.1f}",f"{current_ixic_change*100:.2f}")

cols[2].line_chart(df_normal[["KOSPI","VIX","USDKRW"]][-240:])











fig = go.Figure()
fig.add_trace(go.Scatter(x=temp_df.index, y=temp_df['vix_line'],
                    mode='lines',
                    name='50'))
fig.add_trace(go.Scatter(x=temp_df.index, y=temp_df['VIX'],
                    mode='lines',
                    name='VIX'))

# 지수 
st.write(f"### VIX 지수")
st.plotly_chart(fig)


# 환율
fig = go.Figure()
fig.add_trace(go.Scatter(x=temp_df.index, y=temp_df['USDKRW'],
                    mode='lines',
                    name='USD/KRX',
                    line = dict(color='royalblue', width=4)))
fig.add_trace(go.Scatter(x=temp_df.index, y=temp_df['usdkrx_top'],
                    mode='lines',line_color='green'))
fig.add_trace(go.Scatter(x=temp_df.index, y=temp_df['usdkrx_bottom'],
                    mode='lines',line_color='green',
                    fill = "tonexty",opacity=0.5))
st.write(f"### 환율")
st.plotly_chart(fig)


# KOSPI지수  temp_df['KOSPI']
st.write(f"### KOSPI 지수")
st.line_chart(temp_df['KOSPI'].iloc[-150:])

# KOSDAQ지수 
st.write(f"### KOSDAQ 지수")
st.line_chart(temp_df['KOSDAQ'].iloc[-150:])

# 지수 상관관계
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_normal.index, y=df_normal['VIX'],
                    mode='lines',
                    name='VIX'))
fig.add_trace(go.Scatter(x=df_normal.index, y=df_normal['KOSPI'],
                    mode='lines',
                    name='KOSPI'))
fig.add_trace(go.Scatter(x=df_normal.index, y=df_normal['USDKRW'],
                    mode='lines',
                    name='USD/KRX'))
st.write(f"### 지수 상관관계")
st.plotly_chart(fig)

