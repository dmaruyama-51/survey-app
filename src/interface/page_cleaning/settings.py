import streamlit as st
import pandas as pd
from typing import Tuple
from src.utils.logger_config import logger
from src.interface.components.data_settings import (
    render_column_selection,
    render_likert_scale_selection,
)


def render_data_settings_section(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, int]:
    """データ設定セクションを表示"""
    try:
        df_to_process, df_not_to_process = render_column_selection(df)
        likert_scale = render_likert_scale_selection()

        return df_to_process, df_not_to_process, likert_scale

    except Exception as e:
        logger.error(f"Data settings error: {str(e)}")
        st.error("An error occurred while configuring data settings.")
        raise
