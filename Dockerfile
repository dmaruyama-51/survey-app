# Pythonの公式イメージをベースに使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# poetryのインストール
RUN pip install --no-cache-dir poetry

# 依存関係ファイルをコピー
COPY pyproject.toml poetry.lock ./

# poetry設定を変更（仮想環境を作成しない）
RUN poetry config virtualenvs.create false

# 依存関係のインストール
RUN poetry install --without dev --no-root --no-interaction --no-ansi

# アプリケーションのソースコードをコピー
COPY src/ ./src/

ENV PYTHONPATH=/app

EXPOSE 8080
CMD poetry run streamlit run src/app.py --server.port 8080 --server.address 0.0.0.0