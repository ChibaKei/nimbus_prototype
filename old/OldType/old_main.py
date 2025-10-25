import heaven
import town
import ekichika
import delija
import fuja
import shake_town
import shake_ekichika
import time
import datetime
import random
import threading
import utilites
import schedule
import diary_reprint
import vanilla
import shake_vanilla
import blog_db
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import platform

# Windows対応のロック機能
if platform.system() == "Windows":
    import msvcrt
else:
    import fcntl

# プロセスレベルのロックファイル
if platform.system() == "Windows":
    LOCK_FILE = os.path.join(os.getenv('TEMP', ''), 'auto_kitene.lock')
else:
    LOCK_FILE = "/tmp/auto_kitene.lock"
lock_fd = None

# ログ設定
def setup_logging():
    """統一されたログシステムを設定"""
    # ログフォーマットを定義
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # ログレベルを設定
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # コンソール出力
            logging.StreamHandler(sys.stdout),
            # ファイル出力（ローテーション付き）
            RotatingFileHandler(
                'auto_kitene.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )
    
    return logging.getLogger('AutoKitene')

# グローバルロガー
logger = setup_logging()

# urllib3のログレベルを調整（接続エラーの警告を抑制）
logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)

def log_info(message, thread_name=None):
    """情報ログを出力"""
    if thread_name:
        logger.info(f"[{thread_name}] {message}")
    else:
        logger.info(message)

def log_error(message, thread_name=None, exception=None):
    """エラーログを出力"""
    if thread_name:
        if exception:
            logger.error(f"[{thread_name}] {message}: {exception}")
        else:
            logger.error(f"[{thread_name}] {message}")
    else:
        if exception:
            logger.error(f"{message}: {exception}")
        else:
            logger.error(message)

def log_warning(message, thread_name=None):
    """警告ログを出力"""
    if thread_name:
        logger.warning(f"[{thread_name}] {message}")
    else:
        logger.warning(message)

def log_debug(message, thread_name=None):
    """デバッグログを出力"""
    if thread_name:
        logger.debug(f"[{thread_name}] {message}")
    else:
        logger.debug(message)

def acquire_process_lock():
    """プロセスレベルのロックを取得"""
    global lock_fd
    try:
        lock_fd = os.open(LOCK_FILE, os.O_CREAT | os.O_WRONLY | os.O_TRUNC)
        if platform.system() == "Windows":
            # Windowsではmsvcrtを使用
            msvcrt.locking(lock_fd, msvcrt.LK_NBLCK, 1)
        else:
            # Unix系ではfcntlを使用
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        log_info("プロセスロックを取得しました")
        return True
    except (OSError, IOError) as e:
        log_error("既に別のプロセスが実行中です", exception=e)
        return False

def release_process_lock():
    """プロセスレベルのロックを解放"""
    global lock_fd
    if lock_fd:
        try:
            if platform.system() == "Windows":
                # Windowsではmsvcrtを使用
                msvcrt.locking(lock_fd, msvcrt.LK_UNLCK, 1)
            os.close(lock_fd)
            os.unlink(LOCK_FILE)
            log_info("プロセスロックを解放しました")
        except Exception as e:
            log_error("ロック解放エラー", exception=e)

# スレッド管理クラス
class ThreadManager:
    def __init__(self):
        self.threads = {}
        self.locks = {}
        self.running_states = {}
        self.main_lock = threading.Lock()
    
    def get_thread_lock(self, thread_name):
        """スレッド用のロックを取得"""
        if thread_name not in self.locks:
            self.locks[thread_name] = threading.Lock()
        return self.locks[thread_name]
    
    def is_thread_running(self, thread_name):
        """スレッドが実行中かチェック"""
        with self.main_lock:
            return self.running_states.get(thread_name, False)
    
    def set_thread_running(self, thread_name, running):
        """スレッドの実行状態を設定"""
        with self.main_lock:
            self.running_states[thread_name] = running
    
    def start_thread(self, name, target, daemon=False):
        """スレッドを安全に開始"""
        with self.main_lock:
            if name in self.threads and self.threads[name].is_alive():
                log_warning(f"スレッド {name} は既に実行中です")
                return False
            
            thread = threading.Thread(target=target, name=name, daemon=daemon)
            self.threads[name] = thread
            thread.start()
            log_info(f"スレッド {name} を開始しました")
            return True

