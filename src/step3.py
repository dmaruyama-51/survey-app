import streamlit as st
import pandas as pd


# pragma: no cover
def process_data_cleaning_and_export(
    df: pd.DataFrame, likert_scale_case: int
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
    cleaned_df = remove_invalid_responses(df, req1, req2, req3)

    if not cleaned_df.empty and (req1 or req2 or req3):
        st.markdown("#### Download cleaned data")
        st.write("Here is the cleaned data")
        csv = cleaned_df.to_csv(index=False)
        st.write(cleaned_df)
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
) -> pd.DataFrame:
    """
    指定された要件に基づいて無効な回答を削除する
    Args:
        df (pd.DataFrame): 入力データフレーム
        req1 (bool): ストレートライン回答を削除するかどうか
        req2 (bool): 欠損値を含む行を削除するかどうか
        req3 (bool): 規定値を超える行を削除するかどうか
    Returns:
        pd.DataFrame: クリーニング済みのデータフレーム
    """
    try:
        if req1:
            df = remove_straight_line_responses(df)
        return df
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        return pd.DataFrame()


def remove_straight_line_responses(df: pd.DataFrame) -> pd.DataFrame:
    """
    ストレートライン回答（全て同じ値の回答）を削除する
    Args:
        df (pd.DataFrame): 入力データフレーム
    Returns:
        pd.DataFrame: ストレートライン回答を削除したデータフレーム
    """
    straight_line_rows = df.std(axis=1) == 0
    if straight_line_rows.any():
        remove_rows = straight_line_rows[straight_line_rows].index.tolist()
        st.write("以下の行番号にストレートライン回答が見つかりました:")
        st.write(remove_rows)
        df = df.drop(index=remove_rows)
    return df
