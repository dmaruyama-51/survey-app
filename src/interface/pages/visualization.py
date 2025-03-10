from typing import List

import pandas as pd
import streamlit as st

from src.interface.components.display import (
    display_histograms,
    display_statistics_summary,
)
from src.interface.components.input import input_visualization_columns


def render_visualization_settings_section(df: pd.DataFrame) -> List[str]:
    """
    可視化用のカラム選択セクションを表示

    Args:
        df: 入力データフレーム

    Returns:
        選択されたカラム名のリスト
    """
    st.markdown(
        "<div class='tight-header'><h4>Column Selection</h4></div>",
        unsafe_allow_html=True,
    )

    # カラム選択UIを表示
    selected_columns = input_visualization_columns(df)

    return selected_columns


def render_visualization_section(df: pd.DataFrame, selected_columns: List[str]) -> None:
    """
    可視化ページ全体を表示

    Args:
        df: 入力データフレーム
        selected_columns: 選択されたカラム名のリスト
    """

    # 可視化セクションを表示
    if st.button("Visualize Data", type="primary"):
        # 統計情報のサマリテーブルを表示
        display_statistics_summary(df, selected_columns)

        # ヒストグラムを表示
        display_histograms(df, selected_columns)
