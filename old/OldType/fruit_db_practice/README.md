# フルーツ価格データベース練習プロジェクト

SQLiteデータベースのCRUD操作を学習するための練習用プロジェクトです。

## プロジェクト概要

このプロジェクトでは、フルーツの価格情報を管理するシンプルなデータベースアプリケーションを作成し、以下の操作を学習できます：

- **CREATE（作成）**: 新しいフルーツ情報の追加
- **READ（読み取り）**: フルーツ情報の取得・検索
- **UPDATE（更新）**: 既存のフルーツ情報の修正
- **DELETE（削除）**: フルーツ情報の削除

## ファイル構成

```
fruit_db_practice/
├── fruit_db.py          # メインのデータベース操作ファイル
├── test_fruit_db.py     # 動作確認用テストファイル
├── fruit_prices.db      # SQLiteデータベースファイル
├── requirements.txt     # 依存関係ファイル
└── README.md           # このファイル
```

## 必要な環境

- Python 3.6以上
- 追加のライブラリは不要（Python標準ライブラリのみ使用）

## セットアップ

1. プロジェクトフォルダーに移動
```bash
cd fruit_db_practice
```

2. データベースの初期化（初回のみ）
```bash
python fruit_db.py
```

## 使用方法

### 1. 自動テストの実行

```bash
python test_fruit_db.py
```

このコマンドで以下のテストが自動実行されます：
- データベース初期化
- フルーツの追加（CREATE）
- フルーツの取得・検索（READ）
- フルーツ情報の更新（UPDATE）
- フルーツの削除（DELETE）
- 統計情報の表示

### 2. 対話モードでの操作

テスト実行後に対話モードが起動します。以下のコマンドが使用できます：

```
add <名前> <価格> [カテゴリ] [説明]  # フルーツ追加
list                              # 全フルーツ表示
get <ID>                          # 特定フルーツ表示
search <名前>                     # 名前検索
update <ID> <項目> <値>           # 更新
delete <ID>                       # 削除
stats                             # 統計表示
quit                              # 終了
```

### 3. プログラムから直接使用

```python
import fruit_db

# データベース初期化
fruit_db.init_fruit_database()

# フルーツ追加
fruit_db.add_fruit("りんご", 150, "果物", "甘くて美味しい")

# 全フルーツ取得
fruits = fruit_db.get_all_fruits()

# 特定フルーツ取得
fruit = fruit_db.get_fruit_by_id(1)

# フルーツ更新
fruit_db.update_fruit(1, price=180)

# フルーツ削除
fruit_db.delete_fruit(1)
```

## データベース構造

### fruits テーブル

| カラム名 | データ型 | 説明 |
|---------|---------|------|
| id | INTEGER | 主キー（自動採番） |
| name | TEXT | フルーツ名（必須、ユニーク） |
| price | INTEGER | 価格（必須） |
| category | TEXT | カテゴリ（オプション） |
| description | TEXT | 説明（オプション） |
| created_at | TIMESTAMP | 作成日時（自動設定） |
| updated_at | TIMESTAMP | 更新日時（自動設定） |

## 学習ポイント

### 1. SQLクエリの基本

```sql
-- テーブル作成
CREATE TABLE fruits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    price INTEGER NOT NULL
);

-- データ挿入
INSERT INTO fruits (name, price) VALUES (?, ?);

-- データ取得
SELECT * FROM fruits WHERE name LIKE ?;

-- データ更新
UPDATE fruits SET price = ? WHERE id = ?;

-- データ削除
DELETE FROM fruits WHERE id = ?;
```

### 2. プレースホルダーの使用

```python
# 安全なSQLクエリ（推奨）
cursor.execute('INSERT INTO fruits (name, price) VALUES (?, ?)', (name, price))

# 危険なSQLクエリ（非推奨）
cursor.execute(f"INSERT INTO fruits (name, price) VALUES ('{name}', {price})")
```

### 3. エラーハンドリング

```python
try:
    # データベース操作
    conn = sqlite3.connect('fruit_prices.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
except Exception as e:
    # エラー処理
    if conn:
        conn.rollback()
    print(f"エラー: {e}")
finally:
    # リソースの解放
    if conn:
        conn.close()
```

## 拡張アイデア

1. **Webアプリケーション化**: FlaskやFastAPIを使用
2. **データ可視化**: matplotlibでグラフ作成
3. **GUIアプリケーション**: tkinterやPyQtでデスクトップアプリ
4. **API化**: RESTful APIの作成
5. **テスト追加**: pytestでユニットテスト

## トラブルシューティング

### よくあるエラー

1. **データベースファイルが見つからない**
   - `python fruit_db.py`を実行してデータベースを初期化

2. **重複エラー**
   - 同じ名前のフルーツは追加できません

3. **文字エンコーディングエラー**
   - Windows環境では文字化けが発生する場合があります

## ライセンス

このプロジェクトは学習目的で作成されています。自由に使用・改変してください。
