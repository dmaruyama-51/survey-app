import streamlit as st

st.title("Survey Data Cleaning App")

st.markdown("""
## 🎯 Overview
A user-friendly web application designed to streamline the preprocessing of survey data collected using Likert scales. 
Whether you're a researcher or data analyst, this tool helps you clean and transform your survey data with ease.

## 📊 Available Features

### Data Cleaning Page
Clean your raw survey data with our comprehensive cleaning tools:
""")

# Data Cleaning Features Table
cleaning_data = {
    "Feature": ["🔍 Straight-Line Response Detection", "❌ Missing Value Handling", 
                "📏 Out-of-Range Value Filtering", "📈 Sequential Pattern Detection"],
    "Description": [
        "Identifies and removes responses where participants selected the same value for all questions",
        "Removes rows containing missing values",
        "Removes responses outside the valid Likert scale range (e.g., -1 or 100 in a 5-point scale)",
        "Identifies and removes responses with sequential patterns (e.g., 1,2,3,4,5...)"
    ],
    "Benefits": [
        "Helps eliminate potentially unreliable data",
        "Ensures data completeness for analysis",
        "Maintains data quality within scale bounds",
        "Helps identify potentially non-genuine responses"
    ]
}

st.table(cleaning_data)

st.markdown("""
### Data Manipulation Page
Transform your cleaned data with these helpful features:
""")

# Data Manipulation Features Table
manipulation_data = {
    "Feature": ["🔄 Reverse Item Creation", "➗ Scale Statistics"],
    "Description": [
        "Easily create reverse-scored items",
        "Calculate scale totals and means"
    ],
    "Benefits": [
        "Maintain consistency in your scale directions",
        "Streamline your data aggregation process"
    ]
}

st.table(manipulation_data)

st.markdown("""
## 🔗 Source Code
Interested in the implementation? Check out our [GitHub repository](https://github.com/dmaruyama-51/survey-app/tree/main)
""")