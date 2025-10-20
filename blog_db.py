import sqlite3
from datetime import datetime

def init_database():
    """データベースの初期化（テーブル作成）"""
    conn = None
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # 既存のテーブル（バニラ用）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS blog_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 新しいテーブル（shake_vanilla用）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shake_blog_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                image_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # ヘブンスケジュール用テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS heaven_schedules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gal_name TEXT NOT NULL,
                monday_start TEXT,
                monday_end TEXT,
                tuesday_start TEXT,
                tuesday_end TEXT,
                wednesday_start TEXT,
                wednesday_end TEXT,
                thursday_start TEXT,
                thursday_end TEXT,
                friday_start TEXT,
                friday_end TEXT,
                saturday_start TEXT,
                saturday_end TEXT,
                sunday_start TEXT,
                sunday_end TEXT,
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

# 既存のバニラ用関数
def add_blog(title, content, image_path=None):
    """ブログ記事を追加"""
    conn = None
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO blog_articles (title, content, image_path)
            VALUES (?, ?, ?)
        ''', (title, content, image_path))
        
        blog_id = cursor.lastrowid
        conn.commit()
        return blog_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def get_all_blogs():
    """全てのブログ記事を取得"""
    conn = None
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, content, image_path, created_at
            FROM blog_articles
            ORDER BY created_at DESC
        ''')
        
        return cursor.fetchall()
    finally:
        if conn:
            conn.close()

def get_blog_by_id(blog_id):
    """指定したIDのブログ記事を取得"""
    conn = None
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, content, image_path, created_at
            FROM blog_articles
            WHERE id = ?
        ''', (blog_id,))
        
        return cursor.fetchone()
    finally:
        if conn:
            conn.close()

def delete_blog(blog_id):
    """ブログ記事を削除"""
    conn = None
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM blog_articles WHERE id = ?', (blog_id,))
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

# shake_vanilla用の新しい関数
def add_shake_blog(title, content, image_path=None):
    """shake_vanilla用のブログ記事を追加"""
    conn = None
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO shake_blog_articles (title, content, image_path)
            VALUES (?, ?, ?)
        ''', (title, content, image_path))
        
        blog_id = cursor.lastrowid
        conn.commit()
        return blog_id
    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

def get_all_shake_blogs():
    """shake_vanilla用の全てのブログ記事を取得"""
    conn = None
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, content, image_path, created_at
            FROM shake_blog_articles
            ORDER BY created_at DESC
        ''')
        
        return cursor.fetchall()
    finally:
        if conn:
            conn.close()

def get_shake_blog_by_id(blog_id):
    """shake_vanilla用の指定したIDのブログ記事を取得"""
    conn = None
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, content, image_path, created_at
            FROM shake_blog_articles
            WHERE id = ?
        ''', (blog_id,))
        
        return cursor.fetchone()
    finally:
        if conn:
            conn.close()

def delete_shake_blog(blog_id):
    """shake_vanilla用のブログ記事を削除"""
    conn = None
    try:
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM shake_blog_articles WHERE id = ?', (blog_id,))
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
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        # 既存のスケジュールを削除（同じガールの古いデータを削除）
        cursor.execute('DELETE FROM heaven_schedules WHERE gal_name = ?', (gal_name,))
        
        # 新しいスケジュールを挿入
        cursor.execute('''
            INSERT INTO heaven_schedules (
                gal_name, monday_start, monday_end, tuesday_start, tuesday_end,
                wednesday_start, wednesday_end, thursday_start, thursday_end,
                friday_start, friday_end, saturday_start, saturday_end,
                sunday_start, sunday_end
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            gal_name,
            schedule_data[0][0] if len(schedule_data) > 0 else None,  # monday_start
            schedule_data[0][1] if len(schedule_data) > 0 else None,  # monday_end
            schedule_data[1][0] if len(schedule_data) > 1 else None,  # tuesday_start
            schedule_data[1][1] if len(schedule_data) > 1 else None,  # tuesday_end
            schedule_data[2][0] if len(schedule_data) > 2 else None,  # wednesday_start
            schedule_data[2][1] if len(schedule_data) > 2 else None,  # wednesday_end
            schedule_data[3][0] if len(schedule_data) > 3 else None,  # thursday_start
            schedule_data[3][1] if len(schedule_data) > 3 else None,  # thursday_end
            schedule_data[4][0] if len(schedule_data) > 4 else None,  # friday_start
            schedule_data[4][1] if len(schedule_data) > 4 else None,  # friday_end
            schedule_data[5][0] if len(schedule_data) > 5 else None,  # saturday_start
            schedule_data[5][1] if len(schedule_data) > 5 else None,  # saturday_end
            schedule_data[6][0] if len(schedule_data) > 6 else None,  # sunday_start
            schedule_data[6][1] if len(schedule_data) > 6 else None,  # sunday_end
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
        conn = sqlite3.connect('blog.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, gal_name, monday_start, monday_end, tuesday_start, tuesday_end,
                   wednesday_start, wednesday_end, thursday_start, thursday_end,
                   friday_start, friday_end, saturday_start, saturday_end,
                   sunday_start, sunday_end, created_at
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
        conn = sqlite3.connect('blog.db')
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

# データベース初期化を実行
init_database() 