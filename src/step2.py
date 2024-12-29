import streamlit as st
import pandas as pd
from typing import Tuple
from src.utils.logger_config import logger


# pragma: no cover
def split_numeric_and_non_numeric_columns(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    処理の対象外のカラムと、対象カラムとでデータフレームを分割する
    Args:
        df (pd.DataFrame): 入力データフレーム
    Returns:
        pd.DataFrame: 選択された列（処理の対象外カラム）を除外したデータフレーム
        pd.DataFrame: 選択された列のみを残したデータフレーム
    """
    try:
        remove_cols: list[str] = st.multiselect(
            "Select non-numeric columns to exclude", df.columns
        )
        logger.info(f"除外カラム選択: {remove_cols}")

        df_to_process = df.drop(columns=remove_cols)
        df_not_to_process = df.loc[:, remove_cols]

        logger.info(f"処理対象データ shape: {df_to_process.shape}")
        logger.info(f"除外データ shape: {df_not_to_process.shape}")

        return df_to_process, df_not_to_process
    except Exception as e:
        logger.error(f"データフレーム分割エラー: {str(e)}")
        raise


# pragma: no cover
def select_likert_scale_points() -> int | None:
    """
    リッカート尺度のポイント数を選択する
    Returns:
        int | None: 選択されたリッカート尺度のポイント数、未選択の場合はNone
    """
    try:
        likert_scale_case = st.selectbox(
            "Select the number of Likert scale points", (3, 4, 5, 6, 7, 8, 9), index=4
        )
        st.info("Note: Sample data uses a 7-point Likert scale.")
        if likert_scale_case is not None:
            logger.info(f"リッカート尺度ポイント選択: {likert_scale_case}")
        else:
            logger.info("リッカート尺度未選択")
        return likert_scale_case
    except Exception as e:
        logger.error(f"リッカート尺度選択エラー: {str(e)}")
        raise
