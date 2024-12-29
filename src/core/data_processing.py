import pandas as pd
from typing import Tuple
from src.utils.logger_config import logger


def split_dataframe(
    df: pd.DataFrame, exclude_columns: list[str]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    データフレームを処理対象と非対象に分割する
    Args:
        df (pd.DataFrame): 入力データフレーム
        exclude_columns (list[str]): 除外するカラムのリスト
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: 処理対象データ、非処理対象データ
    """
    try:
        df_to_process = df.drop(columns=exclude_columns)
        df_not_to_process = df.loc[:, exclude_columns]

        logger.info(f"除外カラム: {exclude_columns}")
        logger.info(f"処理対象データ shape: {df_to_process.shape}")
        logger.info(f"除外データ shape: {df_not_to_process.shape}")

        return df_to_process, df_not_to_process

    except Exception as e:
        logger.error(f"データフレーム分割エラー: {str(e)}")
        raise


def create_final_dataset(
    cleaned_df: pd.DataFrame, removed_df: pd.DataFrame, rows_to_keep: list
) -> pd.DataFrame:
    """
    最終的なデータセットを作成
    Args:
        cleaned_df (pd.DataFrame): クリーニング済みデータ
        removed_df (pd.DataFrame): 除外されたデータ
        rows_to_keep (list): 復元する行のインデックスリスト
    Returns:
        pd.DataFrame: 最終的なデータセット
    """
    if rows_to_keep:
        return pd.concat([cleaned_df, removed_df.loc[rows_to_keep]])
    return cleaned_df
