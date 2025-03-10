import streamlit as st
import plotly.express as px
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
                
                # 可視化ボタン
                if st.button("Visualize Data", type="primary"):
                    # -----------------------------------
                    # Step3. Data Visualization
                    # -----------------------------------
                    st.markdown(
                        "<div class='tight-header step-header'><h3>📌 Step 3: Data Visualization</h3></div><hr/>",
                        unsafe_allow_html=True,
                    )
                    
                    # 各選択カラムのヒストグラムを表示
                    st.markdown("#### Histograms")
                    st.write("Distribution of selected variables:")
                    
                    # 選択されたカラムの数に応じてレイアウトを調整
                    if len(selected_columns) == 1:
                        # 1つのカラムの場合は大きく表示
                        col = selected_columns[0]
                        fig = px.histogram(
                            df, 
                            x=col,
                            title=f"Distribution of {col}",
                            labels={col: col},
                            color_discrete_sequence=['#3366CC'],
                            opacity=0.7
                        )
                        fig.update_layout(
                            xaxis_title=col,
                            yaxis_title="Frequency",
                            bargap=0.1,
                            height=500
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        # 複数のカラムの場合は2列のグリッドで表示
                        cols = st.columns(2)
                        for i, col in enumerate(selected_columns):
                            with cols[i % 2]:
                                fig = px.histogram(
                                    df, 
                                    x=col,
                                    title=f"Distribution of {col}",
                                    labels={col: col},
                                    color_discrete_sequence=['#3366CC'],
                                    opacity=0.7
                                )
                                fig.update_layout(
                                    xaxis_title=col,
                                    yaxis_title="Frequency",
                                    bargap=0.1,
                                    height=350
                                )
                                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Please select at least one column to visualize", icon="ℹ️")

except Exception as e:
    logger.error(f"Application error: {str(e)}")
    st.error("An unexpected error occurred.")
