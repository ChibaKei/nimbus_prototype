import sqlite3
from datetime import datetime

def init_database():
    """データベースの初期化（テーブル作成）"""
    conn = None
    try:
        conn = sqlite3.connect('nimbus.db')
        cursor = conn.cursor()
        # キャスト情報テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cast_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cast_name TEXT NOT NULL,
                pdeco_state TEXT NOT NULL,
                pdeco_id TEXT,
                pdeco_password TEXT,
                pdeco_url TEXT,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # ヘブンスケジュール用テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS heaven_schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gal_name TEXT NOT NULL,
                day1_start TEXT, day1_end TEXT,
                day2_start TEXT, day2_end TEXT,
                day3_start TEXT, day3_end TEXT,
                day4_start TEXT, day4_end TEXT,
                day5_start TEXT, day5_end TEXT,
                day6_start TEXT, day6_end TEXT,
                day7_start TEXT, day7_end TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def add_heaven_schedule(gal_name, schedule_data):
    """ヘブンスケジュールを追加"""
    conn = None
    try:
        conn = sqlite3.connect('nimbus.db')
        cursor = conn.cursor()
        
        # 既存のスケジュールを削除（同じガールの古いデータを削除）
        cursor.execute('DELETE FROM heaven_schedules WHERE gal_name = ?', (gal_name,))
        
        # 新しいスケジュールを挿入
        cursor.execute('''
            INSERT INTO heaven_schedules (
                gal_name, day1_start, day1_end, day2_start, day2_end,
                day3_start, day3_end, day4_start, day4_end,
                day5_start, day5_end, day6_start, day6_end,
                day7_start, day7_end
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            gal_name,
            schedule_data[0][0] if len(schedule_data) > 0 else None,  # day1_start
            schedule_data[0][1] if len(schedule_data) > 0 else None,  # day1_end
            schedule_data[1][0] if len(schedule_data) > 1 else None,  # day2_start
            schedule_data[1][1] if len(schedule_data) > 1 else None,  # day2_end
            schedule_data[2][0] if len(schedule_data) > 2 else None,  # day3_start
            schedule_data[2][1] if len(schedule_data) > 2 else None,  # day3_end
            schedule_data[3][0] if len(schedule_data) > 3 else None,  # day4_start
            schedule_data[3][1] if len(schedule_data) > 3 else None,  # day4_end
            schedule_data[4][0] if len(schedule_data) > 4 else None,  # day5_start
            schedule_data[4][1] if len(schedule_data) > 4 else None,  # day5_end
            schedule_data[5][0] if len(schedule_data) > 5 else None,  # day6_start
            schedule_data[5][1] if len(schedule_data) > 5 else None,  # day6_end
            schedule_data[6][0] if len(schedule_data) > 6 else None,  # day7_start
            schedule_data[6][1] if len(schedule_data) > 6 else None,  # day7_end
        ))
        
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"スケジュール保存エラー: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_all_heaven_schedules():
    """全てのヘブンスケジュールを取得"""
    conn = None
    try:
        conn = sqlite3.connect('nimbus.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, gal_name, day1_start, day1_end, day2_start, day2_end,
                   day3_start, day3_end, day4_start, day4_end,
                   day5_start, day5_end, day6_start, day6_end,
                   day7_start, day7_end, created_at
            FROM heaven_schedules
            ORDER BY created_at DESC
        ''')
        
        return cursor.fetchall()
    finally:
        if conn:
            conn.close()

