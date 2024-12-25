import pandas as pd
from src.step3 import (
    remove_straight_line_responses,
    remove_missing_values,
    remove_out_of_range_values,
)


def test_remove_straight_line_responses():
    """ストレートライン回答の削除をテスト"""
    # テストデータの作成
    test_data = {"Q1": [1, 1, 2, 3], "Q2": [1, 1, 3, 4], "Q3": [1, 1, 4, 5]}
    df = pd.DataFrame(test_data)
    remove_rows = remove_straight_line_responses(df)

    # 検証
    assert (
        len(remove_rows) == 2
    )  # ストレートライン回答（1, 2行目）が1つ検出されることを確認
    assert remove_rows == [0, 1]  # 削除対象の行インデックスが正しいことを確認


def test_remove_straight_line_responses_no_straight_lines():
    """ストレートライン回答が存在しない場合のテスト"""
    # テストデータの作成（ストレートライン回答なし）
    test_data = {"Q1": [1, 2, 3], "Q2": [2, 3, 4], "Q3": [3, 4, 5]}
    df = pd.DataFrame(test_data)
    remove_rows = remove_straight_line_responses(df)

    # 検証
    assert len(remove_rows) == 0  # ストレートライン回答が検出されないことを確認


def test_remove_missing_values():
    """欠損値を含む行の検出をテスト"""
    # テストデータの作成（欠損値を含むデータ）
    test_data = {"Q1": [1, None, 3, 4], "Q2": [1, 2, None, 4], "Q3": [1, 2, 3, 4]}
    df = pd.DataFrame(test_data)
    remove_rows = remove_missing_values(df)

    # 検証
    assert len(remove_rows) == 2  # 欠損値を含む行が2つ検出されることを確認
    assert sorted(remove_rows) == [1, 2]  # 削除対象の行インデックスが正しいことを確認


def test_remove_missing_values_no_missing():
    """欠損値が存在しない場合のテスト"""
    # テストデータの作成（欠損値なし）
    test_data = {"Q1": [1, 2, 3, 4], "Q2": [1, 2, 3, 4], "Q3": [1, 2, 3, 4]}
    df = pd.DataFrame(test_data)
    remove_rows = remove_missing_values(df)

    # 検証
    assert len(remove_rows) == 0  # 欠損値を含む行が検出されないことを確認


def test_remove_out_of_range_values():
    """規定値を超える行の検出をテスト"""
    # テストデータの作成（5段階のリッカート尺度を想定）
    test_data = {
        "Q1": [1, 6, 3, 0],  # 正常、超過、正常、未満
        "Q2": [2, 4, 3, 1],  # すべて正常
        "Q3": [3, 5, 7, 2],  # 正常、正常、超過、正常
    }
    df = pd.DataFrame(test_data)
    likert_scale_case = 5
    remove_rows = remove_out_of_range_values(df, likert_scale_case)

    # 検証
    assert len(remove_rows) == 3  # 範囲外の値を含む行が3つ検出されることを確認
    assert sorted(remove_rows) == [
        1,
        2,
        3,
    ]  # 削除対象の行インデックスが正しいことを確認


def test_remove_out_of_range_values_no_invalid():
    """規定値を超える値が存在しない場合のテスト"""
    # テストデータの作成（すべて範囲内の値）
    test_data = {"Q1": [1, 2, 3], "Q2": [2, 3, 4], "Q3": [3, 4, 5]}
    df = pd.DataFrame(test_data)
    likert_scale_case = 5
    remove_rows = remove_out_of_range_values(df, likert_scale_case)

    # 検証
    assert len(remove_rows) == 0  # 範囲外の値を含む行が検出されないことを確認
