import streamlit as st
import pandas as pd
from src.utils.logger_config import logger


def display_data_summary(df: pd.DataFrame) -> None:
    """
    データフレームの基本情報を表示
    Args:
        df (pd.DataFrame): 表示対象のデータフレーム
    """
    try:
        st.markdown("#### Data Summary")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Number of rows: {df.shape[0]}")
        with col2:
            st.write(f"Number of columns: {df.shape[1]}")

        st.write("First few rows of the data:")
        st.dataframe(df.head(), use_container_width=True)

    except Exception as e:
        logger.error(f"データサマリー表示エラー: {str(e)}")
        st.error("データの表示中にエラーが発生しました。")