def clear_heaven_schedules():
    """全てのヘブンスケジュールを削除"""
    conn = None
    try:
        conn = sqlite3.connect('nimbus.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM heaven_schedules')
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"スケジュール削除エラー: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_heaven_schedule(gal_name):
    """指定されたキャストのスケジュールを取得"""
    conn = None
    try:
        conn = sqlite3.connect('nimbus.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT day1_start, day1_end, day2_start, day2_end,
                   day3_start, day3_end, day4_start, day4_end,
                   day5_start, day5_end, day6_start, day6_end,
                   day7_start, day7_end
            FROM heaven_schedules
            WHERE gal_name = ?
            ORDER BY created_at DESC
            LIMIT 1
        ''', (gal_name,))
        
        result = cursor.fetchone()
        if result:
            # データベースの形式をスケジュール配列に変換
            schedule_data = []
            for i in range(0, 14, 2):  # 7日分のデータを処理
                start_time = result[i] if result[i] else ""
                end_time = result[i + 1] if result[i + 1] else ""
                schedule_data.append([start_time, end_time])
            return schedule_data
        return None
    except Exception as e:
        print(f"スケジュール取得エラー: {e}")
        return None
    finally:
        if conn:
            conn.close()

def compare_schedules(old_schedule, new_schedule):
    """2つのスケジュールを比較して変更があるかチェック"""
    if not old_schedule or not new_schedule:
        return old_schedule != new_schedule
    
    if len(old_schedule) != len(new_schedule):
        return True
    
    for i in range(len(old_schedule)):
        if old_schedule[i] != new_schedule[i]:
            return True
    
    return False

def update_heaven_schedule_if_changed(gal_name, new_schedule_data):
    """スケジュールを比較して変更があった場合のみ更新し、更新されたキャストリストを返す"""
    conn = None
    updated_casts = []
    
    try:
        conn = sqlite3.connect('nimbus.db')
        cursor = conn.cursor()
        
        # 既存のスケジュールを取得
        old_schedule = get_heaven_schedule(gal_name)
        
        # スケジュールを比較
        if compare_schedules(old_schedule, new_schedule_data):
            # 変更がある場合は更新
            cursor.execute('DELETE FROM heaven_schedules WHERE gal_name = ?', (gal_name,))
            
            cursor.execute('''
                INSERT INTO heaven_schedules (
                    gal_name, day1_start, day1_end, day2_start, day2_end,
                    day3_start, day3_end, day4_start, day4_end,
                    day5_start, day5_end, day6_start, day6_end,
                    day7_start, day7_end
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                gal_name,
                new_schedule_data[0][0] if len(new_schedule_data) > 0 else None,
                new_schedule_data[0][1] if len(new_schedule_data) > 0 else None,
                new_schedule_data[1][0] if len(new_schedule_data) > 1 else None,
                new_schedule_data[1][1] if len(new_schedule_data) > 1 else None,
                new_schedule_data[2][0] if len(new_schedule_data) > 2 else None,
                new_schedule_data[2][1] if len(new_schedule_data) > 2 else None,
                new_schedule_data[3][0] if len(new_schedule_data) > 3 else None,
                new_schedule_data[3][1] if len(new_schedule_data) > 3 else None,
                new_schedule_data[4][0] if len(new_schedule_data) > 4 else None,
                new_schedule_data[4][1] if len(new_schedule_data) > 4 else None,
                new_schedule_data[5][0] if len(new_schedule_data) > 5 else None,
                new_schedule_data[5][1] if len(new_schedule_data) > 5 else None,
                new_schedule_data[6][0] if len(new_schedule_data) > 6 else None,
                new_schedule_data[6][1] if len(new_schedule_data) > 6 else None,
            ))
            
            conn.commit()
            updated_casts.append(gal_name)
            print(f"✓ {gal_name}のスケジュールを更新しました")
        else:
            print(f"- {gal_name}のスケジュールに変更はありません")
        
        return updated_casts
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"スケジュール更新エラー ({gal_name}): {e}")
        return updated_casts
    finally:
        if conn:
            conn.close()

def batch_update_heaven_schedules(schedule_data_list):
    """複数のスケジュールを一括で比較・更新し、更新されたキャストリストを返す"""
    all_updated_casts = []
    
    for cast_name, schedule_data in schedule_data_list:
        updated_casts = update_heaven_schedule_if_changed(cast_name, schedule_data)
        all_updated_casts.extend(updated_casts)
    
    return all_updated_casts

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

# データベース初期化を実行
init_database() 