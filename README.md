# TestRoad - テスト管理システム

TestRoadは、ソフトウェアテストの計画、実行、追跡を効率的に管理するためのWebアプリケーションです。

## 主な機能

- プロジェクト管理
- テストスイート管理
- テストケース作成・管理
- テストプラン作成
- テスト実行管理
- バグ追跡
- テストケースのインポート/エクスポート
- ファイル添付機能

## 技術スタック

- Python 3.11
- Django 5.0.2
- Tailwind CSS
- PostgreSQL（開発環境ではSQLite3）
- Docker & Docker Compose

## 開発環境のセットアップ

### 前提条件

- Python 3.11以上
- Node.js
- Docker & Docker Compose（オプション）

### ローカル環境でのセットアップ

1. リポジトリのクローン
```bash
git clone [repository-url]
cd testroad
```

2. 仮想環境の作成と有効化
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows
```

3. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

4. 環境変数の設定
```bash
cp .env.example .env
# .envファイルを編集して必要な設定を行う
```

5. データベースのマイグレーション
```bash
python manage.py migrate
```

6. 開発サーバーの起動
```bash
python manage.py runserver
```

### Dockerを使用したセットアップ

1. コンテナのビルドと起動
```bash
docker-compose up -d --build
```

2. マイグレーションの実行
```bash
docker-compose exec web python manage.py migrate
```

## 使用方法

1. 管理者アカウントの作成
```bash
python manage.py createsuperuser
```

2. ブラウザで以下のURLにアクセス
- 開発サーバー: http://localhost:8000
- 管理画面: http://localhost:8000/admin

## 主な機能の使い方

### プロジェクト管理
- プロジェクトの作成、編集、削除が可能
- プロジェクト単位でテストスイートを管理

### テストスイート
- プロジェクト内でテストケースをグループ化
- テストスイート単位でテストケースのインポート/エクスポートが可能

### テストケース
- 詳細な前提条件、テストステップ、期待される結果を記録
- ファイル添付機能でスクリーンショットなどを管理
- テストケースの複製機能

### テストプラン
- テストケースを選択してテストプランを作成
- テスト実行の進捗管理

### バグ追跡
- テスト実行中に発見されたバグの記録
- バグのステータス、優先度、担当者の管理

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
