import sqlite3

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

# データベース初期化を実行
init_database()
