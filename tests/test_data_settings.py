import pandas as pd
from src.core.dataframe_operation import split_dataframe


def test_split_dataframe():
    """データフレーム分割機能のテスト"""
    # テストデータの作成
    test_data = {
        "ID": ["001", "002", "003"],
        "Q1": [1, 2, 3],
        "Q2": [4, 5, 6],
        "Category": ["A", "B", "C"],
    }
    df = pd.DataFrame(test_data)

    # テスト実行
    exclude_columns = ["ID", "Category"]
    df_to_process, df_not_to_process = split_dataframe(df, exclude_columns)

    # 検証
    assert list(df_to_process.columns) == ["Q1", "Q2"]
    assert list(df_not_to_process.columns) == ["ID", "Category"]
    assert df_to_process.shape[0] == 3
    assert df_not_to_process.shape[0] == 3
