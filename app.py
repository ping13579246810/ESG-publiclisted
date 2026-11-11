import io

import pandas as pd
import requests
import streamlit as st

URL = "https://mopsfin.twse.com.tw/opendata/t187ap46_L_1.csv"  # 換連結

st.set_page_config(page_title="資料下載與顯示", layout="wide")
st.title("開放資料表格")

url = st.text_input("資料連結", value=URL)


@st.cache_data(show_spinner="下載資料中…")
def load_data(url: str) -> tuple[pd.DataFrame, bytes]:
    response = requests.get(url, verify=False, timeout=30)
    response.raise_for_status()
    content = response.content
    df = pd.read_csv(io.BytesIO(content), encoding="utf-8-sig")  # 繁體中文
    df = df.dropna()
    return df, content


if st.button("載入資料", type="primary") or "df" in st.session_state:
    try:
        df, raw = load_data(url)
        st.session_state["df"] = df
        st.success(f"共 {len(df)} 筆資料")
        st.dataframe(df, use_container_width=True)
        st.download_button(
            "下載原始 CSV",
            data=raw,
            file_name="data01.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"載入失敗：{e}")
