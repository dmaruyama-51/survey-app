from src.interface.state import check_step2_completion


def test_check_step2_completion():
    """Step2の完了チェック機能のテスト"""
    # 両方とも未設定
    assert not check_step2_completion([], None)

    # カラムのみ設定
    assert not check_step2_completion(["col1"], None)

    # リッカート尺度のみ設定
    assert not check_step2_completion([], 5)

    # 両方とも設定
    assert check_step2_completion(["col1"], 5)
