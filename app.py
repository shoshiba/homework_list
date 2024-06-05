import streamlit as st
from data_cloling import crawl_and_save_iidex_data
import pandas as pd

# Streamlitアプリの設定
st.title('IIDX DP Homework確認用ツール')

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

fetch_score_data = st.button('Fetch Score Data')
#fetch_rival1 = st.button('Fetch Rival1 Data')
#fetch_rival2 = st.button('Fetch Rival2 Data')
#fetch_rival3 = st.button('Fetch Rival3 Data')

if fetch_score_data:
    df_me = crawl_and_save_iidex_data(iidx_id_me)
    st.session_state['df_me'] = df_me
    st.subheader('自分のデータ')
    st.dataframe(df_me)
    df_rival1 = crawl_and_save_iidex_data(iidx_id_rival1)
    st.session_state['df_rival1'] = df_rival1
    st.subheader('ライバル1のデータ')
    st.dataframe(df_rival1)
    df_rival2 = crawl_and_save_iidex_data(iidx_id_rival2)
    st.session_state['df_rival2'] = df_rival2
    st.subheader('ライバル2のデータ')
    st.dataframe(df_rival2)
    df_rival3 = crawl_and_save_iidex_data(iidx_id_rival3)
    st.session_state['df_rival3'] = df_rival3
    st.subheader('ライバル3のデータ')

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

# 各曲の順位を計算
    def calculate_rank(row):
        scores = [row['Me'], row['Rival1'], row['Rival2'], row['Rival3']]
        return sorted(scores, reverse=True).index(row['Me']) + 1
    comparison['Rank'] = comparison.apply(calculate_rank, axis=1)

    comparison = comparison[['Level', 'Title','Rank', 'Me', 'Rival1', 'Rival2', 'Rival3', 'vsRival1', 'vsRival2', 'vsRival3']]
    st.subheader('ライバルスコアとの比較')
    # フィルタリングチェックボックス
    filter_checkbox = st.checkbox('全員が未プレイの曲を除外')

    st.write('レベル別フィルター')
    # レベルフィルタリングチェックボックス
    if 'df_me' in st.session_state:
        df_me = st.session_state['df_me']
        levels = sorted(df_me['Level'].unique(), key=lambda x: int(x.lstrip('☆')))
        selected_levels = []
        
        cols = st.columns(len(levels))
        for i, level in enumerate(levels):
            if cols[i].checkbox(level, value=True):
                selected_levels.append(level)
    else:
        selected_levels = []
    # レベルフィルタリングを適用
    comparison = comparison[comparison['Level'].isin(selected_levels)]
    if filter_checkbox:
        comparison = comparison[(comparison['Me'] != 0) | (comparison['Rival1'] != 0) | (comparison['Rival2'] != 0) | (comparison['Rival3'] != 0)]
    st.dataframe(comparison)


