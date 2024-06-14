"""
IIDX DataをClolingするためのモジュール
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def crawl_iidx_data(iidx_id: str) -> str:
    """指定されたIIDX IDのデータをクローリングして返す"""
    base_url = f"http://ereter.net/iidxplayerdata/{iidx_id}/level"
    data = []
    for i in range(1, 13):
        url = f"{base_url}/{i}"
        response = requests.get(url)
        HTTP_OK = 200
        if response.status_code != HTTP_OK:
            print(f"Failed to retrieve data from {url}")
            continue
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="table condensed")
        if not table:
            print(f"No table found on page {url}")
            continue
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if cols:
                cols = [col.get_text(strip=True) for col in cols]
                data.append(cols)

    return data


def create_iidx_dataframe(data: list) -> pd.DataFrame:
    """クローリングされたデータからDatatableを作成して返す"""
    column_names = [
        "Level",
        "Title",
        "Rank",
        "Details",
        "Performance",
        "Difficulty",
    ]
    df = pd.DataFrame(data, columns=column_names)
    df["Details"] = df["Details"].replace("", "0")
    df["Details_Number"] = (
        df["Details"].str.extract(r"(\d+)").fillna(0).astype(int)
    )
    df["Rank"] = df["Rank"].replace("", "99999").astype(int)

    df.drop(columns=["Details"], inplace=True)

    return df


def crawl_and_save_iidx_data(iidx_id: str) -> pd.DataFrame:
    """IIDX IDに基づいてデータをクローリングし、Datatableを作成して返す"""
    raw_data = crawl_iidx_data(iidx_id)
    df = create_iidx_dataframe(raw_data)
    return df
