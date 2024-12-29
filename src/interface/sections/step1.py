import streamlit as st
import pandas as pd
from src.utils.logger_config import logger
from src.core.data_loading import load_and_validate_csv, load_sample_data


def render_file_upload_section() -> pd.DataFrame | None:
    """
    CSVファイルのアップロードセクションを表示
    Returns:
        pd.DataFrame | None: アップロードされたCSVデータ、またはNone
    """
    try:
        st.markdown("#### Upload CSV File")
        use_sample = st.checkbox(
            "Use sample data",
            help="Check this box to use sample data instead of uploading a file",
        )

        if use_sample:
            df = load_sample_data()
            if df is not None:
                st.success("Sample data loaded successfully!")
                return df
            return None

        uploaded_file = st.file_uploader(
            "Choose a CSV file", type="csv", key="file_uploader"
        )

        if uploaded_file is not None:
            df = load_and_validate_csv(uploaded_file)
            if df is not None:
                st.success("File successfully uploaded and validated!")
                return df

        return None

    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        st.error("An error occurred while uploading the file.")
        return None
