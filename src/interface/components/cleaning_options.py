import streamlit as st
import pandas as pd
from typing import Tuple, List
from src.core.dataframe_operation import create_final_dataset


def render_cleaning_options() -> Tuple[bool, bool, bool, bool]:
    """データクリーニングのオプションを表示し、選択状態を返す"""
    st.markdown("#### Data Cleaning Options")
    req1 = st.checkbox("Remove straight-line responses")
    req2 = st.checkbox("Remove responses with missing values")
    req3 = st.checkbox("Remove responses outside of valid range")
    req4 = st.checkbox("Remove step pattern responses")
    return req1, req2, req3, req4


def render_removed_records_editor() -> List[int]:
    """削除されたレコードの編集UIを表示"""
    if "removed_df_with_checkbox" not in st.session_state:
        st.session_state.removed_df_with_checkbox = st.session_state.removed_df.copy()
        st.session_state.removed_df_with_checkbox.insert(0, "Keep This Row", False)
        st.session_state.editor_key = 0

    edited_df = st.data_editor(
        st.session_state.removed_df_with_checkbox,
        hide_index=True,
        column_config={
            "Keep This Row": st.column_config.CheckboxColumn(
                "Keep This Row",
                help="Select to keep this row in the final dataset",
                default=False,
            )
        },
        key=f"removed_records_editor_{st.session_state.editor_key}",
    )

    if not edited_df.equals(st.session_state.removed_df_with_checkbox):
        st.session_state.removed_df_with_checkbox = edited_df.copy()
        st.session_state.editor_key += 1
        st.rerun()

    return st.session_state.removed_df_with_checkbox[
        st.session_state.removed_df_with_checkbox["Keep This Row"]
    ].index.tolist()


def render_final_dataset(rows_to_keep: list) -> pd.DataFrame:
    """最終的なデータセットを作成してUIに表示"""
    final_cleaned_df = create_final_dataset(
        st.session_state.cleaned_df, st.session_state.removed_df, rows_to_keep
    )

    if rows_to_keep:
        st.write(
            f"Final dataset will keep {len(rows_to_keep)} previously removed rows."
        )

    return final_cleaned_df
