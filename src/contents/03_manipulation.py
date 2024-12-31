import streamlit as st
from src.interface.sections.file_upload import render_file_upload_section
from src.interface.sections.manipulation_settings import render_manipulation_settings_section
from src.interface.sections.manipulation_preview import render_manipulation_preview_section
from src.interface.components.data_summary import display_data_summary
from src.interface.state import check_file_upload_completion
from src.utils.logger_config import logger

try:
    logger.info("Data Manipulation Page loaded")
    st.title("Data Manipulation")
    st.markdown("Transform your survey data with reverse scoring")

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
    try:
        df = render_file_upload_section()
        if df is not None:
            logger.info(f"Data loaded successfully. Shape: {df.shape}")
            display_data_summary(df)
        else:
            logger.warning("No data loaded")
    except Exception as e:
        logger.error(f"Data loading error: {str(e)}")
        st.error("Failed to load data. Please check your file.")

    # Step1の完了チェック
    if check_file_upload_completion(df):
        # -----------------------------------
        # Step2. Configure Reverse Scoring
        # -----------------------------------
        st.markdown(
            "<div class='tight-header step-header'><h3>📌 Step 2: Configure Reverse Scoring</h3></div><hr/>",
            unsafe_allow_html=True,
        )
        try:
            reverse_columns, scale_points = render_manipulation_settings_section(df)

            # Step2の完了チェック
            if reverse_columns:
                # -----------------------------------
                # Step3. Preview and Download Results
                # -----------------------------------
                st.markdown(
                    "<div class='tight-header step-header'><h3>📌 Step 3: Preview and Download Results</h3></div><hr/>",
                    unsafe_allow_html=True,
                )
                try:
                    render_manipulation_preview_section(df, reverse_columns, scale_points)
                except Exception as e:
                    logger.error(f"Data processing error: {str(e)}")
                    st.error("An error occurred while processing the data.")
            else:
                st.info("Please select at least one column to reverse-score.", icon="ℹ️")

        except Exception as e:
            logger.error(f"Step 2 configuration error: {str(e)}")
            st.error("An error occurred in Step 2 configuration.")

except Exception as e:
    logger.error(f"Application error: {str(e)}")
    st.error("An unexpected error occurred.")
