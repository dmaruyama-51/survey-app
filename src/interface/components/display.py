import streamlit as st
import pandas as pd
from src.core.dataframe_operation import create_final_dataset
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
