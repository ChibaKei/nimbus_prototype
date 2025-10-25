import sqlite3
from .database_init import init_database

def save_casts_info(casts_data):
    """キャスト情報をデータベースに保存・更新
    
    Args:
        casts_data: get_casts_info()の戻り値 [[キャスト名, 状態, ID, パスワード], ...]
    
    Returns:
        bool: 保存成功時True
    """
    conn = None
    try:
        conn = sqlite3.connect('nimbus.db')
        cursor = conn.cursor()
        
        # 既存のデータを削除
        cursor.execute('DELETE FROM cast_info')
        
        # 新しいキャスト情報を挿入
        for cast_info in casts_data:
            if len(cast_info) >= 4:  # [キャスト名, 状態, ID, パスワード]の形式をチェック
                cursor.execute('''
                    INSERT INTO cast_info (cast_name, pdeco_state, pdeco_id, pdeco_password)
                    VALUES (?, ?, ?, ?)
                ''', (
                    cast_info[0],  # キャスト名
                    cast_info[1],  # 状態
                    cast_info[2],  # ID
                    cast_info[3]   # パスワード
                ))
        
        conn.commit()
        print(f"{len(casts_data)}件のキャスト情報を保存しました")
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"キャスト情報保存エラー: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_casts_info():
    """キャスト情報を取得
    
    Returns:
        list: キャスト情報のリスト
    """
    conn = None
    try:
        conn = sqlite3.connect('nimbus.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT cast_name, pdeco_state, pdeco_id, pdeco_password, created_at
            FROM cast_info
            ORDER BY cast_name
        ''')
        
        return cursor.fetchall()
        
    except Exception as e:
        print(f"キャスト情報取得エラー: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_cast_info(cast_name: str):
    """キャスト情報を取得
    
    Args:
        cast_name: キャスト名
    
    Returns:
        list: キャスト情報のリスト
    """
    conn = None
    try:
        conn = sqlite3.connect('nimbus.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM cast_info WHERE cast_name = ?', (cast_name,))
        return cursor.fetchone()
    except Exception as e:
        print(f"キャスト情報取得エラー: {e}")
        return []
    finally:
        if conn:
            conn.close()

def clear_casts_info():
    """キャスト情報を削除
    
    Returns:
        bool: 削除成功時True
    """
    conn = None
    try:
        conn = sqlite3.connect('nimbus.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM cast_info')
        conn.commit()
        print("キャスト情報を削除しました")
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"キャスト情報削除エラー: {e}")
        return False
    finally:
        if conn:
            conn.close()
