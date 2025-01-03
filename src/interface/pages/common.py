from src.interface.components.display import display_data_summary
from src.interface.components.input import input_file_upload
from src.utils.logger_config import logger
import streamlit as st


def render_file_upload_section():
    """ファイルアップロードセクションを表示"""
    try:
        df = input_file_upload()
        if df is not None:
            logger.info(f"Data loaded successfully. Shape: {df.shape}")
            display_data_summary(df)
        else:
            logger.warning("No data loaded")
        return df
    except Exception as e:
        logger.error(f"Data loading error: {str(e)}")
        st.error("Failed to load data. Please check your file.")
