import pandas as pd
from src.step3 import remove_straight_line_responses


def test_remove_straight_line_responses():
    """ストレートライン回答の削除をテスト"""
    # テストデータの作成
    test_data = {"Q1": [1, 1, 2, 3], "Q2": [1, 1, 3, 4], "Q3": [1, 1, 4, 5]}
    df = pd.DataFrame(test_data)
    result_df = remove_straight_line_responses(df)

    # 検証
    assert (
        len(result_df) == 2
    )  # ストレートライン回答（1行目）が削除されていることを確認
    assert result_df.index.tolist() == [2, 3]  # 残っている行が正しいことを確認
    assert (result_df.std(axis=1) != 0).all()  # 全ての行の標準偏差が0でないことを確認


def test_remove_straight_line_responses_no_straight_lines():
    """ストレートライン回答が存在しない場合のテスト"""
    # テストデータの作成（ストレートライン回答なし）
    test_data = {"Q1": [1, 2, 3], "Q2": [2, 3, 4], "Q3": [3, 4, 5]}
    df = pd.DataFrame(test_data)
    result_df = remove_straight_line_responses(df)

    # 検証
    assert len(result_df) == len(df)  # データフレームのサイズが変わっていないことを確認
    assert result_df.equals(df)  # 元のデータフレームと同じであることを確認
