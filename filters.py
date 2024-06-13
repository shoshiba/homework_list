import streamlit as st

DIFFICULTY_ORDER = ['NORMAL', 'HYPER', 'ANOTHER', 'LEGGENDARIA']


def apply_filters(comparison, dfs, num_rivals):
    with st.sidebar:
        st.header('フィルター設定')

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
        for level in levels:
            if st.checkbox(level, value=st.session_state.selected_levels[level], key=f'level_{level}'):
                selected_levels.append(level)

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
        for difficulty in difficulties:
            if st.checkbox(difficulty, value=st.session_state.selected_difficulty[difficulty], key=difficulty):
                selected_difficulties.append(difficulty)

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
        for rank in ranks:
            rank_str = str(rank)
            if rank_str not in st.session_state.selected_rank:
                st.session_state.selected_rank[rank_str] = True
            if st.checkbox(rank_str, value=st.session_state.selected_rank[rank_str], key=rank_str):
                selected_ranks.append(rank)

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

    return comparison
