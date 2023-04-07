import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def 등급(등락율):
    result = ""
    if 0 <= 등락율 <4:
        result = "0:4%"
    elif 4 <= 등락율 < 8:
        result = "4:8%"
    elif 8 <= 등락율 < 15:
        result = "8:15%"
    elif 15 <= 등락율 < 25:
        result = "15:25%"
    elif 25 <= 등락율 <= 31:
        result = "25:30%" 
    elif -4 <= 등락율 < 0:
        result = "-4:0%"  
    elif -10 <= 등락율 < -4:
        result = "-4:-10%" 
    elif -20 <= 등락율 < -10:
        result = "-10:-20%"
    elif -31 <= 등락율 < -20:
        result = "-20:-30%"
    else:
        result = "?"
    return result

st.set_page_config(
    page_icon="🍋",
    page_title = "과거 추천데이터 분석",
    layout='wide',)

data_path = "/home/sean/sean/data/"
try:
    check_df = pd.read_pickle(f"{data_path}recommended_df1.pickle")
except:
    check_df = pd.DataFrame()

if len(check_df)==0:
    st.write(f"### 추천종목데이터가 없음")
    
# 매수일 
buy_date = check_df['추천일'].iloc[-1]
buy_date= buy_date.strftime("%Y-%m-%d")
st.write(f"### 추천일 : {buy_date}")

current_date = check_df['현재날짜'].iloc[-1]
current_date = current_date.strftime("%Y-%m-%d")
st.write(f"### 현재일 : {current_date}")

소요일수  = check_df['소요일수'].iloc[-1]
st.write(f"### 추천주 {소요일수}일간 수익율 분석")


## 전체추천종목 현황
st.write(f"### 전체추천종목 현황")
temp_df = check_df[['code', 'code_name', '현재수익율','최고수익율', '최저수익율','추천기법','추천일등락율', '당시point', '추천일', '현재날짜',
        ]].sort_values('현재수익율',ascending = False)
temp_df.reset_index(drop=True)
temp_df



# coke 돌파 종목 수익율.  
word = '코크돌파'
st.write(f"### coke 돌파 종목 수익율 현황")

temp_df = check_df[(check_df['매수사유'].str.contains(f'{word}'))]
if len(temp_df):
    temp_df['cnt']= temp_df['매수사유'].apply( lambda x :len([item for item in x.split("|") if f"{word}" in item ]))
    temp_df = temp_df[temp_df['cnt'] >1]    ## 코크돌파 키워드가 2개이상만 취급. 
    if len(temp_df):
        temp_df
if len(temp_df)==0 :
    st.write(f"------")
        


## 추천당일 등락율별 상승율
st.write(f"### 추천당일 등락율별 수익율 분석")
check_df['당일등락율등급'] = check_df['추천일등락율'].apply(lambda x :등급(x))
temp_df = check_df.groupby('당일등락율등급').mean()[["최고수익율","최저수익율","현재수익율"]].sort_values('최고수익율',ascending = False)
temp_df
st.bar_chart(temp_df)


## 추천기법별 최고현재수익율
st.write(f"### 추천기법별 최고현재수익율")
fig = px.scatter(check_df, x = '현재수익율', y='최고수익율',color='추천기법',hover_name='code_name')
st.plotly_chart(fig)


## 최고최저현재수익율 분포도.
st.write(f"### 수익율 분포도")
view = check_df[["최고수익율","최저수익율","현재수익율"]]
st.bar_chart(view)


# 추천기법에 따른 평균수익율.
view1 = check_df.groupby('추천기법').mean()[['최고수익율','최저수익율']]
st.write('### 추천기법에 따른 평균수익율')
view1

# 통계요약
st.write("### 통계요약")
temp_df = check_df.describe().loc[['mean','std','min','max'],["당시point","최고수익율","최저수익율","현재수익율"]]
temp_df

## 상승 하락 개수 
st.write("### 추천종목중 상승 하락")
temp_df = check_df['현재수익율'].apply(lambda x : "상승" if x > 0 else '하락').value_counts().to_frame()
temp_df.columns = ['count']
st.bar_chart(temp_df)


## 추천종목평균수익율
current_value = check_df['현재수익율'].mean()
high_value = check_df['최고수익율'].mean()
st.write(f"### 평균현재수익율{current_value:,.1f}%")
st.write(f"### 평균최고수익율{high_value:,.1f}%")

## 최고 10프로이상 상승종목의 기법 count
temp_df = check_df[check_df['최고수익율'] >=10].value_counts(['추천기법']).to_frame()
temp_df.columns=['cnt']
st.write(f"### 최고 10%이상 상승종목의 기법들")
temp_df


## 현재 10프로이상 상승종목의 기법 count
temp_df = check_df[check_df['현재수익율'] >=10].value_counts(['추천기법']).to_frame()
temp_df.columns=['cnt']
st.write(f"### 현재 10%이상 상승종목의 기법들")
temp_df

## 현재 플러스 종목의 기법 count
temp_df = check_df[check_df['현재수익율'] >0].value_counts(['추천기법']).to_frame()
temp_df.columns=['cnt']
st.write(f"### 현재 상승종목의 기법들")
temp_df

## 현재 마이너스 종목의 기법 count
temp_df = check_df[check_df['현재수익율'] < 0].value_counts(['추천기법']).to_frame()
temp_df.columns=['cnt']
st.write(f"### 현재 하락종목의 기법들")
temp_df


## 현재수익율과 매수사유갯수와의 상관관계
value = check_df[['매수사유갯수','현재수익율']].corr().iloc[0,1]
st.write(f"### 현재수익율과 매수사유갯수 상관관계: {value *100 :,.1f}")

## 현재수익율과 당시point와의 상관관계
value = check_df[['당시point','현재수익율']].corr().iloc[0,1]
st.write(f"### 현재수익율과 당시point 상관관계: {value *100 :,.1f}")

## 추천기법에 따른 수익율 평균
temp_df = check_df.groupby('추천기법').mean()[['현재수익율','최고수익율','최저수익율']]
temp_df = temp_df.sort_values('최고수익율',ascending = False)
st.write(f"### 추천기법에 따른 수익율 평균")
temp_df

# 추천기법에 따른 최고수익율
temp_df = check_df.groupby('추천기법').max()[['현재수익율','최고수익율','최저수익율']]
temp_df = temp_df.sort_values('최고수익율',ascending = False)
st.write(f"### 추천기법에 따른 최고수익율")
temp_df
