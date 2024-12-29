import pandas as pd
import streamlit as st
from pathlib import Path
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
        logger.error(f"CSVファイル読み込みエラー: {str(e)}")
        st.error("CSVファイルの読み込み中にエラーが発生しました。")
        return None


def load_sample_data() -> pd.DataFrame | None:
    """サンプルデータを読み込む"""
    try:
        # プロジェクトのルートディレクトリを取得
        root_dir = Path(__file__).parent.parent.parent
        sample_path = root_dir / "src" / "core" / "data" / "sample.csv"

        if not sample_path.exists():
            logger.error(f"サンプルデータファイルが見つかりません: {sample_path}")
            st.error("サンプルデータファイルが見つかりません。")
            return None

        df = pd.read_csv(sample_path)
        logger.info(f"サンプルデータ読み込み完了 shape: {df.shape}")
        return df

    except Exception as e:
        logger.error(f"サンプルデータ読み込みエラー: {str(e)}")
        st.error("サンプルデータの読み込み中にエラーが発生しました。")
        return None
