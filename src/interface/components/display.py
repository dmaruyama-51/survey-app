from typing import List

import pandas as pd
import plotly.express as px
import streamlit as st

from src.core.dataframe_operation import create_final_dataset
from src.core.visualization import (
    calculate_statistics,
    check_ceiling_effect,
    check_floor_effect,
    create_statistics_summary,
)
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

        st.write("Data content:")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        logger.error(f"Error displaying data summary: {str(e)}")
        st.error("An error occurred while displaying the data.")


def disaply_final_dataset(rows_to_keep: list) -> pd.DataFrame:
    """最終的にダウンロードされるデータセットを作成してUIに表示"""
    final_cleaned_df = create_final_dataset(
        st.session_state.cleaned_df, st.session_state.removed_df, rows_to_keep
    )

    if rows_to_keep:
        st.write(
            f"Final dataset will keep {len(rows_to_keep)} previously removed rows."
        )

    return final_cleaned_df


def display_statistics_summary(df: pd.DataFrame, selected_columns: List[str]) -> None:
    """
    統計情報のサマリテーブルを表示

    Args:
        df: 入力データフレーム
        selected_columns: 表示するカラム名のリスト
    """
    st.markdown("#### Statistical Summary")

    # 統計情報のサマリテーブルを作成
    stats_df = create_statistics_summary(df, selected_columns)

    # サマリテーブルを表示
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

    # 効果の説明
    with st.expander("What are Ceiling and Floor Effects?"):
        st.markdown("""
        **Ceiling Effect**: Occurs when a measure has a distinct upper limit for potential responses and a large concentration of participants score at or near this limit. Statistically detected when Mean + SD > Maximum value.
        
        **Floor Effect**: Occurs when a measure has a distinct lower limit for potential responses and a large concentration of participants score at or near this limit. Statistically detected when Mean - SD < Minimum value.
        
        These effects can limit the ability to distinguish between participants at the extremes and may reduce the validity of the measure.
        """)


def display_histograms(df: pd.DataFrame, selected_columns: List[str]) -> None:
    """
    選択されたカラムのヒストグラムを表示

    Args:
        df: 入力データフレーム
        selected_columns: 表示するカラム名のリスト
    """
    st.markdown("#### Histograms")

    display_columns = selected_columns

    st.write(f"Displaying histograms for {len(display_columns)} columns:")

    # 選択されたカラムの数に応じてレイアウトを調整
    if len(display_columns) == 1:
        # 1つのカラムの場合は大きく表示
        display_single_histogram(df, display_columns[0])
    else:
        # 複数のカラムの場合は2列のグリッドで表示
        display_multiple_histograms(df, display_columns)


def display_single_histogram(df: pd.DataFrame, column: str) -> None:
    """
    単一カラムのヒストグラムを表示

    Args:
        df: 入力データフレーム
        column: 表示するカラム名
    """
    fig = px.histogram(
        df,
        x=column,
        title=f"Distribution of {column}",
        labels={column: column},
        color_discrete_sequence=["#3366CC"],
        opacity=0.7,
    )
    fig.update_layout(
        xaxis_title=column, yaxis_title="Frequency", bargap=0.1, height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # 統計情報を計算
    stats = calculate_statistics(df, column)

    # 天井効果と床効果の判定
    ceiling_effect = check_ceiling_effect(stats)
    floor_effect = check_floor_effect(stats)

    # 統計情報と効果の表示
    stats_md = f"**Statistics for {column}:**  \n"
    stats_md += f"Mean: {stats['mean']:.2f}  \n"
    stats_md += f"Standard Deviation: {stats['std']:.2f}  \n"
    stats_md += f"Min: {stats['min']:.2f}, Max: {stats['max']:.2f}  \n"

    if ceiling_effect:
        stats_md += f"⚠️ **Ceiling Effect Detected**: Mean + SD ({stats['mean_plus_std']:.2f}) > Max ({stats['max']:.2f})  \n"
    if floor_effect:
        stats_md += f"⚠️ **Floor Effect Detected**: Mean - SD ({stats['mean_minus_std']:.2f}) < Min ({stats['min']:.2f})  \n"

    st.markdown(stats_md)


def display_multiple_histograms(df: pd.DataFrame, columns: List[str]) -> None:
    """
    複数カラムのヒストグラムを2列グリッドで表示

    Args:
        df: 入力データフレーム
        columns: 表示するカラム名のリスト
    """
    cols = st.columns(2)
    for i, column in enumerate(columns):
        with cols[i % 2]:
            fig = px.histogram(
                df,
                x=column,
                title=f"Distribution of {column}",
                labels={column: column},
                color_discrete_sequence=["#3366CC"],
                opacity=0.7,
            )
            fig.update_layout(
                xaxis_title=column, yaxis_title="Frequency", bargap=0.1, height=350
            )
            st.plotly_chart(fig, use_container_width=True)

            # 統計情報を計算
            stats = calculate_statistics(df, column)

            # 天井効果と床効果の判定
            ceiling_effect = check_ceiling_effect(stats)
            floor_effect = check_floor_effect(stats)

            # 統計情報と効果の表示
            stats_md = f"**Statistics for {column}:**  \n"
            stats_md += f"Mean: {stats['mean']:.2f}  \n"
            stats_md += f"Standard Deviation: {stats['std']:.2f}  \n"
            stats_md += f"Min: {stats['min']:.2f}, Max: {stats['max']:.2f}  \n"

            if ceiling_effect:
                stats_md += f"⚠️ **Ceiling Effect Detected**: Mean + SD ({stats['mean_plus_std']:.2f}) > Max ({stats['max']:.2f})  \n"
            if floor_effect:
                stats_md += f"⚠️ **Floor Effect Detected**: Mean - SD ({stats['mean_minus_std']:.2f}) < Min ({stats['min']:.2f})  \n"

            st.markdown(stats_md)
