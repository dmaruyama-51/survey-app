import streamlit as st
import pandas as pd
from typing import List
from src.utils.logger_config import logger


# pragma: no cover
def display_cleaning_options() -> tuple[bool, bool, bool, bool]:
    """データクリーニングのオプションを表示し、選択状態を返す"""
    st.markdown("#### Data Cleaning Options")
    req1 = st.checkbox("Remove straight-line responses")
    req2 = st.checkbox("Remove responses with missing values")
    req3 = st.checkbox("Remove responses outside of valid range")
    req4 = st.checkbox("Remove step pattern responses")
    return req1, req2, req3, req4


def initialize_cleaning_state(
    df_to_process: pd.DataFrame,
    df_not_to_process: pd.DataFrame,
    likert_scale_case: int,
    reqs: tuple[bool, bool, bool, bool],
) -> None:
    """クリーニング処理の初期化と実行"""
    req1, req2, req3, req4 = reqs
    remove_rows = remove_invalid_responses(
        df_to_process, likert_scale_case, req1, req2, req3, req4
    )
    all_df = pd.concat([df_not_to_process, df_to_process], axis=1)
    st.session_state.cleaned_df = all_df.drop(index=remove_rows)
    st.session_state.removed_df = all_df.loc[remove_rows]


def display_removed_records_editor() -> list:
    """削除されたレコードの編集UIを表示"""
    if "removed_df_with_checkbox" not in st.session_state:
        st.session_state.removed_df_with_checkbox = st.session_state.removed_df.copy()
        st.session_state.removed_df_with_checkbox.insert(0, "Keep This Row", False)
        st.session_state.editor_key = 0

    edited_df = st.data_editor(
        st.session_state.removed_df_with_checkbox,
        hide_index=True,
        column_config={
            "Keep This Row": st.column_config.CheckboxColumn(
                "Keep This Row",
                help="Select to keep this row in the final dataset",
                default=False,
            )
        },
        key=f"removed_records_editor_{st.session_state.editor_key}",
    )

    if not edited_df.equals(st.session_state.removed_df_with_checkbox):
        st.session_state.removed_df_with_checkbox = edited_df.copy()
        st.session_state.editor_key += 1
        st.rerun()

    return st.session_state.removed_df_with_checkbox[
        st.session_state.removed_df_with_checkbox["Keep This Row"]
    ].index.tolist()


def create_final_dataset(rows_to_keep: list) -> pd.DataFrame:
    """最終的なデータセットを作成"""
    if rows_to_keep:
        final_cleaned_df = pd.concat(
            [st.session_state.cleaned_df, st.session_state.removed_df.loc[rows_to_keep]]
        )
        st.write(
            f"Final dataset will keep {len(rows_to_keep)} previously removed rows."
        )
    else:
        final_cleaned_df = st.session_state.cleaned_df
    return final_cleaned_df


def reset_cleaning_state() -> None:
    """クリーニング関連の全セッション状態をリセット"""
    keys_to_remove = [
        "cleaning_executed",
        "cleaned_df",
        "removed_df",
        "removed_df_with_checkbox",
        "editor_key",
    ]
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]


def process_data_cleaning_and_export(
    df_to_process: pd.DataFrame, df_not_to_process: pd.DataFrame, likert_scale_case: int
) -> pd.DataFrame:
    """
    データクリーニングの要件を選択し、実行ボタンクリック後にクリーニングを実施、
    クリーニング後のデータをダウンロード可能にする
    """
    try:
        # クリーニングオプションの表示
        cleaning_reqs = display_cleaning_options()

        # セッション状態の初期化
        if "cleaning_executed" not in st.session_state:
            st.session_state.cleaning_executed = False

        start_cleaning = st.button("Start Data Cleaning")

        # クリーニング実行ボタンの処理
        if start_cleaning or st.session_state.cleaning_executed:
            st.session_state.cleaning_executed = True

            if not any(cleaning_reqs):
                st.warning("Please select at least one cleaning option.")
                return df_to_process

            logger.info(
                f"クリーニング要件選択: straight_lines={cleaning_reqs[0]}, "
                f"missing={cleaning_reqs[1]}, out_of_range={cleaning_reqs[2]}, "
                f"step_pattern={cleaning_reqs[3]}"
            )

            # 初回実行時のみクリーニングを実行
            if "cleaned_df" not in st.session_state:
                initialize_cleaning_state(
                    df_to_process, df_not_to_process, likert_scale_case, cleaning_reqs
                )

            if not st.session_state.cleaned_df.empty:
                st.markdown("#### Cleaning Results and Download")
                st.write(
                    "Below are the records marked for removal. Please check any rows you wish to keep. "
                    "If no rows are selected, the downloaded data will exclude all records shown here."
                )

                # 削除レコードの選択UI
                rows_to_keep = display_removed_records_editor()

                # 最終データセットの作成
                final_cleaned_df = create_final_dataset(rows_to_keep)

                # リセットボタンとダウンロードボタンの表示
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("Reset Cleaning Process"):
                        reset_cleaning_state()
                        st.rerun()
                with col2:
                    csv = final_cleaned_df.to_csv(index=False)
                    st.download_button(
                        label="Download Cleaned Data",
                        data=csv,
                        file_name="cleaned_survey_data.csv",
                        mime="text/csv",
                    )
                return final_cleaned_df
            else:
                st.warning(
                    "All rows have been removed. No data is available for download."
                )

        return df_to_process

    except Exception as e:
        logger.error(f"データクリーニング処理エラー: {str(e)}")
        raise


