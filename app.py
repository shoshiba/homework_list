import streamlit as st
import pandas as pd
from utils import fetch_data, create_comparison_dataframe

# 定数の定義
DIFFICULTY_ORDER = ['NORMAL', 'HYPER', 'ANOTHER', 'LEGGENDARIA']

# タイトルの設定
st.title('IIDX DP Homework確認用ツール')

def is_valid_iidx_id(iidx_id):
    return iidx_id.isdigit() and len(iidx_id) == 8

# 自分のIIDX ID入力
iidx_id_me = st.text_input('自分のIIDX IDを入れてください:', '')

# ライバルの人数選択
num_rivals = st.selectbox('ライバルの人数を選択してください:', [1, 2, 3, 4])

# ライバルのIIDX ID入力
iidx_ids = {'me': iidx_id_me}
for i in range(1, num_rivals + 1):
    iidx_ids[f'rival{i}'] = st.text_input(f'比較したい人のIIDX IDを入れてください{i}:')

# エラーメッセージ表示用
errors = []


# 入力検証
if st.button('Fetch Score Data', key='fetch_data'):
    valid = True
    if not is_valid_iidx_id(iidx_id_me):
        errors.append('自分のIIDX IDは8桁の数字でなければなりません。')
        valid = False
    
    for i in range(1, num_rivals + 1):
        if not is_valid_iidx_id(iidx_ids[f'rival{i}']):
            errors.append(f'比較したい人のIIDX ID {i} は8桁の数字でなければなりません。')
            valid = False

    if valid:
        progress_bar = st.progress(0)
        dfs = {}
        for i, (key, iidx_id) in enumerate(iidx_ids.items(), start=1):
            if iidx_id:
                dfs[key] = fetch_data(iidx_id)
                st.session_state[f'df_{key}'] = dfs[key]
            progress_bar.progress(i / len(iidx_ids))
    else:
        for error in errors:
            st.error(error)

# データが存在する場合の処理
if all(f'df_{key}' in st.session_state for key in iidx_ids.keys()):
    dfs = {key: st.session_state[f'df_{key}'] for key in iidx_ids.keys()}
    comparison = create_comparison_dataframe(dfs, num_rivals)

    # CSSスタイルの追加
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

    # レベル別フィルターの初期化
    st.write('レベル別フィルター')
    levels = sorted(dfs['me']['Level'].unique(), key=lambda x: int(x.lstrip('☆')))
    if 'selected_levels' not in st.session_state:
        st.session_state.selected_levels = {level: True for level in levels}

    # 譜面難易度別フィルターの初期化
    difficulties = sorted(comparison['Difficulty'].unique(), key=lambda x: DIFFICULTY_ORDER.index(x))
    if 'selected_difficulty' not in st.session_state:
        st.session_state.selected_difficulty = {difficulty: True for difficulty in difficulties}

    # 順位別フィルターの初期化
    ranks = sorted(comparison['Rank'].unique())
    if 'selected_rank' not in st.session_state:
        st.session_state.selected_rank = {str(rank): True for rank in ranks}

    # 全チェック/全解除関数の定義
    def set_all_checkboxes(key, items, value):
        st.session_state[key] = {item: value for item in items}

    # ボタンの追加
    if st.button('全部チェックを入れる'):
        set_all_checkboxes('selected_levels', levels, True)
    if st.button('全部チェックを外す'):
        set_all_checkboxes('selected_levels', levels, False)

    # チェックボックスの表示（横一列）
    selected_levels = []
    with st.container():
        st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)
        for level in levels:
            if st.checkbox(level, value=st.session_state.selected_levels[level], key=f'level_{level}'):
                selected_levels.append(level)
        st.markdown('</div>', unsafe_allow_html=True)

    # フィルタリング適用
    comparison = comparison[comparison['Level'].isin(selected_levels)]

    # 譜面難易度別フィルター
    st.write('譜面難易度別フィルター')
    if st.button('全部チェックを入れる2'):
        set_all_checkboxes('selected_difficulty', difficulties, True)
    if st.button('全部チェックを外す2'):
        set_all_checkboxes('selected_difficulty', difficulties, False)

    # チェックボックスの表示（横一列）
    selected_difficulties = []
    with st.container():
        st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)
        for difficulty in difficulties:
            if st.checkbox(difficulty, value=st.session_state.selected_difficulty[difficulty], key=difficulty):
                selected_difficulties.append(difficulty)
        st.markdown('</div>', unsafe_allow_html=True)

    # フィルタリング適用
    comparison = comparison[comparison['Difficulty'].isin(selected_difficulties)]

    # 順位別フィルター
    st.write('順位別フィルター')
    if st.button('全部チェックを入れる3'):
        set_all_checkboxes('selected_rank', ranks, True)
    if st.button('全部チェックを外す3'):
        set_all_checkboxes('selected_rank', ranks, False)

    # チェックボックスの表示（横一列）
    selected_ranks = []
    with st.container():
        st.markdown('<div class="checkbox-container">', unsafe_allow_html=True)
        for rank in ranks:
            rank_str = str(rank)
            if rank_str not in st.session_state.selected_rank:
                st.session_state.selected_rank[rank_str] = True
            if st.checkbox(rank_str, value=st.session_state.selected_rank[rank_str], key=rank_str):
                selected_ranks.append(rank)
        st.markdown('</div>', unsafe_allow_html=True)

    # フィルタリング適用
    comparison = comparison[comparison['Rank'].isin(selected_ranks)]

    # 未プレイ曲に関する除外
    st.write('未プレイフィルター')
    if st.checkbox('全員が未プレイの曲を除外'):
        condition = (comparison['Me'] != 0)
        for i in range(1, num_rivals + 1):
            condition |= (comparison[f'Rival{i}'] != 0)
        comparison = comparison[condition]
    if st.checkbox('自分が未プレイの曲を除外'):
        comparison = comparison[(comparison['Me'] != 0)]

    for i in range(1, num_rivals + 1):
        if st.checkbox(f'Rival{i}が未プレイの曲を除外'):
            comparison = comparison[(comparison[f'Rival{i}'] != 0)]

    st.subheader('ライバルスコアとの比較')

    # フィルタリングされたデータフレームを表示
    st.dataframe(comparison)
