# pragma: no cover
import streamlit as st
from src.step1 import load_survey_data, display_data_summary
from src.step2 import (
    split_numeric_and_non_numeric_columns,
    select_likert_scale_points,
    check_step2_completion,
)
from src.step3 import process_data_cleaning_and_export
from src.utils.logger_config import logger


def main():
    try:
        logger.info("アプリケーション開始")
        st.title("Survey Data Cleaning Tool")
        st.write("Clean and process your survey data with ease")

        # カスタムCSSを追加
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
        # Step1. upload the survey data
        # -----------------------------------
        st.markdown(
            "<div class='tight-header step1-header'><h3>📌 Step 1: Upload Survey Data</h3></div><hr/>",
            unsafe_allow_html=True,
        )
        try:
            df = load_survey_data()
            if df is not None:
                logger.info(f"データ読み込み完了 shape: {df.shape}")
                display_data_summary(df)
            else:
                logger.warning("データ未読み込み")
                return
        except Exception as e:
            logger.error(f"データ読み込みエラー: {str(e)}")
            st.error("データの読み込みに失敗しました。ファイルを確認してください。")
            return

        # -----------------------------------
        # Step2. Enter the data information
        # -----------------------------------
        st.markdown(
            "<div class='tight-header step-header'><h3>📌 Step 2: Configure Data Settings</h3></div><hr/>",
            unsafe_allow_html=True,
        )
        try:
            df_to_process, df_not_to_process = split_numeric_and_non_numeric_columns(df)
            likert_scale = select_likert_scale_points()

            # Step 2の完了チェック
            step2_completed = check_step2_completion(
                remove_cols=df_not_to_process.columns.tolist(),
                likert_scale=likert_scale,
            )

            # Step 2が完了している場合のみStep 3を表示
            if step2_completed:
                st.markdown(
                    "<div class='tight-header step-header'><h3>📌 Step 3: Clean Data and Download Results</h3></div><hr/>",
                    unsafe_allow_html=True,
                )
                try:
                    logger.info("クリーニング開始")
                    process_data_cleaning_and_export(
                        df_to_process, df_not_to_process, likert_scale
                    )
                    logger.info("クリーニング完了")
                except Exception as e:
                    logger.error(f"クリーニングエラー: {str(e)}")
                    st.error("データのクリーニング中にエラーが発生しました。")
                    return
        except Exception as e:
            logger.error(f"Step 2エラー: {str(e)}")
            st.error("Step 2の設定にエラーが発生しました。")
            return

    except Exception as e:
        logger.error(f"システムエラー: {str(e)}")
        st.error("アプリケーションでエラーが発生しました。")


if __name__ == "__main__":
    main()

# end pragma: no cover
