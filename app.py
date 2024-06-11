import streamlit as st
import pandas as pd
from utils import fetch_data, create_comparison_dataframe
from validation import validate_inputs
from filters import apply_filters

# 定数の定義
DIFFICULTY_ORDER = ['NORMAL', 'HYPER', 'ANOTHER', 'LEGGENDARIA']

# タイトルの設定
st.title('IIDX DP Homework確認用ツール')

# 自分のIIDX ID入力
iidx_id_me = st.text_input('自分のIIDX IDを入れてください:', '')

# ライバルの人数選択
num_rivals = st.selectbox('ライバルの人数を選択してください:', [0, 1, 2, 3, 4])

# ライバルのIIDX ID入力
iidx_ids = {'me': iidx_id_me}
for i in range(1, num_rivals + 1):
    iidx_ids[f'rival{i}'] = st.text_input(f'比較したい人のIIDX IDを入れてください{i}:')

# エラーメッセージ表示用
errors = []

# 入力検証
if st.button('Fetch Score Data', key='fetch_data'):
    valid, errors = validate_inputs(iidx_id_me, iidx_ids, num_rivals)
    if valid:
        progress_bar = st.progress(0)
        dfs = {}
        for i, (key, iidx_id) in enumerate(iidx_ids.items(), start=1):
            if iidx_id:
                df = fetch_data(iidx_id)
                if df.empty:
                    errors.append(f'ID: {iidx_id} は存在しない可能性があります。')
                else:
                    dfs[key] = df
                    st.session_state[f'df_{key}'] = dfs[key]
            progress_bar.progress(i / len(iidx_ids))
        
        if errors:
            for error in errors:
                st.error(error)
            st.stop()
    else:
        for error in errors:
            st.error(error)

# データが存在する場合の処理
if 'df_me' in st.session_state:
    dfs = {key: st.session_state[f'df_{key}'] for key in iidx_ids.keys() if f'df_{key}' in st.session_state}
    if dfs:
        comparison = create_comparison_dataframe(dfs, num_rivals)

        # サイドバーにフィルターを移動
        comparison = apply_filters(comparison, dfs, num_rivals)

        st.subheader('ライバルスコアとの比較')

        # フィルタリングされたデータフレームを表示
        st.dataframe(comparison)
