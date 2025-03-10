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


def remove_step_pattern_responses(df: pd.DataFrame, likert_scale: int) -> List[int]:
    """
    階段パターンの回答を判定

    【要件】
        1. 各被験者の回答は、1〜ユーザーが指定したポイント数（例: 7, 5, 10 など）の整数が20項目分、リスト形式で与えられるものとします。
        2. ユーザーはリッカート尺度のポイント数を自由に指定できるようにし、関数の引数としてその尺度の最大値（例: 7）を受け取ります。
        3. 「階段状パターン」とは、隣接する回答が常に ±1 の変化を示すパターンです。ただし、以下の循環ケースを考慮してください。
        - 昇順の場合:
            - 通常ケース：前の回答が指定された最大値以外の場合、次の回答は「前の回答 + 1」でなければならない。
            - 循環ケース：前の回答が指定された最大値の場合、次の回答は 1 である必要がある。
        - 降順の場合:
            - 通常ケース：前の回答が 1 以外の場合、次の回答は「前の回答 - 1」でなければならない。
            - 循環ケース：前の回答が 1 の場合、次の回答は指定された最大値である必要がある。
        4. 山型パターン（昇順から降順に変わる）や谷型パターン（降順から昇順に変わる）も階段パターンとして検出します。
        5. 与えられたリスト全体が、上記のパターンに該当する場合は remove_rows に行番号を追加

    Args:
        df (pd.DataFrame): 入力データフレーム
        likert_scale (int): リッカート尺度のポイント数
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

            # 階段パターンのチェック（昇順・降順・山型・谷型を含む）
            is_step_pattern = True
            
            # 前の値と現在の値の差分を記録
            prev_diff = None
            
            for i in range(len(values) - 1):
                current_val = values[i]
                next_val = values[i + 1]
                
                # 通常の昇順ケース
                if current_val < likert_scale and next_val == current_val + 1:
                    current_diff = 1
                # 昇順の循環ケース
                elif current_val == likert_scale and next_val == 1:
                    current_diff = 1
                # 通常の降順ケース
                elif current_val > 1 and next_val == current_val - 1:
                    current_diff = -1
                # 降順の循環ケース
                elif current_val == 1 and next_val == likert_scale:
                    current_diff = -1
                # 階段パターンではない
                else:
                    is_step_pattern = False
                    break
                
                # 方向の変化をチェック（山型・谷型パターンの検出）
                if prev_diff is not None and prev_diff != current_diff:
                    # 方向が変わっても階段パターンとして検出する
                    pass
                
                prev_diff = current_diff

            if is_step_pattern:
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
            remove_rows.extend(remove_step_pattern_responses(df, likert_scale))

        # 重複を除去
        remove_rows = list(set(remove_rows))
        logger.info(f"Total {len(remove_rows)} invalid responses detected")
        return remove_rows

    except Exception as e:
        logger.error(f"Error detecting invalid responses: {str(e)}")
        raise