def remove_invalid_responses(
    df: pd.DataFrame,
    likert_scale_case: int,
    req1: bool,
    req2: bool,
    req3: bool,
    req4: bool,
) -> List[int]:
    """
    指定された要件に基づいて無効な回答の行番号を取得
    Args:
        df (pd.DataFrame): 入力データフレーム
        likert_scale_case (int): リッカート尺度のポイント数
        req1 (bool): ストレートライン回答を削除するかどうか
        req2 (bool): 欠損値を含む行を削除するかどうか
        req3 (bool): 規定値を超える行を削除するかどうか
        req4 (bool): 階段状のパターンを削除するかどうか
    Returns:
        List[int]: 削除対象の行インデックスのリスト
    """
    try:
        remove_rows: List[int] = []
        if req1:
            req1_remove_rows = remove_straight_line_responses(df)
            remove_rows.extend(req1_remove_rows)
            logger.info(f"ストレートライン削除行数: {len(req1_remove_rows)}")

        if req2:
            req2_remove_rows = remove_missing_values(df)
            remove_rows.extend(req2_remove_rows)
            logger.info(f"欠損値削除行数: {len(req2_remove_rows)}")

        if req3:
            req3_remove_rows = remove_out_of_range_values(df, likert_scale_case)
            remove_rows.extend(req3_remove_rows)
            logger.info(f"範囲外値削除行数: {len(req3_remove_rows)}")

        if req4:
            req4_remove_rows = remove_step_pattern_responses(df)
            remove_rows.extend(req4_remove_rows)
            logger.info(f"階段パターン削除行数: {len(req4_remove_rows)}")

        return list(set(remove_rows))  # 重複を除去

    except Exception as e:
        logger.error(f"無効回答削除処理エラー: {str(e)}")
        raise


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
            logger.info(f"ストレートライン検出: {remove_rows}")
        return remove_rows

    except Exception as e:
        logger.error(f"ストレートライン検出エラー: {str(e)}")
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
            logger.info(f"欠損値検出: {remove_rows}")
        return remove_rows

    except Exception as e:
        logger.error(f"欠損値検出エラー: {str(e)}")
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
            logger.info(f"範囲外値検出: {remove_rows}")
        return remove_rows

    except Exception as e:
        logger.error(f"範囲外値検出エラー: {str(e)}")
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
                if (
                    values[i] == 1 and i < len(values) - 1
                ):  # 1に戻る点を検出（最後の要素は除く）
                    if (
                        len(current_segment) > 1
                    ):  # セグメントが複数の要素を持つ場合のみ追加
                        segments.append(current_segment)
                    current_segment = [values[i]]
                else:
                    current_segment.append(values[i])

            # 最後のセグメントを追加
            if len(current_segment) > 1:
                segments.append(current_segment)

            # 各セグメントが厳密な増加パターンかチェック
            if len(segments) > 0:
                is_reset_pattern = all(
                    all(seg[j] < seg[j + 1] for j in range(len(seg) - 1))
                    for seg in segments
                )

            if peak_idx is not None or valley_idx is not None or is_reset_pattern:
                remove_rows.append(idx)

        if remove_rows:
            logger.info(f"階段パターン検出: {remove_rows}")
        return remove_rows

    except Exception as e:
        logger.error(f"階段パターン検出エラー: {str(e)}")
        raise
