import streamlit as st
from src.interface.pages.common import render_file_upload_section
from src.interface.state import check_file_upload_completion
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
        
        st.markdown(
            "<div class='tight-header'><h4>Column Selection</h4></div>",
            unsafe_allow_html=True,
        )
        st.write(
            "Select columns you want to visualize. You can select multiple columns for comparison."
        )
        
        # 数値型カラムのみを抽出
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_columns:
            st.warning("No numeric columns found in the data. Visualization requires numeric data.")
        else:
            # 複数選択可能なカラム選択UI
            selected_columns = st.multiselect(
                "Select columns to visualize",
                options=numeric_columns,
                default=numeric_columns[:2] if len(numeric_columns) >= 2 else numeric_columns,
                help="Select one or more columns to create visualizations"
            )
            
            if selected_columns:
                st.session_state.selected_viz_columns = selected_columns
                st.success(f"Selected {len(selected_columns)} columns for visualization")
            else:
                st.info("Please select at least one column to visualize", icon="ℹ️")

except Exception as e:
    logger.error(f"Application error: {str(e)}")
    st.error("An unexpected error occurred.")
