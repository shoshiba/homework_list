import streamlit as st
from data_cloling import crawl_and_save_iidex_data
import pandas as pd

# Streamlitアプリの設定
st.title('IIDX Player Data')

#iidx_id_me = st.text_input('自分のIIDX IDを入れてください:', '16548190')
#
#if st.button('Fetch Data',key='fetch_data_me'):
#    df_me = crawl_and_save_iidex_data(iidx_id_me)
#    st.dataframe(df_me)
#
#iidx_id_rival = st.text_input('比較したい人のIIDX IDを入れてください:', '55344136')
#
#if st.button('Fetch Data',key='fetch_data_rival'):
#    df_rival = crawl_and_save_iidex_data(iidx_id_rival)
#    st.dataframe(df_rival)



iidx_id_me = st.text_input('自分のIIDX IDを入れてください:', '16548190')
iidx_id_rival1 = st.text_input('比較したい人のIIDX IDを入れてください1:', '55344136')
iidx_id_rival2 = st.text_input('比較したい人のIIDX IDを入れてください2:', '42936531')
iidx_id_rival3 = st.text_input('比較したい人のIIDX IDを入れてください3:', '48537824')

fetch_me = st.button('Fetch My Data')
fetch_rival1 = st.button('Fetch Rival1 Data')
fetch_rival2 = st.button('Fetch Rival2 Data')
fetch_rival3 = st.button('Fetch Rival3 Data')

if fetch_me:
    df_me = crawl_and_save_iidex_data(iidx_id_me)
    st.session_state['df_me'] = df_me
    st.subheader('自分のデータ')
    st.dataframe(df_me)

if fetch_rival1:
    df_rival1 = crawl_and_save_iidex_data(iidx_id_rival1)
    st.session_state['df_rival1'] = df_rival1
    st.subheader('ライバルのデータ')
    st.dataframe(df_rival1)

if fetch_rival2:
    df_rival2 = crawl_and_save_iidex_data(iidx_id_rival2)
    st.session_state['df_rival2'] = df_rival2
    st.subheader('ライバルのデータ')
    st.dataframe(df_rival2)
if fetch_rival3:
    df_rival3 = crawl_and_save_iidex_data(iidx_id_rival3)
    st.session_state['df_rival3'] = df_rival3
    st.subheader('ライバルのデータ')
    st.dataframe(df_rival3)

# 比較データの表示
if 'df_me' in st.session_state and 'df_rival1' in st.session_state:
    df_me = st.session_state['df_me']
    df_rival1 = st.session_state['df_rival1']
    df_rival2 = st.session_state['df_rival2']
    df_rival3 = st.session_state['df_rival3']
    
    comparison = pd.DataFrame({
        'Level': df_me['Level'],
        'Title': df_me['Title'],
        'Me': df_me['Details_Number'],
        'Rival1': df_rival1['Details_Number'],
        'Rival2': df_rival2['Details_Number'],
        'Rival3': df_rival3['Details_Number'],
        'vsRival1': df_me['Details_Number'] - df_rival1['Details_Number'],
        'vsRival2': df_me['Details_Number'] - df_rival2['Details_Number'],
        'vsRival3': df_me['Details_Number'] - df_rival3['Details_Number'],
    }).fillna(0)  # データの数が一致しない場合は0で埋める

    st.subheader('Details_Numberの比較')
    st.dataframe(comparison)
