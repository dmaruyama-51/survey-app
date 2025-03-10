from typing import Dict, List

import pandas as pd


def calculate_statistics(df: pd.DataFrame, column: str) -> Dict[str, float]:
    """
    指定されたカラムの基本統計量を計算する

    Args:
        df: 入力データフレーム
        column: 統計量を計算するカラム名

    Returns:
        統計量を含む辞書（平均、標準偏差、最小値、最大値など）
    """
    mean_val = df[column].mean()
    std_val = df[column].std()
    min_val = df[column].min()
    max_val = df[column].max()

    return {
        "mean": mean_val,
        "std": std_val,
        "min": min_val,
        "max": max_val,
        "mean_plus_std": mean_val + std_val,
        "mean_minus_std": mean_val - std_val,
    }


def check_ceiling_effect(stats: Dict[str, float]) -> bool:
    """
    天井効果があるかどうかを判定する

    Args:
        stats: 統計量を含む辞書

    Returns:
        天井効果がある場合はTrue、ない場合はFalse
    """
    return stats["mean_plus_std"] > stats["max"]


def check_floor_effect(stats: Dict[str, float]) -> bool:
    """
    床効果があるかどうかを判定する

    Args:
        stats: 統計量を含む辞書

    Returns:
        床効果がある場合はTrue、ない場合はFalse
    """
    return stats["mean_minus_std"] < stats["min"]


def create_statistics_summary(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    複数カラムの統計情報サマリーを作成する

    Args:
        df: 入力データフレーム
        columns: 統計量を計算するカラム名のリスト

    Returns:
        統計情報のサマリーを含むデータフレーム
    """
    stats_data = []

    for col in columns:
        stats = calculate_statistics(df, col)

        # 天井効果と床効果の判定
        ceiling_effect = check_ceiling_effect(stats)
        floor_effect = check_floor_effect(stats)

        # 効果の表示用テキスト
        ceiling_text = "⚠️ Yes" if ceiling_effect else "No"
        floor_text = "⚠️ Yes" if floor_effect else "No"

        # データを追加
        stats_data.append(
            {
                "Variable": col,
                "Mean": f"{stats['mean']:.2f}",
                "SD": f"{stats['std']:.2f}",
                "Min": f"{stats['min']:.2f}",
                "Max": f"{stats['max']:.2f}",
                "Mean+SD": f"{stats['mean_plus_std']:.2f}",
                "Mean-SD": f"{stats['mean_minus_std']:.2f}",
                "Ceiling Effect": ceiling_text,
                "Floor Effect": floor_text,
            }
        )

    # データフレームに変換
    return pd.DataFrame(stats_data)
