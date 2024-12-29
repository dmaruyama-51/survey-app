import pandas as pd
from src.core.cleaning import (
    remove_straight_line_responses,
    remove_missing_values,
    remove_out_of_range_values,
    remove_invalid_responses,
)


def test_remove_straight_line_responses():
    """ストレートライン回答の削除をテスト"""
    # テストデータの作成
    test_data = {"Q1": [1, 1, 2, 3], "Q2": [1, 1, 3, 4], "Q3": [1, 1, 4, 5]}
    df = pd.DataFrame(test_data)
    remove_rows = remove_straight_line_responses(df)

    # 検証
    assert len(remove_rows) == 2
    assert remove_rows == [0, 1] 


def test_remove_missing_values():
    """欠損値を含む行の検出をテスト"""
    # テストデータの作成（欠損値を含むデータ）
    test_data = {"Q1": [1, None, 3, 4], "Q2": [1, 2, None, 4], "Q3": [1, 2, 3, 4]}
    df = pd.DataFrame(test_data)
    remove_rows = remove_missing_values(df)

    # 検証
    assert len(remove_rows) == 2  
    assert sorted(remove_rows) == [1, 2]


def test_remove_out_of_range_values():
    """範囲外の値を含む行の検出をテスト"""
    # テストデータの作成（7段階のリッカート尺度を想定）
    test_data = {"Q1": [1, 8, 3, 0], "Q2": [1, 2, 3, 4], "Q3": [1, 2, 3, 4]}
    df = pd.DataFrame(test_data)
    remove_rows = remove_out_of_range_values(df, likert_scale_case=7)

    # 検証
    assert len(remove_rows) == 2
    assert sorted(remove_rows) == [1, 3]


def test_remove_invalid_responses():
    """無効な回答の検出をテスト（複数の条件を組み合わせた場合）"""
    # テストデータの作成
    test_data = {
        "Q1": [1, 1, None, 8],  # 行1: ストレートライン, 行2: 欠損値, 行3: 範囲外
        "Q2": [1, 2, None, 4],
        "Q3": [1, 2, 3, 4],
    }
    df = pd.DataFrame(test_data)
    remove_rows = remove_invalid_responses(
        df,
        likert_scale=7,
        remove_straight_lines=True,
        remove_missing=True,
        remove_out_of_range=True,
    )

    # 検証
    assert len(remove_rows) == 3  
    assert sorted(remove_rows) == [
        0,
        2,
        3,
    ] 