import pandas as pd
import pytest


def test_read_sample_data():
    """サンプルデータが正しく読み込めることをテスト"""
    df = pd.read_csv("src/data/sample.csv")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty


@pytest.fixture
def sample_csv(tmp_path):
    """テスト用のCSVファイルを作成するフィクスチャ"""
    df = pd.DataFrame({"column1": [1, 2, 3], "column2": ["a", "b", "c"]})
    csv_path = tmp_path / "test.csv"
    df.to_csv(csv_path, index=False)
    return csv_path


def test_file_upload(sample_csv):
    """ファイルアップロード機能のテスト"""
    df = pd.read_csv(sample_csv)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert list(df.columns) == ["column1", "column2"]
