# pragma: no cover
import streamlit as st
import pandas as pd

st.title("Survey Cleaning App")
st.write("This app is used to clean survey data")


st.markdown("## Step1. upload the survey data")
uploaded_file = st.file_uploader("Please upload the survey data", type=["csv"])

if uploaded_file is not None:
    st.write("Here is the uploaded data")
    df = pd.read_csv(uploaded_file)
else:
    st.write("No file uploaded. Using sample data.")
    df = pd.read_csv("src/data/sample.csv")

st.write(df)
# end pragma: no cover
