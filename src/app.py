# pragma: no cover
import streamlit as st
from src.interface.sections.step1 import render_file_upload_section
from src.interface.sections.step2 import render_data_settings_section
from src.interface.sections.step3 import process_data_cleaning_and_export
from src.interface.components.data_summary import display_data_summary
from src.interface.state import check_step2_completion
from src.utils.logger_config import logger


def main():
    try:
        logger.info("Application started")
        st.title("Survey Data Cleaning App")
        st.markdown("Clean and process your survey data with ease")

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
                return
        except Exception as e:
            logger.error(f"Data loading error: {str(e)}")
            st.error("Failed to load data. Please check your file.")
            return

        # -----------------------------------
        # Step2. Configure Data Settings
        # -----------------------------------
        st.markdown(
            "<div class='tight-header step-header'><h3>📌 Step 2: Configure Data Settings</h3></div><hr/>",
            unsafe_allow_html=True,
        )
        try:
            df_to_process, df_not_to_process, likert_scale = (
                render_data_settings_section(df)
            )

            # step2の要件が満たされているかチェック
            step2_completed = check_step2_completion(
                remove_cols=df_not_to_process.columns.tolist(),
                likert_scale=likert_scale,
            )

            # -----------------------------------
            # Step3. Clean Data and Download Results
            # -----------------------------------
            if step2_completed:
                st.markdown(
                    "<div class='tight-header step-header'><h3>📌 Step 3: Clean Data and Download Results</h3></div><hr/>",
                    unsafe_allow_html=True,
                )
                try:
                    logger.info("Starting data cleaning process")
                    process_data_cleaning_and_export(
                        df_to_process, df_not_to_process, likert_scale
                    )
                    logger.info("Data cleaning completed")
                except Exception as e:
                    logger.error(f"Data cleaning error: {str(e)}")
                    st.error("An error occurred during data cleaning.")
                    return
        except Exception as e:
            logger.error(f"Step 2 configuration error: {str(e)}")
            st.error("An error occurred in Step 2 configuration.")
            return

    except Exception as e:
        logger.error(f"System error: {str(e)}")
        st.error("An application error occurred.")


if __name__ == "__main__":
    main()

# end pragma: no cover
