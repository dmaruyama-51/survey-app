import streamlit as st
import pandas as pd
from typing import List
from src.utils.logger_config import logger


def render_manipulation_preview_section(
    original_df: pd.DataFrame,
    processed_df: pd.DataFrame,
    reverse_columns: List[str],
    scale_points: int,
) -> None:
    """データ操作のプレビューとダウンロードセクションを表示"""
    try:
        # 逆転項目の有無でタブ構成を変更
        if reverse_columns:
            tabs = st.tabs(["Original Data", "Reversed Scores", "Scale Scores"])
        else:
            tabs = st.tabs(["Original Data", "Scale Scores"])

        with tabs[0]:
            st.write("Original values:")
            if reverse_columns:
                st.dataframe(
                    original_df[reverse_columns],
                    use_container_width=True,
                )
            else:
                st.dataframe(
                    original_df,
                    use_container_width=True,
                )

        if reverse_columns:
            with tabs[1]:
                reversed_columns = [f"{col}_r" for col in reverse_columns]
                st.write("Reversed values:")
                st.dataframe(
                    processed_df[reversed_columns],
                    use_container_width=True,
                )
            scale_scores_tab = tabs[2]
        else:
            scale_scores_tab = tabs[1]

        with scale_scores_tab:
            score_columns = [
                col for col in processed_df.columns if col.endswith(("_total", "_mean"))
            ]
            if score_columns:
                st.write("Scale scores:")
                st.dataframe(
                    processed_df[score_columns],
                    use_container_width=True,
                )
            else:
                st.info("No scale scores calculated yet.")

        # ダウンロードオプション
        st.markdown("#### Download Options")

        # 逆転項目の有無でダウンロードオプションを変更
        if reverse_columns:
            download_options = [
                "Include all columns",
                "Include only reversed and scale score columns",
                "Include only scale score columns",
            ]
        else:
            download_options = [
                "Include all columns",
                "Include only scale score columns",
            ]

        download_option = st.radio(
            "Select columns to include in download:",
            options=download_options,
            help="Choose which columns to include in the downloaded file",
        )

        # ダウンロード用のデータフレームを準備
        if download_option == "Include only scale score columns":
            download_df = (
                processed_df[score_columns].copy() if score_columns else processed_df
            )
        elif download_option == "Include only reversed and scale score columns":
            reversed_columns = [f"{col}_r" for col in reverse_columns]
            download_df = processed_df[reversed_columns + score_columns].copy()
        else:
            download_df = processed_df

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
