import streamlit as st

from src.interface.pages.common import render_file_upload_section
from src.interface.pages.visualization import (
    render_visualization_section,
    render_visualization_settings_section,
)
from src.interface.state import (
    check_file_upload_completion,
    check_visualization_selection_completion,
)
from src.utils.logger_config import logger

try:
    logger.info("Data Visualization Page loaded")
    st.title("Data Visualization")
    st.markdown("Visualize your survey data with interactive charts and graphs.")

    st.markdown(
        """
        <style>
        .step1-header h3 {
            margin-top: 1rem !important;
            margin-bottom: 0px;
        }
        .step-header h3 {
            margin-top: 3rem !important;
            margin-bottom: 0px;
        }
        .tight-header + hr {
            margin-top: 0px;
            margin-bottom: 2rem;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # -----------------------------------
    # Step1. Upload Survey Data
    # -----------------------------------
    st.markdown(
        "<div class='tight-header step1-header'><h3>📌 Step 1: Upload Survey Data</h3></div><hr/>",
        unsafe_allow_html=True,
    )
    df = render_file_upload_section()

    # Step1の完了チェック
    if check_file_upload_completion(df):
        # -----------------------------------
        # Step2. Select Columns for Visualization
        # -----------------------------------
        st.markdown(
            "<div class='tight-header step-header'><h3>📌 Step 2: Select Columns for Visualization</h3></div><hr/>",
            unsafe_allow_html=True,
        )
        selected_columns = render_visualization_settings_section(df)

        if check_visualization_selection_completion(selected_columns):
            # -----------------------------------
            # Step3. Data Visualization
            # -----------------------------------
            st.markdown(
                "<div class='tight-header step-header'><h3>📌 Step 3: Data Visualization</h3></div><hr/>",
                unsafe_allow_html=True,
            )

            render_visualization_section(df, selected_columns)


except Exception as e:
    logger.error(f"Application error: {str(e)}")
    st.error("An unexpected error occurred.")
