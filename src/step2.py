import streamlit as st
import pandas as pd


# pragma: no cover
def select_non_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    数値データではない列を選択して除外する
    Args:
        df (pd.DataFrame): 入力データフレーム
    Returns:
        pd.DataFrame: 選択された列を除外したデータフレーム
    """
    remove_cols: list[str] = st.multiselect(
        "Which column is not a numerical answer?", df.columns
    )
    _df = df.copy()
    _df = _df.drop(columns=remove_cols)
    return _df


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
