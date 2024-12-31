import pytest
import pandas as pd
import streamlit as st
from src.interface.state import (
    check_data_settings_completion,
    initialize_cleaning_state,
    reset_cleaning_state,
)


def test_check_data_settings_completion():
    """Step2の完了チェック機能のテスト"""
    # 両方とも未設定
    assert not check_data_settings_completion([], None)

    # カラムのみ設定
    assert not check_data_settings_completion(["col1"], None)

    # リッカート尺度のみ設定
    assert not check_data_settings_completion([], 5)

    # 両方とも設定
    assert check_data_settings_completion(["col1"], 5)


def test_initialize_cleaning_state():
    """クリーニング状態の初期化テスト"""
    # テストデータの準備
    df_to_process = pd.DataFrame({"Q1": [1, 2, 3], "Q2": [1, 2, 3]})
    df_not_to_process = pd.DataFrame({"ID": ["001", "002", "003"]})
    likert_scale = 5
    reqs = (True, False, False, False)  # ストレートライン検出のみ有効

    # 関数の実行
    initialize_cleaning_state(df_to_process, df_not_to_process, likert_scale, reqs)

    # セッション状態の検証
    assert "cleaned_df" in st.session_state
    assert "removed_df" in st.session_state

    # クリーニング結果の検証
    assert len(st.session_state.cleaned_df) + len(st.session_state.removed_df) == len(
        df_to_process
    )
    assert "ID" in st.session_state.cleaned_df.columns
    assert "ID" in st.session_state.removed_df.columns


def test_reset_cleaning_state():
    """クリーニング状態のリセットテスト"""
    # テスト用のセッション状態を設定
    st.session_state.cleaned_df = pd.DataFrame({"test": [1, 2, 3]})
    st.session_state.removed_df = pd.DataFrame({"test": [4, 5]})
    st.session_state.cleaning_executed = True

    # リセット実行
    reset_cleaning_state()

    # セッション状態の検証
    assert "cleaned_df" not in st.session_state
    assert "removed_df" not in st.session_state
    assert "cleaning_executed" not in st.session_state


@pytest.mark.parametrize(
    "df_to_process,reqs,expected_removed",
    [
        # ストレートライン回答のみ検出
        (
            pd.DataFrame({"Q1": [1, 1, 2], "Q2": [1, 1, 3]}),
            (True, False, False, False),
            2,
        ),  # 2行が削除される
        # 欠損値のみ検出
        (
            pd.DataFrame({"Q1": [1, None, 2], "Q2": [1, 2, 3]}),
            (False, True, False, False),
            1,
        ),  # 1行が削除される
        # 範囲外の値のみ検出
        (
            pd.DataFrame({"Q1": [1, 6, 2], "Q2": [1, 2, 3]}),
            (False, False, True, False),
            1,
        ),  # 1行が削除される
    ],
)
def test_initialize_cleaning_state_various_cases(df_to_process, reqs, expected_removed):
    """様々なケースでのクリーニング状態初期化テスト"""
    df_not_to_process = pd.DataFrame({"ID": ["001"] * len(df_to_process)})
    likert_scale = 5

    initialize_cleaning_state(df_to_process, df_not_to_process, likert_scale, reqs)

    assert len(st.session_state.removed_df) == expected_removed
    assert len(st.session_state.cleaned_df) == len(df_to_process) - expected_removed
