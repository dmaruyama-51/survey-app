import streamlit as st
import pandas as pd
from typing import List


# pragma: no cover
def process_data_cleaning_and_export(
    df_to_process: pd.DataFrame, 
    df_not_to_process: pd.DataFrame,
    likert_scale_case: int
) -> pd.DataFrame:
    """
    データクリーニングの要件を選択し、クリーニング後のデータをダウンロード可能にする
    Args:
        df (pd.DataFrame): 入力データフレーム
        likert_scale_case (int): リッカート尺度のポイント数
    Returns:
        pd.DataFrame: クリーニング済みのデータフレーム
    """
    st.markdown("#### Select data cleaning requirements")
    req1 = st.checkbox("Remove straight lines")
    req2 = st.checkbox("Remove rows with missing values")
    req3 = st.checkbox("Remove rows with maximum or minimum value exceeds the default")

    remove_rows = remove_invalid_responses(df_to_process, req1, req2, req3)
    all_df = pd.concat([df_not_to_process, df_to_process], axis=1)
    cleaned_df = all_df.drop(index=remove_rows)
    removed_df = all_df.loc[remove_rows]

    if not cleaned_df.empty and (req1 or req2 or req3):
        st.markdown("#### Download cleaned data")
        st.write(f"Process Completed. {len(remove_rows)} rows were removed.")
        st.write(removed_df)
        
        csv = cleaned_df.to_csv(index=False)
        st.download_button(
            label="Download cleaned data",
            data=csv,
            file_name="cleaned_survey_data.csv",
            mime="text/csv",
        )
    return cleaned_df


# pragma: no cover
def remove_invalid_responses(
    df: pd.DataFrame, req1: bool, req2: bool, req3: bool
) -> List[int]:
    """
    指定された要件に基づいて無効な回答の行番号を取得
    Args:
        df (pd.DataFrame): 入力データフレーム
        req1 (bool): ストレートライン回答を削除するかどうか
        req2 (bool): 欠損値を含む行を削除するかどうか
        req3 (bool): 規定値を超える行を削除するかどうか
    Returns:
        List[int]: 削除対象の行インデックスのリスト
    """
    try:
        remove_rows: List[int] = []
        if req1:
            req1_remove_rows = remove_straight_line_responses(df)
            remove_rows.extend(req1_remove_rows)

        return remove_rows
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        return []


def remove_straight_line_responses(df: pd.DataFrame) -> List[int]:
    """
    ストレートライン回答（全て同じ値の回答）の行番号を取得
    Args:
        df (pd.DataFrame): 入力データフレーム
    Returns:
        List[int]: ストレートライン回答の行番号のリスト
    """
    straight_line_rows = df.std(axis=1) == 0
    remove_rows = straight_line_rows[straight_line_rows].index.tolist()
    if remove_rows:  # リストが空でない場合のみ表示
        st.write("以下の行番号にストレートライン回答が見つかりました:")
        st.write(remove_rows)
    return remove_rows
