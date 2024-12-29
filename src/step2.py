import streamlit as st
import pandas as pd
from typing import Tuple
from src.utils.logger_config import logger


# pragma: no cover
def split_numeric_and_non_numeric_columns(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """データフレームを処理対象と非対象に分割する"""
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

        df_to_process = df.drop(columns=remove_cols)
        df_not_to_process = df.loc[:, remove_cols]

        logger.info(f"除外カラム選択: {remove_cols}")
        logger.info(f"処理対象データ shape: {df_to_process.shape}")
        logger.info(f"除外データ shape: {df_not_to_process.shape}")

        return df_to_process, df_not_to_process
    except Exception as e:
        logger.error(f"データフレーム分割エラー: {str(e)}")
        raise


# pragma: no cover
def select_likert_scale_points() -> int | None:
    """リッカート尺度のポイント数を選択する"""
    try:
        st.markdown(
            "<div class='tight-header'><h4>Likert Scale Configuration</h4></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "Select the number of points used in your Likert scale data. (Sample data uses a 7-point scale)"
        )

        likert_scale_case = st.select_slider(
            "Number of Likert scale points",
            options=[3, 4, 5, 6, 7, 8, 9],
            value=7,
            help="Common scales are 5 or 7 points, but you can choose others as needed",
        )

        return likert_scale_case
    except Exception as e:
        logger.error(f"リッカート尺度選択エラー: {str(e)}")
        raise


def check_step2_completion(remove_cols: list[str], likert_scale: int | None) -> bool:
    """Step2の要件が満たされているかチェックする"""
    if not remove_cols and likert_scale is None:
        st.info(
            "Please start by selecting columns to exclude and configuring the Likert scale.",
            icon="ℹ️",
        )
        return False
    elif not remove_cols:
        st.info("Please select columns to exclude from numeric processing.", icon="ℹ️")
        return False
    elif likert_scale is None:
        st.info("Please select the number of Likert scale points.", icon="ℹ️")
        return False
    return True
