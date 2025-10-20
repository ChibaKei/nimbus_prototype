import sqlite3
from datetime import datetime

def init_fruit_database():
    """フルーツ価格データベースの初期化（テーブル作成）"""
    conn = None
    try:
        conn = sqlite3.connect('fruit_prices.db')
        cursor = conn.cursor()
        
        # フルーツ価格テーブルを作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fruits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price INTEGER NOT NULL,
                category TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        print("フルーツ価格データベースを初期化しました")
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"データベース初期化エラー: {e}")
        raise
    finally:
        if conn:
            conn.close()

# CREATE（作成）
def add_fruit(name, price, category=None, description=None):
    """新しいフルーツを追加"""
    conn = None
    try:
        conn = sqlite3.connect('fruit_prices.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO fruits (name, price, category, description)
            VALUES (?, ?, ?, ?)
        ''', (name, price, category, description))
        
        fruit_id = cursor.lastrowid
        conn.commit()
        print(f"OK フルーツ '{name}' を追加しました（ID: {fruit_id}）")
        return fruit_id
    except sqlite3.IntegrityError:
        print(f"NG エラー: フルーツ '{name}' は既に存在します")
        return None
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"NG フルーツ追加エラー: {e}")
        return None
    finally:
        if conn:
            conn.close()

# READ（読み取り）
def get_all_fruits():
    """全てのフルーツを取得"""
    conn = None
    try:
        conn = sqlite3.connect('fruit_prices.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, price, category, description, created_at, updated_at
            FROM fruits
            ORDER BY name
        ''')
        
        fruits = cursor.fetchall()
        print(f"全フルーツ一覧（{len(fruits)}件）:")
        for fruit in fruits:
            print(f"  ID: {fruit[0]}, 名前: {fruit[1]}, 価格: {fruit[2]}円, カテゴリ: {fruit[3] or 'なし'}")
        return fruits
    except Exception as e:
        print(f"NG フルーツ取得エラー: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_fruit_by_id(fruit_id):
    """指定したIDのフルーツを取得"""
    conn = None
    try:
        conn = sqlite3.connect('fruit_prices.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, price, category, description, created_at, updated_at
            FROM fruits
            WHERE id = ?
        ''', (fruit_id,))
        
        fruit = cursor.fetchone()
        if fruit:
            print(f"フルーツ詳細:")
            print(f"  ID: {fruit[0]}")
            print(f"  名前: {fruit[1]}")
            print(f"  価格: {fruit[2]}円")
            print(f"  カテゴリ: {fruit[3] or 'なし'}")
            print(f"  説明: {fruit[4] or 'なし'}")
            print(f"  作成日: {fruit[5]}")
            print(f"  更新日: {fruit[6]}")
        else:
            print(f"NG ID {fruit_id} のフルーツが見つかりません")
        return fruit
    except Exception as e:
        print(f"NG フルーツ取得エラー: {e}")
        return None
    finally:
        if conn:
            conn.close()

def search_fruits_by_name(name):
    """名前でフルーツを検索"""
    conn = None
    try:
        conn = sqlite3.connect('fruit_prices.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, price, category, description, created_at, updated_at
            FROM fruits
            WHERE name LIKE ?
            ORDER BY name
        ''', (f'%{name}%',))
        
        fruits = cursor.fetchall()
        print(f"'{name}' で検索結果（{len(fruits)}件）:")
        for fruit in fruits:
            print(f"  ID: {fruit[0]}, 名前: {fruit[1]}, 価格: {fruit[2]}円")
        return fruits
    except Exception as e:
        print(f"NG 検索エラー: {e}")
        return []
    finally:
        if conn:
            conn.close()

# UPDATE（更新）
def update_fruit(fruit_id, name=None, price=None, category=None, description=None):
    """フルーツ情報を更新"""
    conn = None
    try:
        conn = sqlite3.connect('fruit_prices.db')
        cursor = conn.cursor()
        
        # 更新するフィールドを動的に構築
        update_fields = []
        values = []
        
        if name is not None:
            update_fields.append("name = ?")
            values.append(name)
        if price is not None:
            update_fields.append("price = ?")
            values.append(price)
        if category is not None:
            update_fields.append("category = ?")
            values.append(category)
        if description is not None:
            update_fields.append("description = ?")
            values.append(description)
        
        if not update_fields:
            print("NG 更新する項目が指定されていません")
            return False
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(fruit_id)
        
        query = f"UPDATE fruits SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, values)
        
        if cursor.rowcount > 0:
            conn.commit()
            print(f"OK フルーツ ID {fruit_id} を更新しました")
            return True
        else:
            print(f"NG ID {fruit_id} のフルーツが見つかりません")
            return False
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"NG 更新エラー: {e}")
        return False
    finally:
        if conn:
            conn.close()

# DELETE（削除）
def delete_fruit(fruit_id):
    """フルーツを削除"""
    conn = None
    try:
        conn = sqlite3.connect('fruit_prices.db')
        cursor = conn.cursor()
        
        # 削除前に存在確認
        cursor.execute('SELECT name FROM fruits WHERE id = ?', (fruit_id,))
        fruit = cursor.fetchone()
        
        if not fruit:
            print(f"NG ID {fruit_id} のフルーツが見つかりません")
            return False
        
        cursor.execute('DELETE FROM fruits WHERE id = ?', (fruit_id,))
        conn.commit()
        
        print(f"OK フルーツ '{fruit[0]}' (ID: {fruit_id}) を削除しました")
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"NG 削除エラー: {e}")
        return False
    finally:
        if conn:
            conn.close()

def clear_all_fruits():
    """全てのフルーツを削除"""
    conn = None
    try:
        conn = sqlite3.connect('fruit_prices.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM fruits')
        conn.commit()
        print("OK 全てのフルーツを削除しました")
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"NG 全削除エラー: {e}")
        return False
    finally:
        if conn:
            conn.close()

# 統計情報
def get_fruit_statistics():
    """フルーツ統計情報を取得"""
    conn = None
    try:
        conn = sqlite3.connect('fruit_prices.db')
        cursor = conn.cursor()
        
        # 総数
        cursor.execute('SELECT COUNT(*) FROM fruits')
        total_count = cursor.fetchone()[0]
        
        # 平均価格
        cursor.execute('SELECT AVG(price) FROM fruits')
        avg_price = cursor.fetchone()[0]
        
        # 最高価格
        cursor.execute('SELECT MAX(price) FROM fruits')
        max_price = cursor.fetchone()[0]
        
        # 最低価格
        cursor.execute('SELECT MIN(price) FROM fruits')
        min_price = cursor.fetchone()[0]
        
        print("フルーツ統計情報:")
        print(f"  総数: {total_count}件")
        if avg_price:
            print(f"  平均価格: {avg_price:.0f}円")
            print(f"  最高価格: {max_price}円")
            print(f"  最低価格: {min_price}円")
        
        return {
            'total_count': total_count,
            'avg_price': avg_price,
            'max_price': max_price,
            'min_price': min_price
        }
    except Exception as e:
        print(f"NG 統計取得エラー: {e}")
        return None
    finally:
        if conn:
            conn.close()

# データベース初期化を実行
if __name__ == "__main__":
    init_fruit_database()
