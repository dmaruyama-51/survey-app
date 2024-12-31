import pandas as pd
from typing import List


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
