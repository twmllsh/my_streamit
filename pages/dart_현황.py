import pandas as pd
import streamlit as st
import sqlite3
import os
from datetime import datetime, timedelta
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import new_ms

st.set_page_config(
    page_icon="🍋",
    page_title = "과거 추천데이터 분석",
    layout='wide',)

today = datetime.today() - timedelta(days=1)
today = today.strftime('%Y%m%d')

#### 
data_path = '/home/sean/sean/dart/all_dart.db'
table_list = new_ms.Sean_func.get_table_list_from_db(data_path)[1:]


con = sqlite3.connect(data_path)
ls = []
for table_name in table_list:
    dic = {}
    sql = f'select * from "{table_name}" where rcept_dt > {today}'
    with con:
        data = pd.read_sql(sql,con)
        
        if table_name == '전환청구권행사':
            col = ['corp_name','청구일자','청구금액','전환가액','상장일 또는 예정일','url']
            
        elif table_name == '전환사채권발행결정':
            col = ['corp_name','시작일','종료일','전환금액(억)','전환가액','조달목적','표면이자율','만기이자율','시작일','종료일','url']
        elif table_name == '공급계약':
            col = ['corp_name','계약명', '계약금액(억)','매출액대비(%)','계약상대','판매공급지역','계약시작일', '계약종료일','계약일자','report_nm','url']
        elif table_name == '무상증자결정':
            col = ['corp_name', '주식수','주당신주배정주식수', '상장예정일', '배정기준일', '배당기산일','code','url']
        elif table_name == '소각결정':
            col = [ 'corp_name','소각주식수','소각율','소각예정금액_억','소각취득방법', '소각예정일','발행주식총수','code', 'url']
        elif table_name == '주식취득결정':
            col = ['corp_name','취득예정주식수','취득예정금액_억', '취득예상시작일', '취득예상종료일', '보유예상시작일','보유예상종료일', '취득목적', '취득방법', '취득결정일', 'code',  'url']
        else:
            col = data.columns
            
        dic[f"{table_name}"] = data[col]
        ls.append(dic)

if len(ls):
    for items in ls:
        for k,v in items.items():
            st.write(f"### {k} 현황")
            ### columns정리 필요 code_name , 계약금액_억 , 상대 , 기간.순. 
            try:
                if len(v):
                    st.dataframe(v)
                else:
                    st.write(f"#### -")
            except:
                st.write(f"#### col error")