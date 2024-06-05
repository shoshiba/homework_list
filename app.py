import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from data_cloling import crawl_and_save_iidex_data

def crawl_iidx_data(url):
    # ページの内容を取得
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # テーブルを取得
    table = soup.find("table")

    # テーブルデータをリストに変換
    rows = table.find_all("tr")
    data = []

    for row in rows:
        cols = row.find_all("td")
        if cols:
            cols = [col.get_text(strip=True) for col in cols]
            data.append(cols)

    # カラム名を定義（必要に応じて適切な名前を付ける）
    column_names = ["Level", "Song", "Score", "Details", "Performance", "Difficulty"]

    # Pandas DataFrameに変換
    df = pd.DataFrame(data, columns=column_names)

    # "Details" カラムの空欄を0に置換
    df["Details"] = df["Details"].replace("", "0")

    # "Details" カラムから数値を抽出し、新しいカラムとして追加
    df["Details_Number"] = df["Details"].str.extract(r'(\d+)').fillna(0).astype(int)

    return df

# Streamlitアプリの設定
st.title('IIDX Player Data')

iidx_id = st.text_input('Enter the URL of IIDX player data:', '16548190')

if st.button('Fetch Data'):
    df = crawl_and_save_iidex_data(iidx_id)
    st.dataframe(df)

# このコードを実行するには、ターミナルで以下のコマンドを実行します：
# streamlit run app.py
