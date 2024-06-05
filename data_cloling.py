import requests
from bs4 import BeautifulSoup
import pandas as pd

def crawl_and_save_iidex_data(url):
# 指定されたURL
    url = "http://ereter.net/iidxplayerdata/16548190"
    
    # ページの内容を取得
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    
    table = soup.find("table",class_="table condensed")
    
    print(table.prettify())
    
    
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
    
    # "Details" カラムから数値を抽出し、新しいカラムとして追加
    df["Details"] = df["Details"].replace("", "0")
    df["Details_Number"] = df["Details"].str.extract(r'(\d+)').astype(int)
    
    # 不要なカラムがあれば削除（例として "Details" カラムを削除）
    df.drop(columns=["Details"], inplace=True)
    
    # データフレームを表示
    print(df)
    
    # CSVファイルとして保存
    df.to_csv("iidx_player_data.csv", index=False, encoding="utf-8")
    #with open("iidx_player_data.txt", "w", encoding="utf-8") as file:



# 例として、プレイヤーデータの一部を抽出
# プレイヤー名を取得
#player_name = soup.find("div", class_="player_name").text

# その他のデータを取得（例として、クラスとDJポイントを取得）
#class_rank = soup.find("div", class_="class_rank").text
#dj_points = soup.find("div", class_="dj_points").text

#print("Player Name:", player_name)
#print("Class Rank:", class_rank)
#print("DJ Points:", dj_points)