import pandas as pd
import pytest

from src.core.visualization import (
    calculate_statistics,
    check_ceiling_effect,
    check_floor_effect,
    create_statistics_summary,
)


def test_calculate_statistics():
    """基本統計量の計算機能をテスト"""
    # テストデータの作成
    test_data = {"Q1": [1, 2, 3, 4, 5]}
    df = pd.DataFrame(test_data)

    # 統計量の計算
    stats = calculate_statistics(df, "Q1")

    # 結果の検証
    assert stats["mean"] == 3.0
    assert stats["std"] == pytest.approx(1.5811, abs=0.001)
    assert stats["min"] == 1.0
    assert stats["max"] == 5.0
    assert stats["mean_plus_std"] == pytest.approx(4.5811, abs=0.001)
    assert stats["mean_minus_std"] == pytest.approx(1.4189, abs=0.001)


def test_check_ceiling_effect():
    """天井効果の判定機能をテスト"""
    # 天井効果がある場合
    stats_with_ceiling = {
        "mean": 4.5,
        "std": 0.8,
        "max": 5.0,
        "mean_plus_std": 5.3,  # mean + std > max
    }
    assert check_ceiling_effect(stats_with_ceiling) is True

    # 天井効果がない場合
    stats_without_ceiling = {
        "mean": 3.0,
        "std": 1.0,
        "max": 5.0,
        "mean_plus_std": 4.0,  # mean + std < max
    }
    assert check_ceiling_effect(stats_without_ceiling) is False


def test_check_floor_effect():
    """床効果の判定機能をテスト"""
    # 床効果がある場合
    stats_with_floor = {
        "mean": 1.5,
        "std": 0.8,
        "min": 1.0,
        "mean_minus_std": 0.7,  # mean - std < min
    }
    assert check_floor_effect(stats_with_floor) is True

    # 床効果がない場合
    stats_without_floor = {
        "mean": 3.0,
        "std": 1.0,
        "min": 1.0,
        "mean_minus_std": 2.0,  # mean - std > min
    }
    assert check_floor_effect(stats_without_floor) is False


def test_create_statistics_summary():
    """統計情報サマリーの作成機能をテスト"""
    # テストデータの作成
    test_data = {
        "Q1": [1, 2, 3, 4, 5],  # 通常の分布
        "Q2": [5, 5, 5, 4, 5],  # 天井効果あり
        "Q3": [1, 1, 1, 2, 1],  # 床効果あり
    }
    df = pd.DataFrame(test_data)

    # 統計情報サマリーの作成
    summary_df = create_statistics_summary(df, ["Q1", "Q2", "Q3"])

    # 結果の検証
    assert len(summary_df) == 3  # 3つのカラムに対する統計情報

    # Q1の検証（通常の分布）
    q1_row = summary_df[summary_df["Variable"] == "Q1"].iloc[0]
    assert q1_row["Ceiling Effect"] == "No"
    assert q1_row["Floor Effect"] == "No"

    # Q2の検証（天井効果あり）
    q2_row = summary_df[summary_df["Variable"] == "Q2"].iloc[0]
    assert q2_row["Ceiling Effect"] == "⚠️ Yes"

    # Q3の検証（床効果あり）
    q3_row = summary_df[summary_df["Variable"] == "Q3"].iloc[0]
    assert q3_row["Floor Effect"] == "⚠️ Yes"

    # 数値フォーマットの検証
    assert "." in q1_row["Mean"]  # 小数点以下が表示されていることを確認
    assert "." in q1_row["SD"]
