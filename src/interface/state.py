import streamlit as st
import pandas as pd
from src.core.cleaning import remove_invalid_responses
from typing import List


def initialize_cleaning_state(
    df_to_process: pd.DataFrame,
    df_not_to_process: pd.DataFrame,
    likert_scale_case: int,
    reqs: tuple[bool, bool, bool, bool],
) -> None:
    """クリーニング処理の初期化と実行"""
    req1, req2, req3, req4 = reqs
    remove_rows = remove_invalid_responses(
        df_to_process, likert_scale_case, req1, req2, req3, req4
    )
    all_df = pd.concat([df_not_to_process, df_to_process], axis=1)
    st.session_state.cleaned_df = all_df.drop(index=remove_rows)
    st.session_state.removed_df = all_df.loc[remove_rows]


def check_data_settings_completion(
    remove_cols: list[str], likert_scale: int | None
) -> bool:
    """
    Step2の要件が満たされているかチェックする
    Args:
        remove_cols (list[str]): 除外するカラムのリスト
        likert_scale (int | None): 選択されたリッカート尺度のポイント数
    Returns:
        bool: 要件を満たしているかどうか
    """
    if not remove_cols and likert_scale is None:
        st.info(
            "Please start by selecting columns to exclude and configuring the Likert scale.",
            icon="ℹ️",
        )
        return False
    elif not remove_cols:
        st.info("Please select columns to exclude from numeric processing.", icon="ℹ️")
        return False
    elif likert_scale is None:
        st.info("Please select the number of Likert scale points.", icon="ℹ️")
        return False
    return True


def check_file_upload_completion(df: pd.DataFrame | None) -> bool:
    """
    Step1の要件が満たされているかチェックする
    Args:
        df (pd.DataFrame | None): アップロードされたデータフレーム
    Returns:
        bool: 要件を満たしているかどうか
    """
    if df is None:
        st.info("Please upload a CSV file or use sample data to proceed.", icon="ℹ️")
        return False
    return True


def reset_cleaning_state() -> None:
    """クリーニング関連の全セッション状態をリセット"""
    keys_to_remove = [
        "cleaning_executed",
        "cleaned_df",
        "removed_df",
        "removed_df_with_checkbox",
        "editor_key",
    ]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]


def check_manipulation_settings_completion(
    has_reverse_items: bool,
    reverse_columns: List[str] | None = None,
) -> bool:
    """
    Step2（逆転項目の設定）の要件が満たされているかチェック
    Args:
        has_reverse_items (bool): 逆転項目の有無
        reverse_columns (List[str] | None): 選択された逆転項目のリスト
    Returns:
        bool: 要件を満たしているかどうか
    """
    if has_reverse_items and not reverse_columns:
        st.info(
            "Please select at least one column to reverse-score.",
            icon="ℹ️",
        )
        return False
    return True


def check_scale_scores_completion(df: pd.DataFrame | None) -> bool:
    """
    Step3（因子得点の計算）の要件が満たされているかチェック
    Args:
        df (pd.DataFrame | None): 因子得点が計算されたデータフレーム
    Returns:
        bool: 要件を満たしているかどうか
    """
    if df is None:
        st.info(
            "Please configure at least one scale to calculate scores.",
            icon="ℹ️",
        )
        return False

    # 因子得点が計算されているかチェック
    score_columns = [col for col in df.columns if col.endswith(("_total", "_mean"))]
    if not score_columns:
        st.info(
            "Please configure at least one scale to calculate scores.",
            icon="ℹ️",
        )
        return False
    return True
