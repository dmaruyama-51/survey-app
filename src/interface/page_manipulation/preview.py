import streamlit as st
import pandas as pd
from typing import List
from src.core.manipulation import reverse_score, prepare_download_data
from src.utils.logger_config import logger


def render_manipulation_preview_section(
    df: pd.DataFrame, reverse_columns: List[str], scale_points: int
) -> None:
    """データ操作のプレビューとダウンロードセクションを表示"""
    try:
        # タブでオリジナルと変換後のデータを表示
        tab1, tab2 = st.tabs(["Original Data", "Data with Reversed Scores"])

        with tab1:
            st.write("Original values:")
            st.dataframe(
                df[reverse_columns],
                use_container_width=True,
            )

        with tab2:
            reversed_df = reverse_score(df, reverse_columns, scale_points)
            reversed_columns = [f"{col}_r" for col in reverse_columns]
            st.write("Reversed values:")
            st.dataframe(
                reversed_df[reversed_columns],
                use_container_width=True,
            )

        # ダウンロードオプション
        st.markdown("#### Download Options")

        download_option = st.radio(
            "Select columns to include in download:",
            options=[
                "Include both original and reversed columns",
                "Include only reversed columns",
            ],
            help="Choose whether to keep or remove the original columns in the downloaded file",
        )

        # ダウンロード用のデータフレームを準備
        include_original = (
            download_option == "Include both original and reversed columns"
        )
        download_df = prepare_download_data(
            df, reversed_df, reverse_columns, include_original
        )

        st.write("Preview of data to be downloaded:")
        st.dataframe(download_df.head(), use_container_width=True)

        csv = download_df.to_csv(index=False)
        st.download_button(
            label="Download Processed Data",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv",
            type="primary",
        )

    except Exception as e:
        logger.error(f"Manipulation preview error: {str(e)}")
        st.error("An error occurred while displaying the preview.")
        raise