# グローバルスレッド管理インスタンス
thread_manager = ThreadManager()

def safe_thread_wrapper(thread_name, target_func):
    """スレッドを安全に実行するラッパー"""
    def wrapper():
        thread_lock = thread_manager.get_thread_lock(thread_name)
        
        with thread_lock:
            if thread_manager.is_thread_running(thread_name):
                log_warning(f"{thread_name} は既に実行中です。スキップします。", thread_name)
                return
            
            thread_manager.set_thread_running(thread_name, True)
        
        try:
            log_info(f"{thread_name} 開始", thread_name)
            target_func()
        except Exception as e:
            log_error(f"{thread_name} でエラー", thread_name, e)
        finally:
            thread_manager.set_thread_running(thread_name, False)
            log_info(f"{thread_name} 終了", thread_name)
    
    return wrapper

def town_pickupper():
    i = 3
    j = 1
    while True:
        try:
            town_count = town.town_pickup(get_count=True)
            shake_town_count = shake_town.town_pickup(get_count=True)
            if town_count == 0:
                log_warning("タウンの数が0です。待機中...", "town_pickupper")
                time.sleep(1800)  # 30分待機
                continue
            
            gcount_delay = 60 / town_count
            i += 1
            next_run_time = utilites.get_random_delay(base_minutes=int(gcount_delay), rand_min_range=(0, 0), rand_sec_range=(1, 30))
            town.town_pickup(int=i)
            shake_town.town_pickup(int=j)
            
            log_info(f"{i}: タウンpickup実行", "town_pickupper")
            if i >= town_count:
                i = 0
            if j >= shake_town_count:
                j = 1
            
            time.sleep(next_run_time.total_seconds())
        except Exception as e:
            log_error("town_pickupper でエラー", "town_pickupper", e)
            time.sleep(300)  # 5分待機してから再試行

def town_news_updater():
    i = 0
    j = 0
    while True:
        try:
            i += 1
            next_run_time = utilites.get_random_delay(base_minutes=20, rand_min_range=(1, 3), rand_sec_range=(10, 30))
            town.town_news(i)
            if j == 0:
                shake_town.town_news(i)
                j += 1
            elif j == 2:
                j = 0
            
            ekichika.ekichika_news()
            shake_ekichika.ekichika_news()
            log_info(f"{i}:タウン駅チカおしらせ実行", "town_news_updater")
            if i == 5:
                i = 0
            time.sleep((next_run_time).total_seconds())
        except Exception as e:
            log_error("town_news_updater でエラー", "town_news_updater", e)
            time.sleep(300)  # 5分待機してから再試行

def delija_news_updater():
    i = 0
    while True:
        try:
            i += 1
            next_run_time = utilites.get_random_delay(base_minutes=36, rand_min_range=(1, 3), rand_sec_range=(10, 30))
            delija.delija_news(i)
            fuja.fuja_news(i)
            log_info(f"{i}:デリじゃお知らせ実行", "delija_news_updater")
            if i == 5:
                i = 0
            time.sleep((next_run_time).total_seconds())
        except Exception as e:
            log_error("delija_news_updater でエラー", "delija_news_updater", e)
            time.sleep(300)  # 5分待機してから再試行

def heaven_updater():
    while True:
        try:
            heaven.heaven_update()
            log_info("Heaven上位更新", "heaven_updater")
            next_run_time = utilites.get_random_delay(base_minutes=44, rand_min_range=(1, 3), rand_sec_range=(10, 30))
            time.sleep((next_run_time).total_seconds())
        except Exception as e:
            log_error("heaven_updater でエラー", "heaven_updater", e)
            time.sleep(300)  # 5分待機してから再試行

