from typing import Tuple

import pandas as pd
import streamlit as st

from src.interface.components.display import disaply_final_dataset
from src.interface.components.input import (
    input_cleaning_options,
    input_column_selection,
    input_keep_records,
    input_likert_scale_selection,
)
from src.interface.state import (
    initialize_cleaning_state,
    reset_cleaning_state,
)
from src.utils.logger_config import logger


def render_data_settings_section(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, int, str]:
    """データ設定セクションを表示"""
    try:
        # カラム選択
        df_to_process, df_not_to_process, exclude_option = input_column_selection(df)

        # リッカート尺度の選択
        likert_scale = input_likert_scale_selection()

        return df_to_process, df_not_to_process, likert_scale, exclude_option

    except Exception as e:
        logger.error(f"Data settings error: {str(e)}")
        st.error("An error occurred while configuring data settings.")
        raise


def render_process_data_cleaning_and_export_section(
    df_to_process: pd.DataFrame, df_not_to_process: pd.DataFrame, likert_scale_case: int
) -> pd.DataFrame:
    """データクリーニングの実行とエクスポート処理"""
    try:
        cleaning_reqs = input_cleaning_options()

        if "cleaning_executed" not in st.session_state:
            st.session_state.cleaning_executed = False

        start_cleaning = st.button("Start Data Cleaning")

        if start_cleaning or st.session_state.cleaning_executed:
            st.session_state.cleaning_executed = True

            if not any(cleaning_reqs):
                st.warning("Please select at least one cleaning option.")
                return df_to_process

            logger.info(
                f"Selected cleaning options: straight_lines={cleaning_reqs[0]}, "
                f"missing={cleaning_reqs[1]}, out_of_range={cleaning_reqs[2]}, "
                f"step_pattern={cleaning_reqs[3]}"
            )

            if "cleaned_df" not in st.session_state:
                initialize_cleaning_state(
                    df_to_process, df_not_to_process, likert_scale_case, cleaning_reqs
                )

            if not st.session_state.cleaned_df.empty:
                st.markdown("#### Results and Download")

                st.write("The following rows have been detected.")
                st.dataframe(
                    st.session_state.removed_df.loc[:, df_to_process.columns],
                    use_container_width=True,
                )

                st.write(
                    "If there are any rows you don't want to delete, please check the rows you wish to keep."
                    "If no rows are selected, the downloaded data will exclude all records shown here."
                )

                rows_to_keep = input_keep_records()
                final_cleaned_df = disaply_final_dataset(rows_to_keep)

                # 元のアップロードされたデータのカラム順序を取得
                if (
                    "uploaded_df" in st.session_state
                    and st.session_state.uploaded_df is not None
                ):
                    original_columns = st.session_state.uploaded_df.columns.tolist()

                    # final_cleaned_dfのカラムが元のカラムと一致するか確認
                    if set(original_columns) == set(final_cleaned_df.columns):
                        # カラム順序を元の順序に合わせる
                        final_cleaned_df = final_cleaned_df[original_columns]
                    else:
                        # カラムが一致しない場合はログに記録
                        logger.warning(
                            "Column mismatch between original and cleaned data"
                        )

                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("Reset Cleaning Process"):
                        reset_cleaning_state()
                        st.rerun()
                with col2:
                    csv = final_cleaned_df.to_csv(index=False)
                    st.download_button(
                        label="Download Cleaned Data",
                        data=csv,
                        file_name="cleaned_survey_data.csv",
                        mime="text/csv",
                        type="primary",
                    )
                return final_cleaned_df
            else:
                st.warning(
                    "All rows have been removed. No data is available for download."
                )

        return df_to_process

    except Exception as e:
        logger.error(f"Data cleaning error: {str(e)}")
        raise
