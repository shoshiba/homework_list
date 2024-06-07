import streamlit as st
import pandas as pd
from utils import fetch_data, create_comparison_dataframe

st.title('IIDX DP Homework確認用ツール')

# IIDX ID入力
iidx_ids = {
    'me': st.text_input('自分のIIDX IDを入れてください:', '16548190'),
    'rival1': st.text_input('比較したい人のIIDX IDを入れてください1:', '55344136'),
    'rival2': st.text_input('比較したい人のIIDX IDを入れてください2:', '42936531'),
    'rival3': st.text_input('比較したい人のIIDX IDを入れてください3:', '48537824')
}

# スコアデータの取得
if st.button('Fetch Score Data'):
    dfs = {key: fetch_data(iidx_id) for key, iidx_id in iidx_ids.items()}
    for key, df in dfs.items():
        st.session_state[f'df_{key}'] = df

# 比較データの表示
if all(f'df_{key}' in st.session_state for key in iidx_ids.keys()):
    dfs = {key: st.session_state[f'df_{key}'] for key in iidx_ids.keys()}
    comparison = create_comparison_dataframe(dfs)

    # CSSスタイルを追加してチェックボックスを横一列に並べる
    st.markdown("""
        <style>
        .checkbox-container {
            display: flex;
            flex-wrap: wrap;
        }
        .checkbox-container > div {
            margin-right: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    # レベル別フィルター
    st.write('レベル別フィルター')
    levels = sorted(dfs['me']['Level'].unique(), key=lambda x: int(x.lstrip('☆')))
    difficulty_order = ['NORMAL', 'HYPER', 'ANOTHER', 'LEGGENDARIA']
    difficulties = sorted(comparison['Difficulty'].unique(), key=lambda x: difficulty_order.index(x))

    # 状態を保持するためのチェックボックスの初期値を設定
    if 'selected_levels' not in st.session_state:
        st.session_state.selected_levels = {level: True for level in levels}

    if 'selected_difficulty' not in st.session_state:
        st.session_state.selected_difficulty = {difficulty: True for difficulty in difficulties}

    def set_all_checkboxes_dif(value):
        """全てのチェックボックスを設定する"""
        st.session_state.selected_difficulty = {difficulty: value for difficulty in difficulties}

    def set_all_checkboxes(value):
        """全てのチェックボックスを設定する"""
        st.session_state.selected_levels = {level: value for level in levels}

    # ボタンの追加
    if st.button('全部チェックを入れる'):
        set_all_checkboxes(True)
    if st.button('全部チェックを外す'):
        set_all_checkboxes(False)

    # チェックボックスの表示（横一列）
    selected_levels = []
    checkboxes = st.container()
    with checkboxes:
        with st.container():
            st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)
            st.columns(len(levels))
            for level in levels:
                if st.checkbox(level, value=st.session_state.selected_levels[level], key=f'level_{level}'):
                    selected_levels.append(level)
            st.markdown('</div>', unsafe_allow_html=True)

    # フィルタリング適用
    comparison = comparison[comparison['Level'].isin(selected_levels)]

    # 譜面難易度別フィルター
    st.write('譜面難易度別フィルター')

    # ボタンの追加
    if st.button('全部チェックを入れる2'):
        set_all_checkboxes_dif(True)
    if st.button('全部チェックを外す2'):
        set_all_checkboxes_dif(False)

    # チェックボックスの表示（横一列）
    selected_difficulties = []
    checkboxes = st.container()
    with checkboxes:
        cols = st.columns(len(difficulties))
        for col, difficulty in zip(cols, difficulties):
            if col.checkbox(difficulty, value=st.session_state.selected_difficulty[difficulty], key=difficulty):
                selected_difficulties.append(difficulty)

    # フィルタリング適用
    comparison = comparison[comparison['Difficulty'].isin(selected_difficulties)]

    # 未プレイ曲に関する除外
    st.write('未プレイフィルター')
    if st.checkbox('全員が未プレイの曲を除外'):
        comparison = comparison[(comparison['Me'] != 0) | (comparison['Rival1'] != 0) | (comparison['Rival2'] != 0) | (comparison['Rival3'] != 0)]
    if st.checkbox('自分が未プレイの曲を除外'):
        comparison = comparison[(comparison['Me'] != 0)]

    st.subheader('ライバルスコアとの比較')

    # フィルタリングされたデータフレームを表示
    st.dataframe(comparison)
