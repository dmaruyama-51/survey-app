import streamlit as st
from src.interface.page_common.file_upload import render_file_upload_section
from src.interface.page_manipulation.settings import (
    render_manipulation_settings_section,
)
from src.interface.page_manipulation.preview import render_manipulation_preview_section
from src.interface.components.data_summary import display_data_summary
from src.interface.state import (
    check_file_upload_completion,
    check_manipulation_settings_completion,
    check_scale_scores_completion,
)
from src.utils.logger_config import logger
from src.interface.page_manipulation.scale_scores import render_scale_score_section
from src.core.manipulation import reverse_score
from typing import List

try:
    logger.info("Data Manipulation Page loaded")
    st.title("Data Manipulation")
    st.markdown(
        "Create reverse-scored items and calculate scale scores for your survey data."
    )

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

    if check_file_upload_completion(df):
        # -----------------------------------
        # Step2. Configure Reverse Scoring (Optional)
        # -----------------------------------
        st.markdown(
            "<div class='tight-header step-header'><h3>📌 Step 2: Configure Reverse Scoring (Optional)</h3></div><hr/>",
            unsafe_allow_html=True,
        )
        try:
            # 逆転項目の有無を確認
            has_reverse_items = st.checkbox(
                "I have items that need to be reverse-scored",
                value=False,
                help="Check this if you need to reverse-score any items",
            )

            reverse_columns: List[str] = []
            scale_points = 7
            reversed_df = df.copy() if df is not None else None

            if has_reverse_items and df is not None:
                reverse_columns, scale_points = render_manipulation_settings_section(df)
                if reverse_columns:
                    reversed_df = reverse_score(df, reverse_columns, scale_points)

            if check_manipulation_settings_completion(
                has_reverse_items, reverse_columns
            ):
                # -----------------------------------
                # Step3. Calculate Scale Scores
                # -----------------------------------
                st.markdown(
                    "<div class='tight-header step-header'><h3>📌 Step 3: Calculate Scale Scores</h3></div><hr/>",
                    unsafe_allow_html=True,
                )
                try:
                    df_with_scores = render_scale_score_section(reversed_df)

                    if check_scale_scores_completion(df_with_scores):
                        # -----------------------------------
                        # Step4. Preview and Download Results
                        # -----------------------------------
                        st.markdown(
                            "<div class='tight-header step-header'><h3>📌 Step 4: Preview and Download Results</h3></div><hr/>",
                            unsafe_allow_html=True,
                        )
                        try:
                            render_manipulation_preview_section(
                                df, df_with_scores, reverse_columns, scale_points
                            )
                        except Exception as e:
                            logger.error(f"Data processing error: {str(e)}")
                            st.error("An error occurred while processing the data.")
                except Exception as e:
                    logger.error(f"Scale score calculation error: {str(e)}")
                    st.error("An error occurred while calculating scale scores.")

        except Exception as e:
            logger.error(f"Step 2 configuration error: {str(e)}")
            st.error("An error occurred in Step 2 configuration.")

except Exception as e:
    logger.error(f"Application error: {str(e)}")
    st.error("An unexpected error occurred.")
