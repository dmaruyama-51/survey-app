from pathlib import Path

import pandas as pd
import streamlit as st

from src.utils.logger_config import logger


def load_and_validate_csv(file) -> pd.DataFrame | None:
    """
    CSVファイルを読み込み、基本的なバリデーションを実行
    Args:
        file: アップロードされたファイルオブジェクト
    Returns:
        pd.DataFrame | None: 有効なデータフレーム、またはNone
    """
    try:
        df = pd.read_csv(file)

        if df.empty:
            st.error("The uploaded file is empty.")
            return None

        if len(df.columns) < 2:
            st.error("The file must contain at least two columns.")
            return None

        return df

    except Exception as e:
        logger.error(f"CSV file loading error: {str(e)}")
        st.error("An error occurred while reading the CSV file.")
        return None


def load_sample_data() -> pd.DataFrame | None:
    """サンプルデータを読み込む"""
    try:
        # プロジェクトのルートディレクトリを取得
        root_dir = Path(__file__).parent.parent.parent
        sample_path = root_dir / "src" / "core" / "data" / "sample.csv"

        if not sample_path.exists():
            logger.error(f"Sample data file not found: {sample_path}")
            st.error("Sample data file not found.")
            return None

        df = pd.read_csv(sample_path)
        logger.info(f"Sample data loaded successfully. Shape: {df.shape}")
        return df

    except Exception as e:
        logger.error(f"Sample data loading error: {str(e)}")
        st.error("An error occurred while loading the sample data.")
        return None


def load_and_validate_excel(file) -> pd.DataFrame | None:
    """
    Excelファイルを読み込み、基本的なバリデーションを実行
    Args:
        file: アップロードされたファイルオブジェクト
    Returns:
        pd.DataFrame | None: 有効なデータフレーム、またはNone
    """
    try:
        # ファイル識別子を作成（ファイル名とサイズの組み合わせ）
        file_id = f"{file.name}_{file.size}"

        # シート名のリストを取得
        xls = pd.ExcelFile(file, engine="openpyxl")
        sheet_names = xls.sheet_names

        # セッション状態の初期化
        if (
            "excel_file_id" not in st.session_state
            or st.session_state.excel_file_id != file_id
        ):
            st.session_state.excel_file_id = file_id
            st.session_state.excel_sheets = sheet_names
            st.session_state.selected_sheet = sheet_names[0]
            st.session_state.sheet_confirmed = False if len(sheet_names) > 1 else True

        # シートが複数ある場合は選択UIを表示
        if len(sheet_names) > 1:
            col1, col2 = st.columns([3, 1])
            with col1:
                selected_sheet = st.selectbox(
                    "Select a sheet to load:",
                    options=sheet_names,
                    index=sheet_names.index(st.session_state.selected_sheet),
                    key="sheet_selector",
                )

            with col2:
                confirm_button = st.button("Load Selected Sheet", type="primary")
                if confirm_button:
                    st.session_state.selected_sheet = selected_sheet
                    st.session_state.sheet_confirmed = True

            if not st.session_state.sheet_confirmed:
                st.info(
                    "Please select a sheet and click 'Load Selected Sheet' to continue."
                )
                return None
        else:
            selected_sheet = sheet_names[0]
            st.info(f"Loading the only sheet: {selected_sheet}")

        # 選択されたシートを読み込む
        df = pd.read_excel(
            file, sheet_name=st.session_state.selected_sheet, engine="openpyxl"
        )

        if df.empty:
            st.error("The uploaded file is empty.")
            return None

        if len(df.columns) < 2:
            st.error("The file must contain at least two columns.")
            return None

        return df

    except Exception as e:
        logger.error(f"Excel file loading error: {str(e)}")
        st.error("An error occurred while reading the Excel file.")
        return None
