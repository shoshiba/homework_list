import streamlit as st
import pandas as pd
import re
from data_cloling import crawl_and_save_iidex_data

# Streamlitアプリの設定
st.title('IIDX DP Homework確認用ツール')

# IIDX ID入力
iidx_ids = {
    'me': st.text_input('自分のIIDX IDを入れてください:', '16548190'),
    'rival1': st.text_input('比較したい人のIIDX IDを入れてください1:', '55344136'),
    'rival2': st.text_input('比較したい人のIIDX IDを入れてください2:', '42936531'),
    'rival3': st.text_input('比較したい人のIIDX IDを入れてください3:', '48537824')
}

def fetch_data(iidx_id):
    """指定されたIIDX IDのデータを取得する"""
    return crawl_and_save_iidex_data(iidx_id)

def extract_percentage(performance):
    """Performanceからパーセンテージを抽出"""
    match = re.search(r'(\d+\.\d+%)', performance)
    return match.group(1) if match else '0.0%'

def calculate_rank(row):
    """スコアに基づいて順位を計算する"""
    scores = [row['Me'], row['Rival1'], row['Rival2'], row['Rival3']]
    return sorted(scores, reverse=True).index(row['Me']) + 1

def create_comparison_dataframe(dfs):
    """比較用のデータフレームを作成する"""
    comparison = pd.DataFrame({
        'Level': dfs['me']['Level'],
        'Title': dfs['me']['Title'],
        'Me': dfs['me']['Details_Number'],
        'MePer': dfs['me']['Performance'],
        'Rival1': dfs['rival1']['Details_Number'],
        'Rival2': dfs['rival2']['Details_Number'],
        'Rival3': dfs['rival3']['Details_Number'],
        'vsRival1': dfs['me']['Details_Number'] - dfs['rival1']['Details_Number'],
        'vsRival2': dfs['me']['Details_Number'] - dfs['rival2']['Details_Number'],
        'vsRival3': dfs['me']['Details_Number'] - dfs['rival3']['Details_Number'],
    }).fillna(0)
    comparison['Rank'] = comparison.apply(calculate_rank, axis=1)
    comparison['Me_Per'] = comparison['MePer'].apply(extract_percentage)
    return comparison[['Level', 'Title', 'Rank', 'Me', 'Me_Per', 'Rival1', 'Rival2', 'Rival3', 'vsRival1', 'vsRival2', 'vsRival3']]

# スコアデータの取得
if st.button('Fetch Score Data'):
    dfs = {key: fetch_data(iidx_id) for key, iidx_id in iidx_ids.items()}
    for key, df in dfs.items():
        st.session_state[f'df_{key}'] = df

# 比較データの表示
if all(f'df_{key}' in st.session_state for key in iidx_ids.keys()):
    dfs = {key: st.session_state[f'df_{key}'] for key in iidx_ids.keys()}
    comparison = create_comparison_dataframe(dfs)

    # レベル別フィルター
    st.write('レベル別フィルター')
    levels = sorted(dfs['me']['Level'].unique(), key=lambda x: int(x.lstrip('☆')))
    selected_levels = [level for level in levels if st.checkbox(level, value=True)]

    # フィルタリング適用
    comparison = comparison[comparison['Level'].isin(selected_levels)]
    if st.checkbox('全員が未プレイの曲を除外'):
        comparison = comparison[(comparison['Me'] != 0) | (comparison['Rival1'] != 0) | (comparison['Rival2'] != 0) | (comparison['Rival3'] != 0)]
    
    st.subheader('ライバルスコアとの比較')
    st.dataframe(comparison)
