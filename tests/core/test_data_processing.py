import pandas as pd
from src.core.data_processing import split_dataframe, create_final_dataset


def test_split_dataframe_basic():
    """基本的なデータフレーム分割のテスト"""
    df = pd.DataFrame({"ID": ["1", "2"], "Q1": [1, 2], "Q2": [3, 4]})
    exclude_cols = ["ID"]

    df_process, df_exclude = split_dataframe(df, exclude_cols)

    assert list(df_process.columns) == ["Q1", "Q2"]
    assert list(df_exclude.columns) == ["ID"]


def test_create_final_dataset_basic():
    """基本的な最終データセット作成のテスト"""
    cleaned_df = pd.DataFrame({"Q1": [1, 2], "Q2": [3, 4]})
    removed_df = pd.DataFrame({"Q1": [5], "Q2": [6]})

    # 行を復元しない場合
    result = create_final_dataset(cleaned_df, removed_df, [])
    assert len(result) == 2

    # 行を復元する場合
    result = create_final_dataset(cleaned_df, removed_df, [0])
    assert len(result) == 3
