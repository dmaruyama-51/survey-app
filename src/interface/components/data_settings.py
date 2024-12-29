import streamlit as st
from typing import Tuple
import pandas as pd
from src.core.data_processing import split_dataframe
from src.utils.logger_config import logger


def render_column_selection(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """カラム選択UIを表示"""
    try:
        st.markdown(
            "<div class='tight-header'><h4>Column Selection</h4></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "Select columns that should not be processed as numeric data (e.g., ID, category columns)"
        )

        remove_cols: list[str] = st.multiselect(
            "Select columns to exclude",
            df.columns,
            help="You can select multiple columns. Selected columns will be excluded from the analysis.",
        )

        return split_dataframe(df, remove_cols)

    except Exception as e:
        logger.error(f"カラム選択エラー: {str(e)}")
        raise


def render_likert_scale_selection() -> int:
    """リッカート尺度選択UIを表示"""
    try:
        st.markdown(
            "<div class='tight-header'><h4>Likert Scale Configuration</h4></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "Select the number of points used in your Likert scale data. (Sample data uses a 7-point scale)"
        )

        return st.select_slider(
            "Number of Likert scale points",
            options=[3, 4, 5, 6, 7, 8, 9],
            value=7,
            help="Common scales are 5 or 7 points, but you can choose others as needed",
        )

    except Exception as e:
        logger.error(f"リッカート尺度選択エラー: {str(e)}")
        raise
