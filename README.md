# Survey App

## Description

リッカート尺度で取得した社会調査データを統計処理にかける前にクリーニングするアプリ
以下の処理に対応（予定）

- ストレートラインの除去（全部同一値の回答）
- 欠損値を含む行の除去
- 異常値を含む行の除去（例えば5件法で -1 や 100 といった値）
- 階段回答の除去（1, 2, 3, 4, 5... といった回答）


## Setup

```bash
# 必要なパッケージのインストール
poetry install

# local環境で起動
poetry run streamlit run src/app.py
```


## Deploy

Deployは main ブランチへの push 時に Github Actions で自動実行される。

以下の用意が必要
- Github Actions の環境変数に以下を登録
    - PROJECT_ID: GCPのプロジェクトID
    - REGION: GCPのリージョン
    - REPOSITORY_NAME: Artifact Registryのリポジトリ名
    - APP_NAME: Cloud Runのサービス名
- Github Actions の Secrets に以下を登録
    - WORKLOAD_IDENTITY_PROVIDER: Workload Identity Providerの値
    - SERVICE_ACCOUNT: サービスアカウントのメールアドレス