def heaven_auto_kitene():
    start_time = time.time()
    gals_info = heaven.get_gals_info()
    gal_count = gals_info[0]
    failed_gal = []
    max_retries = 3

    for i in range(1,gal_count+1):
        retries = 0
        gal_info = gals_info[i]

        gal_name = gal_info[0]
        gal_id   = gal_info[1]
        gal_ps   = gal_info[2]
        while retries < max_retries:
            result = heaven.heaven_kitene2(gal_name,gal_id,gal_ps)
            if result == "done":
                #print(str(gal_name) + result)
                break
            else:
                #print("失敗:" + str(i) + result)
                retries += 1
                i -= 1
        if retries == max_retries:
            failed_gal.append(gal_name)

    if not failed_gal:
        log_info("Auto-Kiteneが正常終了しました。", "heaven_auto_kitene")
    else:
        log_warning("Auto-Kiteneが正常終了しました。以下が失敗者のリスト。姫デコログインしてみて、手動で実行推奨", "heaven_auto_kitene")
        for j in range(len(failed_gal)):
            log_info(f"失敗者: {failed_gal[j]}", "heaven_auto_kitene")
    end_time = time.time()
    execution_time = end_time - start_time
    log_info(f"実行時間: {execution_time:.2f}秒", "heaven_auto_kitene")

def ekichika_updater_and_delija_pickupper():
    while True:
        try:
            ekichika_delay = datetime.timedelta(minutes=48)
            ekichika.ekichika_pickup()
            time.sleep(1)
            shake_ekichika.ekichika_pickup()
            delija.delija_pickup()
            log_info(f"Delija即姫 次回: {ekichika_delay}", "ekichika_updater_and_delija_pickupper")
            fuja.fuja_pickup()
            log_info(f"Fuja即姫 次回: {ekichika_delay}", "ekichika_updater_and_delija_pickupper")
            
            time.sleep(ekichika_delay.total_seconds())
        except Exception as e:
            log_error("ekichika_updater_and_delija_pickupper でエラー", "ekichika_updater_and_delija_pickupper", e)
            time.sleep(300)  # 5分待機してから再試行

def ekichika_pickupper():
    while True:
        try:
            ekichika_delay_b = datetime.timedelta(minutes=15)
            ekichika.ekichika_gals_picup(ekichika.ekichika_gals_count())
            shake_ekichika.ekichika_gals_picup(shake_ekichika.ekichika_gals_count())
            log_info("駅チカピックアップ実行", "ekichika_pickupper")
            time.sleep(ekichika_delay_b.total_seconds())
        except Exception as e:
            log_error("ekichika_pickupper でエラー", "ekichika_pickupper", e)
            time.sleep(300)  # 5分待機してから再試行

def ekichika_pickupper2():
    i = 1
    source_num = 0
    target_num = 0
    while True:
        try:
            ekichika_delay_c = datetime.timedelta(minutes=10)
            count = ekichika.ekichika_sokuiku_count()
            
            now_gal_count = count[0]
            gal_count = count[1]
            
            if gal_count <= 1:
                i = 1
            elif i >= gal_count:
                i = 1
            elif source_num >= gal_count:
                i = 1 

            if now_gal_count >= gal_count: 
                log_info("即イク最大人数のためスキップ", "ekichika_pickupper2")
                time.sleep(ekichika_delay_c.total_seconds())
            elif gal_count == 0:
                log_info("即イク出勤人数0のため1時間スキップ", "ekichika_pickupper2")
                time.sleep(ekichika_delay_c.total_seconds() + 600)
            elif now_gal_count == 5:
                log_info("即イク最大人数のためスキップ", "ekichika_pickupper2")
                time.sleep(120)
            else:
                log_info("駅チカ即イク実行", "ekichika_pickupper2")
                source_num = now_gal_count + i
                target_num = now_gal_count + 1
                ekichika.ekichika_sokuiku(source_num,target_num)
                i += 1
                time.sleep(ekichika_delay_c.total_seconds())
        except Exception as e:
            log_error("ekichika_pickupper2 でエラー", "ekichika_pickupper2", e)
            time.sleep(300)  # 5分待機してから再試行

