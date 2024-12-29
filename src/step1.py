# pragma: no cover
import streamlit as st
import pandas as pd
from src.utils.logger_config import logger
from typing import Optional


# pragma: no cover
def load_survey_data() -> Optional[pd.DataFrame]:
    """
    CSVファイルをアップロードまたはサンプルデータを読み込む
    Returns:
        pd.DataFrame | None: 読み込んだデータフレーム、またはNone
    """
    try:
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

        is_use_sample_data = st.checkbox("Try with sample data")
        if is_use_sample_data:
            logger.info("サンプルデータ使用")
            try:
                df = pd.read_csv("src/data/sample.csv")
                logger.info(f"サンプルデータ読み込み完了 shape: {df.shape}")
            except Exception as e:
                logger.error(f"サンプルデータ読み込みエラー: {str(e)}")
                raise
        elif uploaded_file is not None:
            logger.info("アップロードファイル検出")
            try:
                df = pd.read_csv(uploaded_file)
                logger.info(f"アップロードデータ読み込み完了 shape: {df.shape}")
            except Exception as e:
                logger.error(f"アップロードファイル読み込みエラー: {str(e)}")
                raise
        else:
            logger.info("ファイル未アップロード")
            df = None
        return df

    except Exception as e:
        logger.error(f"データ読み込み処理エラー: {str(e)}")
        raise


# pragma: no cover
def display_data_summary(df: pd.DataFrame) -> None:
    """
    アップロードされたデータのプレビューと基本統計量を表示
    Args:
        df (pd.DataFrame): 表示するデータフレーム
    """
    try:
        logger.info("データサマリー表示開始")
        st.markdown("#### Data Preview")
        st.write(df)
        st.markdown("#### Summary Statistics")
        st.write(df.describe())
        logger.info("データサマリー表示完了")
    except Exception as e:
        logger.error(f"データサマリー表示エラー: {str(e)}")
        raise
