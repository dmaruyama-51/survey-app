import streamlit as st
import pandas as pd
from typing import Tuple, List

# pragma: no cover
def split_numeric_and_non_numeric_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    処理の対象外のカラムと、対象カラムとでデータフレームを分割する
    Args:
        df (pd.DataFrame): 入力データフレーム
    Returns:
        pd.DataFrame: 選択された列（処理の対象外カラム）を除外したデータフレーム
        pd.DataFrame: 選択された列のみを残したデータフレーム
    """
    remove_cols: list[str] = st.multiselect(
        "Which column is not a numerical answer?", df.columns
    )
    df_to_process = df.drop(columns=remove_cols)
    df_not_to_process = df.loc[:, remove_cols]
    return df_to_process, df_not_to_process


# pragma: no cover
def select_likert_scale_points() -> int | None:
    """
    リッカート尺度のポイント数を選択する
    Returns:
        int | None: 選択されたリッカート尺度のポイント数、未選択の場合はNone
    """
    likert_scale_case = st.selectbox(
        "Which case is Likert scale?", (3, 4, 5, 6, 7, 8, 9), index=None
    )
    return likert_scale_case
