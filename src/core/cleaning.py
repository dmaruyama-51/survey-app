from typing import List

import pandas as pd

from src.utils.logger_config import logger


def remove_straight_line_responses(df: pd.DataFrame) -> List[int]:
    """
    ストレートライン回答（全て同じ値の回答）の行番号を取得
    Args:
        df (pd.DataFrame): 入力データフレーム
    Returns:
        List[int]: ストレートライン回答の行番号のリスト
    """
    try:
        straight_line_rows = df.std(axis=1) == 0
        remove_rows = straight_line_rows[straight_line_rows].index.tolist()
        if remove_rows:
            logger.info(f"Straight-line responses detected: {remove_rows}")
        return remove_rows

    except Exception as e:
        logger.error(f"Error detecting straight-line responses: {str(e)}")
        raise


def remove_missing_values(df: pd.DataFrame) -> List[int]:
    """
    欠損値を含む行番号を取得
    Args:
        df (pd.DataFrame): 入力データフレーム
    Returns:
        List[int]: 欠損値を含む行番号のリスト
    """
    try:
        remove_rows = df[df.isnull().any(axis=1)].index.tolist()
        if remove_rows:
            logger.info(f"Missing values detected: {remove_rows}")
        return remove_rows

    except Exception as e:
        logger.error(f"Error detecting missing values: {str(e)}")
        raise


def remove_out_of_range_values(df: pd.DataFrame, likert_scale_case: int) -> List[int]:
    """
    規定値を超える行番号を取得
    Args:
        df (pd.DataFrame): 入力データフレーム
        likert_scale_case (int): リッカート尺度のポイント数
    Returns:
        List[int]: 規定値を超える行番号のリスト
    """
    try:
        remove_rows_over = df[df.max(axis=1) > likert_scale_case].index.tolist()
        remove_rows_under = df[df.min(axis=1) < 1].index.tolist()
        remove_rows = remove_rows_over + remove_rows_under
        if remove_rows:
            logger.info(f"Out-of-range values detected: {remove_rows}")
        return remove_rows

    except Exception as e:
        logger.error(f"Error detecting out-of-range values: {str(e)}")
        raise


def remove_step_pattern_responses(df: pd.DataFrame) -> List[int]:
    """
    厳密な階段状のパターンを持つ回答の行番号を取得
    - 連続的な増加または減少
    - 増加後減少、または減少後増加
    - 連続的な増加/減少が途中で1に戻って再度増加するパターン
    同値を含むパターンは検出対象外とする
    ストレートラインも検出対象外

    Args:
        df (pd.DataFrame): 入力データフレーム
    Returns:
        List[int]: 階段状パターンの行番号のリスト
    """
    try:
        remove_rows = []
        for idx, row in df.iterrows():
            values = row.values
            # ストレートラインの場合はスキップ
            if len(set(values)) == 1:
                continue

            # 差分を計算
            diffs = [values[i + 1] - values[i] for i in range(len(values) - 1)]

            # 単調増加または単調減少のパターンをチェック（同値を含まない）
            if all(d > 0 for d in diffs) or all(d < 0 for d in diffs):
                remove_rows.append(idx)
                continue

            # 増加後減少または減少後増加のパターンをチェック
            peak_idx = None
            valley_idx = None

            # ピークを探す（厳密な増加後減少）
            for i in range(1, len(values) - 1):
                if all(values[j] < values[j + 1] for j in range(i)) and all(
                    values[j] > values[j + 1] for j in range(i, len(values) - 1)
                ):
                    peak_idx = i
                    break

            # 谷を探す（厳密な減少後増加）
            for i in range(1, len(values) - 1):
                if all(values[j] > values[j + 1] for j in range(i)) and all(
                    values[j] < values[j + 1] for j in range(i, len(values) - 1)
                ):
                    valley_idx = i
                    break

            # 連続増加が途中で1に戻るパターンをチェック
            is_reset_pattern = False
            segments = []
            current_segment = [values[0]]

            for i in range(1, len(values)):
                if values[i] == 1 and i < len(values) - 1:
                    if len(current_segment) > 1:
                        segments.append(current_segment)
                    current_segment = [values[i]]
                else:
                    current_segment.append(values[i])

            if len(current_segment) > 1:
                segments.append(current_segment)

            if len(segments) > 0:
                is_reset_pattern = all(
                    all(seg[j] < seg[j + 1] for j in range(len(seg) - 1))
                    for seg in segments
                )

            if peak_idx is not None or valley_idx is not None or is_reset_pattern:
                remove_rows.append(idx)

        if remove_rows:
            logger.info(f"Step pattern responses detected: {remove_rows}")
        return remove_rows

    except Exception as e:
        logger.error(f"Error detecting step pattern responses: {str(e)}")
        raise


def remove_invalid_responses(
    df: pd.DataFrame,
    likert_scale: int,
    remove_straight_lines: bool = False,
    remove_missing: bool = False,
    remove_out_of_range: bool = False,
    remove_step_pattern: bool = False,
) -> List[int]:
    """無効な回答を検出して削除"""
    try:
        remove_rows = []

        if remove_straight_lines:
            remove_rows.extend(remove_straight_line_responses(df))

        if remove_missing:
            remove_rows.extend(remove_missing_values(df))

        if remove_out_of_range:
            remove_rows.extend(remove_out_of_range_values(df, likert_scale))

        if remove_step_pattern:
            remove_rows.extend(remove_step_pattern_responses(df))

        # 重複を除去
        remove_rows = list(set(remove_rows))
        logger.info(f"Total {len(remove_rows)} invalid responses detected")
        return remove_rows

    except Exception as e:
        logger.error(f"Error detecting invalid responses: {str(e)}")
        raise
