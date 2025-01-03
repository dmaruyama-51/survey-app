from typing import List

import pandas as pd


def reverse_score(
    df: pd.DataFrame, columns: List[str], scale_points: int
) -> pd.DataFrame:
    """
    選択された列の得点を逆転させる
    例：5件法の場合、1→5, 2→4, 3→3, 4→2, 5→1
    """
    df_reversed = df.copy()
    for col in columns:
        df_reversed[f"{col}_r"] = (scale_points + 1) - df[col]
    return df_reversed


def prepare_download_data(
    df: pd.DataFrame,
    reversed_df: pd.DataFrame,
    reverse_columns: List[str],
    include_original: bool,
) -> pd.DataFrame:
    """ダウンロード用のデータフレームを準備"""
    if not include_original:
        # 元のカラムを削除し、逆転項目のみを含むデータフレームを作成
        download_df = df.drop(columns=reverse_columns).copy()
        # 逆転項目を追加
        for col in reverse_columns:
            download_df[f"{col}_r"] = reversed_df[f"{col}_r"]
        return download_df
    return reversed_df


def calculate_scale_scores(
    df: pd.DataFrame,
    scale_columns: List[str],
    scale_name: str,
) -> pd.DataFrame:
    """
    指定された列の合計得点と平均得点を計算する

    Args:
        df (pd.DataFrame): 入力データフレーム
        scale_columns (List[str]): 因子を構成する項目のリスト
        scale_name (str): 因子の名前
    Returns:
        pd.DataFrame: 合計得点と平均得点が追加されたデータフレーム
    """
    df_scores = df.copy()
    # 合計得点を計算
    df_scores[f"{scale_name}_total"] = df[scale_columns].sum(axis=1)
    # 平均得点を計算
    df_scores[f"{scale_name}_mean"] = df[scale_columns].mean(axis=1)
    return df_scores
