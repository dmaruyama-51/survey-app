import pandas as pd
from typing import Tuple
from src.utils.logger_config import logger


def split_dataframe(
    df: pd.DataFrame, exclude_columns: list[str]
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    データフレームを処理対象とそうでない部分に分割
    Args:
        df (pd.DataFrame): Input dataframe
        exclude_columns (list[str]): List of columns to exclude
    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Data to process, Data not to process
    """
    try:
        df_to_process = df.drop(columns=exclude_columns)
        df_not_to_process = df.loc[:, exclude_columns]

        logger.info(f"Excluded columns: {exclude_columns}")
        logger.info(f"Data to process shape: {df_to_process.shape}")
        logger.info(f"Excluded data shape: {df_not_to_process.shape}")

        return df_to_process, df_not_to_process

    except Exception as e:
        logger.error(f"Dataframe split error: {str(e)}")
        raise


def create_final_dataset(
    cleaned_df: pd.DataFrame, removed_df: pd.DataFrame, rows_to_keep: list
) -> pd.DataFrame:
    """
    rows_to_keepを残した最終的にダウンロードされるデータフレームを作成
    Args:
        cleaned_df (pd.DataFrame): Cleaned data
        removed_df (pd.DataFrame): Removed data
        rows_to_keep (list): List of row indices to restore
    Returns:
        pd.DataFrame: Final dataset
    """
    if rows_to_keep:
        return pd.concat([cleaned_df, removed_df.loc[rows_to_keep]])
    return cleaned_df
