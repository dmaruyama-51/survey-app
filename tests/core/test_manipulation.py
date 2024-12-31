import pandas as pd
from src.core.manipulation import reverse_score, prepare_download_data


def test_reverse_score():
    """逆転項目のスコアリングテスト"""
    # テストデータの作成
    test_data = {"Q1": [1, 2, 3, 4, 5], "Q2": [2, 3, 4, 5, 1], "Q3": [3, 4, 5, 1, 2]}
    df = pd.DataFrame(test_data)

    # 5件法での逆転
    result = reverse_score(df, columns=["Q1", "Q2"], scale_points=5)

    # Q1の逆転を確認
    assert result["Q1_r"].tolist() == [5, 4, 3, 2, 1]
    # Q2の逆転を確認
    assert result["Q2_r"].tolist() == [4, 3, 2, 1, 5]
    # Q3は逆転対象外なので元のデータフレームに含まれていることを確認
    assert "Q3" in result.columns
    assert "Q3_r" not in result.columns


def test_prepare_download_data():
    """ダウンロードデータの準備テスト"""
    # テストデータの作成
    original_df = pd.DataFrame({"Q1": [1, 2, 3], "Q2": [2, 3, 4], "Q3": [3, 4, 5]})

    reversed_df = pd.DataFrame(
        {
            "Q1": [1, 2, 3],
            "Q2": [2, 3, 4],
            "Q3": [3, 4, 5],
            "Q1_r": [5, 4, 3],
            "Q2_r": [4, 3, 2],
        }
    )

    # 元の項目を含むケース
    result_with_original = prepare_download_data(
        original_df, reversed_df, reverse_columns=["Q1", "Q2"], include_original=True
    )
    assert "Q1" in result_with_original.columns
    assert "Q1_r" in result_with_original.columns
    assert "Q2" in result_with_original.columns
    assert "Q2_r" in result_with_original.columns

    # 元の項目を含まないケース
    result_without_original = prepare_download_data(
        original_df, reversed_df, reverse_columns=["Q1", "Q2"], include_original=False
    )
    assert "Q1" not in result_without_original.columns
    assert "Q1_r" in result_without_original.columns
    assert "Q2" not in result_without_original.columns
    assert "Q2_r" in result_without_original.columns
    assert "Q3" in result_without_original.columns


def test_reverse_score_empty_columns():
    """空の逆転項目リストのテスト"""
    df = pd.DataFrame({"Q1": [1, 2, 3], "Q2": [2, 3, 4]})
    result = reverse_score(df, columns=[], scale_points=5)
    # 元のデータフレームと同じカラムを持つことを確認
    assert list(result.columns) == list(df.columns)


def test_prepare_download_data_no_reverse():
    """逆転項目がない場合のテスト"""
    df = pd.DataFrame({"Q1": [1, 2, 3], "Q2": [2, 3, 4]})
    result = prepare_download_data(
        df, df.copy(), reverse_columns=[], include_original=True
    )
    # 元のデータフレームと同じ内容であることを確認
    assert result.equals(df)
