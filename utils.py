import re
import pandas as pd
from data_cloling import crawl_and_save_iidex_data

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

def extract_title_and_difficulty(title):
    """楽曲名と難易度を抽出する"""
    match = re.match(r'^(.*)\((NORMAL|HYPER|ANOTHER|LEGGENDARIA)\)$', title)
    if match:
        return match.group(1), match.group(2)
    return title, ''

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

    # 楽曲名と難易度を抽出して新しいカラムを作成
    comparison[['Song_Title', 'Difficulty']] = comparison.apply(
        lambda row: pd.Series(extract_title_and_difficulty(row['Title'])),
        axis=1
    )

    comparison['Rank'] = comparison.apply(calculate_rank, axis=1)
    comparison['Me_Per'] = comparison['MePer'].apply(extract_percentage)
    return comparison[['Level', 'Song_Title', 'Difficulty', 'Rank', 'Me', 'Me_Per', 'Rival1', 'Rival2', 'Rival3', 'vsRival1', 'vsRival2', 'vsRival3']]
