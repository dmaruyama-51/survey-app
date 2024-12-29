# pragma: no cover
import streamlit as st
from src.step1 import load_survey_data, display_data_summary
from src.step2 import split_numeric_and_non_numeric_columns, select_likert_scale_points
from src.step3 import process_data_cleaning_and_export
from src.utils.logger_config import logger


def main():
    try:
        logger.info("アプリケーション開始")
        st.title("Survey Data Cleaning Tool")
        st.write("Clean and process your survey data with ease")

        # -----------------------------------
        # Step1. upload the survey data
        # -----------------------------------
        st.markdown("### Step 1: Upload Survey Data")
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
        st.markdown("### Step 2: Configure Data Settings")
        try:
            df_to_process, df_not_to_process = split_numeric_and_non_numeric_columns(df)
            likert_scale_case = select_likert_scale_points()
            logger.info(f"リッカート尺度選択: {likert_scale_case}")

            is_all_numerical = (
                df_to_process.select_dtypes(include=["number"]).shape[1]
                == df_to_process.shape[1]
            )
            if not is_all_numerical:
                logger.error("非数値カラムを検出")
                st.error("数値以外のカラムが含まれています。")
                return
        except Exception as e:
            logger.error(f"データ処理エラー: {str(e)}")
            st.error("データの処理中にエラーが発生しました。")
            return

        if is_all_numerical and likert_scale_case is not None:
            # -----------------------------------
            # Step3. Select data cleaning requirements and download
            # -----------------------------------
            st.markdown("### Step 3: Clean Data and Download Results")
            try:
                logger.info("クリーニング開始")
                process_data_cleaning_and_export(
                    df_to_process, df_not_to_process, likert_scale_case
                )
                logger.info("クリーニング完了")
            except Exception as e:
                logger.error(f"クリーニングエラー: {str(e)}")
                st.error("データのクリーニング中にエラーが発生しました。")
                return

    except Exception as e:
        logger.error(f"システムエラー: {str(e)}")
        st.error("アプリケーションでエラーが発生しました。")


if __name__ == "__main__":
    main()

# end pragma: no cover
