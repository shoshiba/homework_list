import re
import pandas as pd
from data_cloling import crawl_and_save_iidx_data


def fetch_data(iidx_id):
    """指定されたIIDX IDのデータを取得する"""
    return crawl_and_save_iidx_data(iidx_id)


def extract_percentage(performance):
    """Performanceからパーセンテージを抽出"""
    match = re.search(r'(\d+\.\d+%)', performance)
    return match.group(1) if match else '0.0%'


def calculate_rank(row, num_rivals):
    """スコアに基づいて順位を計算する"""
    scores = [row['Me']] + [row[f'Rival{i}'] for i in range(1, num_rivals + 1)]
    return sorted(scores, reverse=True).index(row['Me']) + 1


def extract_title_and_difficulty(title):
    """楽曲名と難易度を抽出する"""
    match = re.match(r'^(.*)\((NORMAL|HYPER|ANOTHER|LEGGENDARIA)\)$', title)
    if match:
        return match.group(1), match.group(2)
    return title, ''


def create_comparison_dataframe(dfs, num_rivals):
    """比較用のデータフレームを作成する"""
    comparison_data = {
        'Level': dfs['me']['Level'],
        'Title': dfs['me']['Title'],
        'Me': dfs['me']['Details_Number'],
        'MePer': dfs['me']['Performance'],
    }

    for i in range(1, num_rivals + 1):
        key = f'rival{i}'
        comparison_data[f'Rival{i}'] = dfs[key]['Details_Number']
        comparison_data[f'vsRival{i}'] = (dfs['me']['Details_Number']
                                          - dfs[key]['Details_Number'])
    comparison = pd.DataFrame(comparison_data).fillna(0)

    # 楽曲名と難易度を抽出して新しいカラムを作成
    comparison[['Song_Title', 'Difficulty']] = comparison.apply(
        lambda row: pd.Series(extract_title_and_difficulty(row['Title'])),
        axis=1
    )

    comparison['Rank'] = comparison.apply(
            lambda row: calculate_rank(row, num_rivals), axis=1
            )
    comparison['Me_Per'] = comparison['MePer'].apply(extract_percentage)

    columns = ['Level', 'Song_Title', 'Difficulty', 'Rank', 'Me', 'Me_Per']
    columns += [f'Rival{i}' for i in range(1, num_rivals + 1)]
    columns += [f'vsRival{i}' for i in range(1, num_rivals + 1)]
    return comparison[columns]
