from typing import List, Tuple

import pandas as pd
import streamlit as st

from src.core.data_loading import load_and_validate_csv, load_sample_data, load_and_validate_excel
from src.core.dataframe_operation import split_dataframe
from src.interface.state import save_uploaded_data
from src.utils.logger_config import logger

# ==============================
# for Common
# ==============================


def input_file_upload() -> pd.DataFrame | None:
    """ファイルアップロードUIを表示"""
    try:
        st.markdown("#### Upload CSV or Excel File")

        # 既存のデータがある場合、クリアオプションを表示
        if st.session_state.uploaded_df is not None:
            if st.button("Clear uploaded data"):
                st.session_state.uploaded_df = None
                st.session_state.use_sample = False
                st.rerun()
            return st.session_state.uploaded_df

        # サンプルデータの使用オプション
        use_sample = st.checkbox(
            "Use sample data",
            value=st.session_state.use_sample,
            help="Check this box to use sample data instead of uploading a file",
        )

        if use_sample:
            df = load_sample_data()
            if df is not None:
                st.success("Sample data loaded successfully!")
                save_uploaded_data(df, is_sample=True)
                return df
            return None

        # ファイルアップロードオプション
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file", 
            type=["csv", "xlsx", "xls"], 
            key="file_uploader"
        )

        if uploaded_file is not None:
            # ファイル拡張子に基づいて適切な読み込み関数を選択
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                df = load_and_validate_csv(uploaded_file)
            elif file_extension in ['xlsx', 'xls']:
                df = load_and_validate_excel(uploaded_file)
            else:
                st.error("Unsupported file format.")
                return None
                
            if df is not None:
                st.success("File successfully uploaded and validated!")
                save_uploaded_data(df, is_sample=False)
                return df

        return None

    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        st.error("An error occurred while uploading the file.")
        return None


# ==============================
# for Cleaning
# ==============================


def input_column_selection(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, str]:
    """カラム選択UIを表示"""
    try:
        st.markdown(
            "<div class='tight-header'><h4>Column Selection</h4></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "Select columns that should not be processed as numeric data (e.g., ID, category columns)"
        )

        exclude_columns = st.radio(
            "Would you like to exclude any columns?",
            ["No, process all columns", "Yes, select columns to exclude"],
            help="Choose whether to exclude specific columns from analysis",
        )

        remove_cols: list[str] = []
        if exclude_columns == "Yes, select columns to exclude":
            remove_cols = st.multiselect(
                "Select columns to exclude",
                df.columns,
                help="You can select multiple columns. Selected columns will be excluded from the analysis.",
            )

        return *split_dataframe(df, remove_cols), exclude_columns

    except Exception as e:
        logger.error(f"Column selection error: {str(e)}")
        raise


def input_likert_scale_selection() -> int:
    """リッカート尺度選択UIを表示"""
    try:
        st.markdown(
            "<div class='tight-header'><h4>Likert Scale Configuration</h4></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "Select the number of points used in your Likert scale data. (Sample data uses a 7-point scale)"
        )

        return st.select_slider(
            "Number of Likert scale points",
            options=[3, 4, 5, 6, 7, 8, 9],
            value=7,
            help="Common scales are 5 or 7 points, but you can choose others as needed",
        )

    except Exception as e:
        logger.error(f"Likert scale selection error: {str(e)}")
        raise


def input_cleaning_options() -> Tuple[bool, bool, bool, bool]:
    """データクリーニングのオプションを表示し、選択状態を返す"""
    st.markdown("#### Data Cleaning Options")
    req1 = st.checkbox("Remove straight-line responses")
    req2 = st.checkbox("Remove responses with missing values")
    req3 = st.checkbox("Remove responses outside of valid range")
    req4 = st.checkbox("Remove step pattern responses")
    return req1, req2, req3, req4


def input_keep_records() -> List[int]:
    """保持するレコードを選択"""
    if "removed_df_with_checkbox" not in st.session_state:
        st.session_state.removed_df_with_checkbox = st.session_state.removed_df.copy()
        st.session_state.removed_df_with_checkbox.insert(0, "Keep This Row", False)
        st.session_state.editor_key = 0

    edited_df = st.data_editor(
        st.session_state.removed_df_with_checkbox,
        hide_index=True,
        column_config={
            "Keep This Row": st.column_config.CheckboxColumn(
                "Keep This Row",
                help="Select to keep this row in the final dataset",
                default=False,
            )
        },
        key=f"removed_records_editor_{st.session_state.editor_key}",
    )

    if not edited_df.equals(st.session_state.removed_df_with_checkbox):
        st.session_state.removed_df_with_checkbox = edited_df.copy()
        st.session_state.editor_key += 1
        st.rerun()

    return st.session_state.removed_df_with_checkbox[
        st.session_state.removed_df_with_checkbox["Keep This Row"]
    ].index.tolist()


# ==============================
# for Manipulation
# ==============================


def input_manipulation_settings(df: pd.DataFrame) -> Tuple[int, List[str]]:
    """データ操作設定セクションを表示"""
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

    return scale_points, reverse_columns


def input_visualization_columns(df: pd.DataFrame) -> List[str]:
    """
    可視化するカラムを選択するUIを表示

    Args:
        df: 入力データフレーム

    Returns:
        選択されたカラム名のリスト
    """
    # 数値型カラムのみを抽出
    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

    if not numeric_columns:
        st.warning(
            "No numeric columns found in the data. Visualization requires numeric data."
        )
        return []

    # 選択オプションを追加
    selection_options = ["Select individual columns", "Select all columns"]

    selection_mode = st.radio(
        "How would you like to select columns?",
        options=selection_options,
        horizontal=True,
    )

    selected_columns: List[str] = []

    if selection_mode == "Select individual columns":
        # 従来の複数選択UI
        selected_columns = st.multiselect(
            "Select columns to visualize",
            options=numeric_columns,
            default=numeric_columns[:2]
            if len(numeric_columns) >= 2
            else numeric_columns,
            help="Select one or more columns to create visualizations",
        )

    elif selection_mode == "Select all columns":
        # すべての数値カラムを選択
        selected_columns = numeric_columns
        st.success(f"All {len(numeric_columns)} numeric columns selected")

        # 必要に応じて除外するカラムを選択できるオプション
        exclude_columns: List[str] = st.multiselect(
            "Exclude columns (optional)",
            options=numeric_columns,
            default=[],
            help="Select columns you want to exclude from visualization",
        )

        if exclude_columns:
            selected_columns = [
                col for col in numeric_columns if col not in exclude_columns
            ]
            st.info(f"{len(selected_columns)} columns selected after exclusion")

    # 選択されたカラムの数を表示
    if selected_columns:
        st.session_state.selected_viz_columns = selected_columns

        # 選択カラム数の表示
        st.write(f"Selected {len(selected_columns)} columns for visualization")

    return selected_columns
