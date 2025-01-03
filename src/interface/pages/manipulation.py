import streamlit as st
import pandas as pd
from typing import Tuple, List, Dict
from src.core.manipulation import calculate_scale_scores, reverse_score
from src.utils.logger_config import logger


def render_has_reverse_items_option_section() -> bool:
    # 逆転項目の有無を確認
    has_reverse_items = st.checkbox(
        "I have items that need to be reverse-scored",
        value=False,
        help="Check this if you need to reverse-score any items",
    )
    return has_reverse_items

def render_manipulation_settings_section(df: pd.DataFrame) -> Tuple[List[str], int]:
    """データ操作設定セクションを表示"""
    try:
        # リッカート尺度のポイント数を選択
        scale_points = st.select_slider(
            "Select the number of Likert scale points",
            options=[3, 4, 5, 6, 7, 8, 9],
            value=7,
            help="Choose the number of points in your Likert scale (e.g., 5 for a 5-point scale)",
        )

        # 逆転させる列を選択
        st.write(
            "Choose the columns that need to be reverse-scored. The original columns will be preserved, and new reversed columns will be created with '_r' suffix."
        )

        reverse_columns: List[str] = st.multiselect(
            "Select columns to reverse-score",
            options=df.columns,
            help="Select one or more columns to reverse-score",
        )

        if reverse_columns:
            reversed_df = reverse_score(df, reverse_columns, scale_points)
        else:
            reversed_df = df.copy()
        return reverse_columns, scale_points, reversed_df

    except Exception as e:
        logger.error(f"Error in manipulation settings: {str(e)}")
        raise

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

def render_scale_score_section(df: pd.DataFrame) -> pd.DataFrame:
    """因子得点計算のUIセクションを表示"""
    st.markdown("#### Scale Score Calculation")
    st.write(
        "Create scale scores by selecting items that belong to each scale. "
        "Both total scores and mean scores will be calculated."
    )

    # 因子の数を選択
    num_scales = st.number_input(
        "Number of scales to create",
        min_value=1,
        max_value=10,
        value=1,
        help="Enter the number of different scales you want to calculate",
    )

    scales_config: Dict[str, List[str]] = {}
    df_with_scores = df.copy()

    # 各因子の設定
    for i in range(num_scales):
        st.markdown(f"##### Scale {i + 1}")

        # 因子名の入力
        scale_name = st.text_input(
            f"Scale {i + 1} name",
            value=f"scale_{i + 1}",
            key=f"scale_name_{i}",
            help="Enter a name for this scale (e.g., 'anxiety', 'satisfaction')",
        )

        # 項目の選択（すでに逆転済みの項目も含める）
        scale_items: List[str] = st.multiselect(
            f"Select items for {scale_name}",
            options=df.columns,
            key=f"scale_items_{i}",
            help="Select all items that belong to this scale",
        )

        if scale_items:
            scales_config[scale_name] = scale_items
            # 因子得点を計算
            df_with_scores = calculate_scale_scores(
                df_with_scores, scale_items, scale_name
            )

            # プレビューを表示
            with st.expander(f"Preview {scale_name} scores"):
                preview_cols = scale_items + [
                    f"{scale_name}_total",
                    f"{scale_name}_mean",
                ]
                st.dataframe(
                    df_with_scores[preview_cols].head(),
                    use_container_width=True,
                )

    return df_with_scores
