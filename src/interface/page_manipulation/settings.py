import streamlit as st
import pandas as pd
from typing import Tuple, List
from src.utils.logger_config import logger


def render_manipulation_settings_section(df: pd.DataFrame) -> Tuple[List[str], int]:
    """データ操作設定セクションを表示"""
    try:
        # リッカート尺度のポイント数を選択
        scale_points = st.select_slider(
            "Select the number of Likert scale points",
            options=[3, 4, 5, 6, 7, 8, 9],
            value=7,
            help="Choose the number of points in your Likert scale (e.g., 5 for a 5-point scale)",
        )

        # 逆転させる列を選択
        st.write(
            "Choose the columns that need to be reverse-scored. The original columns will be preserved, and new reversed columns will be created with '_r' suffix."
        )

        reverse_columns: List[str] = st.multiselect(
            "Select columns to reverse-score",
            options=df.columns,
            help="Select one or more columns to reverse-score",
        )

        return reverse_columns, scale_points

    except Exception as e:
        logger.error(f"Error in manipulation settings: {str(e)}")
        raise
