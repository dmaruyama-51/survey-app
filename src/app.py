# pragma: no cover
import streamlit as st
from src.step1 import load_survey_data, display_data_summary
from src.step2 import select_non_numeric_columns, select_likert_scale_points
from src.step3 import process_data_cleaning_and_export


def main():
    st.title("Survey Cleaning App")
    st.write("This app is used to clean survey data")

    # -----------------------------------
    # Step1. upload the survey data
    # -----------------------------------
    st.markdown("### Step1. upload the survey data")
    df = load_survey_data()
    if df is not None:
        display_data_summary(df)

        # -----------------------------------
        # Step2. Enter the data information
        # -----------------------------------
        st.markdown("### Step2. Enter the data information")
        _df = select_non_numeric_columns(df)
        likert_scale_case = select_likert_scale_points()
        st.write(likert_scale_case)

        is_all_numerical = (
            _df.select_dtypes(include=["number"]).shape[1] == _df.shape[1]
        )
        if not is_all_numerical:
            st.write("数値以外のカラムが含まれています。")
            st.stop()

        if is_all_numerical and likert_scale_case is not None:
            # -----------------------------------
            # Step3. Select data cleaning requirements and download
            # -----------------------------------
            st.markdown("### Step3. Select data cleaning requirements and download")
            process_data_cleaning_and_export(_df, likert_scale_case)


if __name__ == "__main__":
    main()

# end pragma: no cover
