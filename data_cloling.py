import requests
from bs4 import BeautifulSoup
import pandas as pd


def crawl_and_save_iidex_data(iidx_id):
# 指定されたURL

    
    url = f"http://ereter.net/iidxplayerdata/{iidx_id}/level"
    # ページの内容を取得

    data = []
    for i in range(1,13):
        urls = [url, "/", str(i)]
        hoge = "".join(urls)

        response = requests.get(hoge)
        soup = BeautifulSoup(response.content, "html.parser")
        
        
        table = soup.find("table",class_="table condensed")
        
        # テーブルデータをリストに変換
        rows = table.find_all("tr")
        
        for row in rows:
            cols = row.find_all("td")
            if cols:
                cols = [col.get_text(strip=True) for col in cols]
                data.append(cols)
        
    # カラム名を定義（必要に応じて適切な名前を付ける）
    column_names = ["Level", "Title", "Rank", "Details", "Performance", "Difficulty"]
    
    # Pandas DataFrameに変換
    df = pd.DataFrame(data, columns=column_names)
    
    # "Details" カラムから数値を抽出し、新しいカラムとして追加
    df["Details"] = df["Details"].replace("", "0")
    df["Details_Number"] = df["Details"].str.extract(r'(\d+)').fillna(0).astype(int)
    
    # 不要なカラムがあれば削除（例として "Details" カラムを削除）
    df.drop(columns=["Details"], inplace=True)
        
        # データフレームを表示
    return df