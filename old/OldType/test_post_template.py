import main
import time

if __name__ == "__main__":
    print("post_template_jobのテストを開始します...")
    try:
        # 1回だけ実行して動作確認
        main.post_template_job()
    except KeyboardInterrupt:
        print("\nテストを終了します。")
    except Exception as e:
        print(f"エラーが発生しました: {e}") 