def ekichika_pickupper3():
    i = 1
    source_num = 0
    target_num = 0
    while True:
        try:
            ekichika_delay_c = datetime.timedelta(minutes=10)
            count = shake_ekichika.ekichika_sokuiku_count()
            
            now_gal_count = count[0]
            gal_count = count[1]
            
            if gal_count <= 1:
                i = 1
            elif i >= gal_count:
                i = 1
            elif source_num >= gal_count:
                i = 1 

            if now_gal_count >= gal_count: 
                log_info("即イク最大人数のためスキップ", "ekichika_pickupper3")
                time.sleep(ekichika_delay_c.total_seconds())
            elif gal_count == 0:
                log_info("即イク出勤人数0のため1時間スキップ", "ekichika_pickupper3")
                time.sleep(ekichika_delay_c.total_seconds() + 600)
            elif now_gal_count == 5:
                log_info("即イク最大人数のためスキップ", "ekichika_pickupper3")
                time.sleep(120)
            else:
                log_info("駅チカ即イク実行", "ekichika_pickupper3")
                source_num = now_gal_count + i
                target_num = now_gal_count + 1
                shake_ekichika.ekichika_sokuiku(source_num,target_num)
                i += 1
                time.sleep(ekichika_delay_c.total_seconds())
        except Exception as e:
            log_error("ekichika_pickupper3 でエラー", "ekichika_pickupper3", e)
            time.sleep(300)  # 5分待機してから再試行

# Schedullerの実行状態を管理するロック
scheduller_lock = threading.Lock()
scheduller_running = False

def scheduller():
    global scheduller_running
    
    # 既に実行中の場合はスキップ
    with scheduller_lock:
        if scheduller_running:
            log_warning("Schedullerは既に実行中です。スキップします。", "scheduller")
            return
        scheduller_running = True
    
    try:
        log_info("Scheduller開始", "scheduller")
        
        # Heavenのスケジュールデータを取得
        shift_data = heaven.get_heaven_schedule()
        if not shift_data:
            log_error("Heavenのスケジュールデータが取得できませんでした", "scheduller")
            return
        
        # タウンのスケジュール設定
        try:
            town.set_town_schedule(shift_data)
            log_info("タウン shift done", "scheduller")
        except Exception as e:
            log_error("タウン shift エラー", "scheduller", e)
        
        # デリじゃのスケジュール設定
        try:
            cast_cont_for_delija = utilites.format_shift_to_delija(shift_data)
            delija.set_delija_schedule(cast_cont_for_delija)
            log_info("デリじゃ shift done", "scheduller")
        except Exception as e:
            log_error("デリじゃ shift エラー", "scheduller", e)
        
        # ふうじゃのスケジュール設定
        try:
            fuja.set_fuja_schedule(shift_data)
            log_info("ふうじゃ shift done", "scheduller")
        except Exception as e:
            log_error("ふうじゃ shift エラー", "scheduller", e)
        
        # 駅チカのスケジュール設定
        """try:
            cast_cont_for_ekichika = ekichika.convert_shift_to_ekichika(shift_data)
            ekichika.set_ekichika_schedule(cast_cont_for_ekichika)
            log_info("駅チカ shift done", "scheduller")
        except Exception as e:
            log_error("駅チカ shift エラー", "scheduller", e)"""
        
        log_info("Scheduller完了", "scheduller")
        
    except Exception as e:
        log_error("Scheduller全体でエラー", "scheduller", e)
    finally:
        # 実行状態をリセット
        with scheduller_lock:
            scheduller_running = False

    
