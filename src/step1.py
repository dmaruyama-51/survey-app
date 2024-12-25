# pragma: no cover
import streamlit as st
import pandas as pd


# pragma: no cover
def load_survey_data() -> pd.DataFrame | None:
    """
    CSVファイルをアップロードまたはサンプルデータを読み込む
    Returns:
        pd.DataFrame | None: 読み込んだデータフレーム、またはNone
    """
    uploaded_file = st.file_uploader("Please upload the survey data", type=["csv"])

    is_use_sample_data = st.checkbox("Use sample data")
    if is_use_sample_data:
        st.write("Using sample data.")
        df = pd.read_csv("src/data/sample.csv")
    elif uploaded_file is not None:
        st.write("Using uploaded data")
        df = pd.read_csv(uploaded_file)
    else:
        st.write("No file uploaded")
        df = None
    return df

# pragma: no cover
def display_data_summary(df: pd.DataFrame) -> None:
    """
    アップロードされたデータのプレビューと基本統計量を表示
    Args:
        df (pd.DataFrame): 表示するデータフレーム
    """
    st.markdown("#### preview uploaded data")
    st.write(df)
    st.markdown("#### basic statistics")
    st.write(df.describe())
