import pandas as pd

from src.core.cleaning import (
    remove_invalid_responses,
    remove_missing_values,
    remove_out_of_range_values,
    remove_step_pattern_responses,
    remove_straight_line_responses,
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


def test_remove_step_pattern_responses():
    """階段パターン回答の検出をテスト"""
    # テストデータの作成（7段階のリッカート尺度を想定）

    # 昇順パターン（1,2,3,4,5,6,7,1,2,3,4,5,6,7,1）
    ascending_data = [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1]

    # 降順パターン（7,6,5,4,3,2,1,7,6,5,4,3,2,1,7）
    descending_data = [7, 6, 5, 4, 3, 2, 1, 7, 6, 5, 4, 3, 2, 1, 7]

    # 階段パターンではないケース
    non_pattern_data = [1, 3, 2, 5, 4, 6, 7, 2, 5, 3, 1, 4, 6, 2, 3]

    # ストレートラインケース（すべて4）
    straight_line_data = [4] * 15

    # 山型パターン（1,2,3,4,5,6,7,6,5,4,3,2,1,2,3）
    mountain_pattern = [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 2, 3]

    # 谷型パターン（7,6,5,4,3,2,1,2,3,4,5,6,7,6,5）
    valley_pattern = [7, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6, 7, 6, 5]

    # 各パターンのデータフレームを作成
    columns = [f"Q{i}" for i in range(1, 16)]

    df_ascending = pd.DataFrame([ascending_data], columns=columns)
    df_descending = pd.DataFrame([descending_data], columns=columns)
    df_non_pattern = pd.DataFrame([non_pattern_data], columns=columns)
    df_straight_line = pd.DataFrame([straight_line_data], columns=columns)
    df_mountain = pd.DataFrame([mountain_pattern], columns=columns)
    df_valley = pd.DataFrame([valley_pattern], columns=columns)

    # 混合ケース（階段パターンと非パターン）
    df_mixed = pd.DataFrame(
        [
            ascending_data,  # 行0: 昇順パターン（検出される）
            non_pattern_data,  # 行1: 非パターン（検出されない）
            descending_data,  # 行2: 降順パターン（検出される）
            mountain_pattern,  # 行3: 山型パターン（検出される）
            valley_pattern,  # 行4: 谷型パターン（検出される）
        ],
        columns=columns,
    )

    likert_scale = 7

    # 各ケースのテスト
    # 昇順パターン
    remove_rows = remove_step_pattern_responses(df_ascending, likert_scale)
    assert len(remove_rows) == 1
    assert 0 in remove_rows

    # 降順パターン
    remove_rows = remove_step_pattern_responses(df_descending, likert_scale)
    assert len(remove_rows) == 1
    assert 0 in remove_rows

    # 階段パターンではないケース
    remove_rows = remove_step_pattern_responses(df_non_pattern, likert_scale)
    assert len(remove_rows) == 0

    # ストレートラインケース（階段パターンとして検出されない）
    remove_rows = remove_step_pattern_responses(df_straight_line, likert_scale)
    assert len(remove_rows) == 0

    # 山型パターン（階段パターンとして検出される）
    remove_rows = remove_step_pattern_responses(df_mountain, likert_scale)
    assert len(remove_rows) == 1
    assert 0 in remove_rows

    # 谷型パターン（階段パターンとして検出される）
    remove_rows = remove_step_pattern_responses(df_valley, likert_scale)
    assert len(remove_rows) == 1
    assert 0 in remove_rows

    # 混合ケース（階段パターンの行のみ検出される）
    remove_rows = remove_step_pattern_responses(df_mixed, likert_scale)
    assert len(remove_rows) == 4  # 行0, 行2, 行3, 行4が検出される
    assert set(remove_rows) == {0, 2, 3, 4}  # 行0, 行2, 行3, 行4が検出される


def test_remove_invalid_responses_with_step_pattern():
    """階段パターンを含む無効な回答の検出をテスト"""
    # テストデータの作成（15カラム）
    columns = [f"Q{i}" for i in range(1, 16)]

    # 昇順パターン
    ascending_data = [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1]

    # 通常データ（階段パターンではない）
    normal_data = [4, 2, 5, 3, 6, 2, 4, 5, 3, 6, 7, 2, 1, 4, 5]

    # 欠損値を含むデータ
    missing_data = [1, 2, None, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1]

    # 範囲外の値を含むデータ
    out_of_range_data = [1, 2, 8, 4, 5, 6, 7, 1, 2, 3, 4, 5, 6, 7, 1]

    # 山型パターン
    mountain_pattern = [1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 2, 3]

    # データフレーム作成
    df = pd.DataFrame(
        [
            ascending_data,  # 行0: 階段パターン
            normal_data,  # 行1: 通常データ
            missing_data,  # 行2: 欠損値あり
            out_of_range_data,  # 行3: 範囲外の値あり
            mountain_pattern,  # 行4: 山型パターン（階段パターンとして検出される）
        ],
        columns=columns,
    )

    # 階段パターンのみ検出
    remove_rows = remove_invalid_responses(
        df,
        likert_scale=7,
        remove_straight_lines=False,
        remove_missing=False,
        remove_out_of_range=False,
        remove_step_pattern=True,
    )

    # 検証
    assert len(remove_rows) == 2  # 行0と行4が検出される
    assert set(remove_rows) == {0, 4}  # 行0と行4が検出される

    # 複合条件での検出
    remove_rows = remove_invalid_responses(
        df,
        likert_scale=7,
        remove_straight_lines=True,
        remove_missing=True,
        remove_out_of_range=True,
        remove_step_pattern=True,
    )

    # 検証
    assert len(remove_rows) == 4  # 行0, 行2, 行3, 行4が検出される
    assert set(remove_rows) == {0, 2, 3, 4}

    # ストレートラインと階段パターンの両方を含むケース
    straight_line_data = [3] * 15
    df_with_straight = pd.DataFrame(
        [
            ascending_data,  # 行0: 階段パターン
            straight_line_data,  # 行1: ストレートライン
        ],
        columns=columns,
    )

    remove_rows = remove_invalid_responses(
        df_with_straight,
        likert_scale=7,
        remove_straight_lines=True,
        remove_missing=False,
        remove_out_of_range=False,
        remove_step_pattern=True,
    )

    # 検証
    assert len(remove_rows) == 2  # 両方の行が検出される
    assert set(remove_rows) == {0, 1}