def patrol():
    while True:
        try:
            log_info("パトロール開始", "patrol")
            basedelay = datetime.timedelta(minutes=60)
            next_run_time = basedelay.total_seconds()

            # AとBの比較結果を取得
            cont = diary_reprint.diary_compare()

            if not cont:
                log_info("抜けなし！", "patrol")
            else:
                log_info(f"新しい記事を発見しました: {utilites.array_to_text(cont)}", "patrol")
                
                # 10分待機して再比較
                time.sleep(600)  # 10分待機
                updated_cont = diary_reprint.diary_compare()
                if not updated_cont:
                    log_warning("元記事が削除された？", "patrol")
                else:
                    # 再比較で確定した差分のみを転記
                    final_diff = [
                        entry for entry in cont
                        if entry in updated_cont
                    ]

                    if final_diff:
                        log_info(f"転記対象が確定しました: {utilites.array_to_text(final_diff)}", "patrol")

                        for entry in final_diff:
                            cast, title = entry[0], entry[1]  # castとtitleを抽出
                            # 転記処理を呼び出し
                            diary_reprint.diary_save_and_submit(cast, title)
                            log_info(f"転記成功: {cast}, {title}", "patrol")
                            

            # 次のチェックまで待機
            log_info("パトロール待機", "patrol")
            time.sleep(next_run_time)
        except Exception as e:
            log_error("patrol でエラー", "patrol", e)
            time.sleep(300)  # 5分待機してから再試行

def post_template_job():
    """1時間ごとにIDを順番に増やしながら記事を投稿するジョブ"""
    
    # データベースから記事数を取得
    blogs = blog_db.get_all_blogs()
    max_article_id = len(blogs) if blogs else 1
    article_id = random.randint(1, max_article_id)
    
    while True:
        try:
            # 記事を投稿
            title = vanilla.post_template(article_id)
            
            if title:
                log_info(f"記事ID {article_id} を投稿しました: {title}", "post_template_job")
                article_id += 1  # 次のIDに進む
                
                # 記事数を再取得して最大値を更新
                blogs = blog_db.get_all_blogs()
                max_article_id = len(blogs) if blogs else 1
                
                # 最大IDを超えた場合は1に戻す
                if article_id > max_article_id:
                    article_id = 1
            else:
                log_warning(f"記事ID {article_id} の投稿に失敗しました。ランダムIDで再試行します。", "post_template_job")
                # ランダムIDで再試行
                blogs = blog_db.get_all_blogs()
                max_article_id = len(blogs) if blogs else 1
                article_id = random.randint(1, max_article_id)
            
        except Exception as e:
            log_error("投稿中にエラーが発生しました。ランダムIDで再試行します。", "post_template_job", e)
            # エラー時もランダムIDで再試行
            blogs = blog_db.get_all_blogs()
            max_article_id = len(blogs) if blogs else 1
            article_id = random.randint(1, max_article_id)
        
        # 1時間待機
        log_info(f"次の投稿まで1時間待機します... (次回ID: {article_id})", "post_template_job")
        time.sleep(3600)  # 1時間待機

def post_shake_template_job():
    """shake_vanilla用の1時間ごとにIDを順番に増やしながら記事を投稿するジョブ"""
    
    # データベースから記事数を取得
    shake_blogs = blog_db.get_all_shake_blogs()
    max_article_id = len(shake_blogs) if shake_blogs else 1
    article_id = random.randint(1, max_article_id)
    
    while True:
        try:
            # 記事を投稿
            title = shake_vanilla.post_template(article_id)
            
            if title:
                log_info(f"Shake記事ID {article_id} を投稿しました: {title}", "post_shake_template_job")
                article_id += 1  # 次のIDに進む
                
                # 記事数を再取得して最大値を更新
                shake_blogs = blog_db.get_all_shake_blogs()
                max_article_id = len(shake_blogs) if shake_blogs else 1
                
                # 最大IDを超えた場合は1に戻す
                if article_id > max_article_id:
                    article_id = 1
            else:
                log_warning(f"Shake記事ID {article_id} の投稿に失敗しました。ランダムIDで再試行します。", "post_shake_template_job")
                # ランダムIDで再試行
                shake_blogs = blog_db.get_all_shake_blogs()
                max_article_id = len(shake_blogs) if shake_blogs else 1
                article_id = random.randint(1, max_article_id)
            
        except Exception as e:
            log_error("Shake投稿中にエラーが発生しました。ランダムIDで再試行します。", "post_shake_template_job", e)
            # エラー時もランダムIDで再試行
            shake_blogs = blog_db.get_all_shake_blogs()
            max_article_id = len(shake_blogs) if shake_blogs else 1
            article_id = random.randint(1, max_article_id)
        
        # 1時間待機
        log_info(f"Shake次の投稿まで1時間待機します... (次回ID: {article_id})", "post_shake_template_job")
        time.sleep(3600)  # 1時間待機

