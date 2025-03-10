import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from src.interface.pages.common import render_file_upload_section
from src.interface.state import check_file_upload_completion, check_visualization_selection_completion
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
        
        # 数値型カラムのみを抽出
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_columns:
            st.warning("No numeric columns found in the data. Visualization requires numeric data.")
        else:
            # 選択オプションを追加
            selection_options = [
                "Select individual columns",
                "Select all columns"
            ]
            
            selection_mode = st.radio(
                "How would you like to select columns?",
                options=selection_options,
                horizontal=True
            )
            
            selected_columns = []
            
            if selection_mode == "Select individual columns":
                # 従来の複数選択UI
                selected_columns = st.multiselect(
                    "Select columns to visualize",
                    options=numeric_columns,
                    default=numeric_columns[:2] if len(numeric_columns) >= 2 else numeric_columns,
                    help="Select one or more columns to create visualizations"
                )
                
            elif selection_mode == "Select all columns":
                # すべての数値カラムを選択
                selected_columns = numeric_columns
                st.success(f"All {len(numeric_columns)} numeric columns selected")
                
                # 必要に応じて除外するカラムを選択できるオプション
                exclude_columns = st.multiselect(
                    "Exclude columns (optional)",
                    options=numeric_columns,
                    default=[],
                    help="Select columns you want to exclude from visualization"
                )
                
                if exclude_columns:
                    selected_columns = [col for col in numeric_columns if col not in exclude_columns]
                    st.info(f"{len(selected_columns)} columns selected after exclusion")
            
            # 選択されたカラムの数を表示
            if selected_columns:
                st.session_state.selected_viz_columns = selected_columns
                
                # 選択カラム数の表示
                st.write(f"Selected {len(selected_columns)} columns for visualization")
            
            if check_visualization_selection_completion(selected_columns):
                # -----------------------------------
                # Step3. Data Visualization
                # -----------------------------------
                st.markdown(
                    "<div class='tight-header step-header'><h3>📌 Step 3: Data Visualization</h3></div><hr/>",
                    unsafe_allow_html=True,
                )
                
                # 可視化ボタン
                if st.button("Visualize Data", type="primary"):
                    # 統計情報のサマリテーブルを作成
                    st.markdown("#### Statistical Summary")
                    
                    # 統計情報を格納するデータフレームを作成
                    stats_data = []
                    
                    for col in selected_columns:
                        mean_val = df[col].mean()
                        std_val = df[col].std()
                        min_val = df[col].min()
                        max_val = df[col].max()
                        
                        # 天井効果と床効果の判定
                        ceiling_effect = (mean_val + std_val) > max_val
                        floor_effect = (mean_val - std_val) < min_val
                        
                        # 効果の表示用テキスト
                        ceiling_text = "⚠️ Yes" if ceiling_effect else "No"
                        floor_text = "⚠️ Yes" if floor_effect else "No"
                        
                        # データを追加
                        stats_data.append({
                            "Variable": col,
                            "Mean": f"{mean_val:.2f}",
                            "SD": f"{std_val:.2f}",
                            "Min": f"{min_val:.2f}",
                            "Max": f"{max_val:.2f}",
                            "Mean+SD": f"{(mean_val+std_val):.2f}",
                            "Mean-SD": f"{(mean_val-std_val):.2f}",
                            "Ceiling Effect": ceiling_text,
                            "Floor Effect": floor_text
                        })
                    
                    # データフレームに変換
                    stats_df = pd.DataFrame(stats_data)
                    
                    # サマリテーブルを表示
                    st.dataframe(stats_df, use_container_width=True, hide_index=True)
                    
                    # 効果の説明
                    with st.expander("What are Ceiling and Floor Effects?"):
                        st.markdown("""
                        **Ceiling Effect**: Occurs when a measure has a distinct upper limit for potential responses and a large concentration of participants score at or near this limit. Statistically detected when Mean + SD > Maximum value.
                        
                        **Floor Effect**: Occurs when a measure has a distinct lower limit for potential responses and a large concentration of participants score at or near this limit. Statistically detected when Mean - SD < Minimum value.
                        
                        These effects can limit the ability to distinguish between participants at the extremes and may reduce the validity of the measure.
                        """)
                    
                    # 各選択カラムのヒストグラムを表示
                    st.markdown("#### Histograms")
                    
                    # 多数のカラムがある場合の警告
                    if len(selected_columns) > 10:
                        st.warning(f"You selected {len(selected_columns)} columns. Displaying histograms for the first 10 columns only.")
                        display_columns = selected_columns[:10]
                        
                        # 残りのカラムを表示するオプション
                        if st.checkbox("Show all selected columns"):
                            display_columns = selected_columns
                    else:
                        display_columns = selected_columns
                    
                    st.write(f"Displaying histograms for {len(display_columns)} columns:")
                    
                    # 選択されたカラムの数に応じてレイアウトを調整
                    if len(display_columns) == 1:
                        # 1つのカラムの場合は大きく表示
                        col = display_columns[0]
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
                        
                        # 統計情報を計算
                        mean_val = df[col].mean()
                        std_val = df[col].std()
                        min_val = df[col].min()
                        max_val = df[col].max()
                        
                        # 天井効果と床効果の判定
                        ceiling_effect = (mean_val + std_val) > max_val
                        floor_effect = (mean_val - std_val) < min_val
                        
                        # 統計情報と効果の表示
                        stats_md = f"**Statistics for {col}:**  \n"
                        stats_md += f"Mean: {mean_val:.2f}  \n"
                        stats_md += f"Standard Deviation: {std_val:.2f}  \n"
                        stats_md += f"Min: {min_val:.2f}, Max: {max_val:.2f}  \n"
                        
                        if ceiling_effect:
                            stats_md += f"⚠️ **Ceiling Effect Detected**: Mean + SD ({mean_val+std_val:.2f}) > Max ({max_val:.2f})  \n"
                        if floor_effect:
                            stats_md += f"⚠️ **Floor Effect Detected**: Mean - SD ({mean_val-std_val:.2f}) < Min ({min_val:.2f})  \n"
                        
                        st.markdown(stats_md)
                    else:
                        # 複数のカラムの場合は2列のグリッドで表示
                        cols = st.columns(2)
                        for i, col in enumerate(display_columns):
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
                                
                                # 統計情報を計算
                                mean_val = df[col].mean()
                                std_val = df[col].std()
                                min_val = df[col].min()
                                max_val = df[col].max()
                                
                                # 天井効果と床効果の判定
                                ceiling_effect = (mean_val + std_val) > max_val
                                floor_effect = (mean_val - std_val) < min_val
                                
                                # 統計情報と効果の表示
                                stats_md = f"**Statistics for {col}:**  \n"
                                stats_md += f"Mean: {mean_val:.2f}  \n"
                                stats_md += f"Standard Deviation: {std_val:.2f}  \n"
                                stats_md += f"Min: {min_val:.2f}, Max: {max_val:.2f}  \n"
                                
                                if ceiling_effect:
                                    stats_md += f"⚠️ **Ceiling Effect Detected**: Mean + SD ({mean_val+std_val:.2f}) > Max ({max_val:.2f})  \n"
                                if floor_effect:
                                    stats_md += f"⚠️ **Floor Effect Detected**: Mean - SD ({mean_val-std_val:.2f}) < Min ({min_val:.2f})  \n"
                                
                                st.markdown(stats_md)

except Exception as e:
    logger.error(f"Application error: {str(e)}")
    st.error("An unexpected error occurred.")
