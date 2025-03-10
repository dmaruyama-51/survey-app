import streamlit as st
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
    st.info("This page is under construction. Visualization features will be available soon.")

except Exception as e:
    logger.error(f"Application error: {str(e)}")
    st.error("An unexpected error occurred.")
