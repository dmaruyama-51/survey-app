import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger():
    """
    アプリケーション用のロガーを設定する

    設定内容:
    - INFOレベル以上のログをコンソールに出力
    - ERRORレベル以上のログをファイルに出力（ローテーション付き）
    - Streamlitのデフォルトログレベルを調整
    """
    # ロガーの取得
    logger = logging.getLogger("survey_cleaning_app")
    logger.setLevel(logging.INFO)

    # フォーマッターの作成
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # コンソールハンドラの設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ファイルハンドラの設定（エラーログ用）
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    file_handler = RotatingFileHandler(
        filename=os.path.join(logs_dir, "error.log"),
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)

    # ハンドラの追加（既存のハンドラを削除してから）
    logger.handlers.clear()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Streamlitのログレベルを調整
    logging.getLogger("streamlit").setLevel(logging.WARNING)

    return logger


logger = setup_logger()