def safe_job(job_func, name=None):
    """ジョブを安全に実行し、ログを出力"""
    def wrapper():
        job_name = name or getattr(job_func, '__name__', 'unknown')
        try:
            log_info(f"Running job: {job_name}", "schedule")

            job_func()
        except Exception as e:
            log_error(f"Error in job {job_name}", "schedule", e)
    return wrapper

def setup_schedule():
    """スケジュールを一度だけ設定する関数"""
    if hasattr(setup_schedule, 'configured'):
        log_info("スケジュールは既に設定済みです", "setup_schedule")
        return
    
    log_info("スケジュールを設定中...", "setup_schedule")
    
    # 既存のスケジュールをクリア
    schedule.clear()
    
    # スケジュールを登録
    schedule.every().day.at("06:30").do(safe_job(heaven.heaven_opening, "heaven_opening"))
    schedule.every().day.at("03:00").do(safe_job(scheduller, "Scheduller"))
    schedule.every().day.at("09:00").do(safe_job(scheduller, "Scheduller"))
    schedule.every().day.at("13:00").do(safe_job(scheduller, "Scheduller"))
    schedule.every().day.at("18:00").do(safe_job(scheduller, "Scheduller"))
    schedule.every().day.at("21:00").do(safe_job(scheduller, "Scheduller"))
    #schedule.every().day.at("08:00").do(safe_job(heaven_auto_kitene, "heaven_auto_kitene"))
    
    setup_schedule.configured = True
    log_info("スケジュール設定完了", "setup_schedule")

def schedule_runner():
    """スケジュール処理を実行するスレッド"""
    while True:
        schedule.run_pending()
        time.sleep(1)  # 1秒ごとにスケジュールをチェック

if __name__ == "__main__":
    
    # プロセスロックを取得
    if not acquire_process_lock():
        log_error("既に別のプロセスが実行中です。終了します。")
        sys.exit(1)
    
    try:
        log_info("Auto-Kitene システムを開始します")
        
        # スケジュールを設定（重複防止）
        setup_schedule()

        # スケジュール管理用のスレッドを作成・開始
        thread_manager.start_thread("schedule_runner", schedule_runner, daemon=True)

        # 他のスレッドを安全に開始
        thread_manager.start_thread("town_pickupper", safe_thread_wrapper("town_pickupper", town_pickupper))
        thread_manager.start_thread("heaven_updater", safe_thread_wrapper("heaven_updater", heaven_updater))
        thread_manager.start_thread("town_news_updater", safe_thread_wrapper("town_news_updater", town_news_updater))
        thread_manager.start_thread("ekichika_updater_and_delija_pickupper", safe_thread_wrapper("ekichika_updater_and_delija_pickupper", ekichika_updater_and_delija_pickupper))
        thread_manager.start_thread("ekichika_pickupper", safe_thread_wrapper("ekichika_pickupper", ekichika_pickupper))
        thread_manager.start_thread("ekichika_pickupper2", safe_thread_wrapper("ekichika_pickupper2", ekichika_pickupper2))
        thread_manager.start_thread("ekichika_pickupper3", safe_thread_wrapper("ekichika_pickupper3", ekichika_pickupper3))
        thread_manager.start_thread("delija_news_updater", safe_thread_wrapper("delija_news_updater", delija_news_updater))
        thread_manager.start_thread("patrol", safe_thread_wrapper("patrol", patrol))
        thread_manager.start_thread("post_template_job", safe_thread_wrapper("post_template_job", post_template_job))
        thread_manager.start_thread("post_shake_template_job", safe_thread_wrapper("post_shake_template_job", post_shake_template_job))

        log_info("全てのスレッドを開始しました")
        
        # メインスレッドを待機
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            log_info("システムを停止します...")
            
    except Exception as e:
        log_error("メイン処理でエラー", exception=e)
    finally:
        # プロセスロックを解放
        release_process_lock()
        log_info("システムを終了しました")