import streamlit as st

# Add custom CSS for headers
st.markdown(
    """
    <style>
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

st.title("Survey Data Preprocessing App")

st.markdown("""
A user-friendly web application designed to streamline the preprocessing of survey data collected using Likert scales. 
Whether you're a researcher or data analyst, this tool helps you clean and transform your survey data with ease.
""")

st.markdown(
    "<div class='tight-header'><h2>📊 Available Features</h2></div><hr/>",
    unsafe_allow_html=True,
)

st.markdown(
    "### Data Cleaning",
    unsafe_allow_html=True,
)
st.markdown("Clean your raw survey data with our comprehensive cleaning tools:")

# Data Cleaning Features Table
cleaning_data = {
    "Feature": ["Straight-Line Response Detection", "Missing Value Handling", 
                "Out-of-Range Value Filtering", "Sequential Pattern Detection"],
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

st.markdown(
    "### Data Manipulation",
    unsafe_allow_html=True,
)
st.markdown("Transform your cleaned data with these helpful features:")

# Data Manipulation Features Table
manipulation_data = {
    "Feature": ["Reverse Item Creation", "Scale Statistics"],
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

# Add call-to-action buttons
st.markdown(
    "<div class='tight-header'><h2>🚀 Get Started</h2></div><hr/>",
    unsafe_allow_html=True,
)
col1, col2 = st.columns(2)

with col1:
    st.info("Ready to clean your data? Go to the **Data Cleaning** page from the sidebar.", icon="🧹")

with col2:
    st.info("Need to manipulate your data? Select **Data Manipulation** from the sidebar.", icon="🔧")

st.markdown(
    "<div class='tight-header'><h2>🔗 Source Code</h2></div><hr/>",
    unsafe_allow_html=True,
)
st.markdown("Interested in the implementation? Check out our [GitHub repository](https://github.com/dmaruyama-51/survey-app/tree/main)")