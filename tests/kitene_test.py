import sys
import os
import traceback
import io

# Windows環境での文字化け対策
if sys.platform == "win32":
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import pdeco
from database import cast_db_manager


if __name__ == "__main__":
    try:
        print("キテネテスト開始", flush=True)
        print("キャスト情報を取得中...", flush=True)
        infos = cast_db_manager.get_casts_info()
        print(f"取得したキャスト数: {len(infos)}", flush=True)
        
        if not infos:
            print("キャスト情報が見つかりませんでした。", flush=True)
        else:
            success_count = 0
            fail_count = 0
            retry_count = 0
            skip_count = 0
            
            for i, info in enumerate(infos):
                cast_name = info[0]
                print(f"\n{'='*50}", flush=True)
                print(f"処理中 [{i+1}/{len(infos)}]: {cast_name}", flush=True)
                print(f"{'='*50}", flush=True)
                
                try:
                    result = pdeco.heaven_kitene(cast_name, max_retries=1)
                    print(f"結果: {result}", flush=True)
                    
                    if result == "done":
                        success_count += 1
                        print(f"✓ 成功: {cast_name}", flush=True)
                    elif result == "retry":
                        retry_count += 1
                        print(f"⚠ リトライ推奨: {cast_name}", flush=True)
                    else:
                        fail_count += 1
                        print(f"✗ 失敗: {cast_name} - {result}", flush=True)
                        
                except Exception as e:
                    fail_count += 1
                    print(f"✗ 例外発生: {cast_name} - {e}", flush=True)
                    traceback.print_exc()
            
            print(f"\n{'='*50}", flush=True)
            print("キテネテスト結果サマリー", flush=True)
            print(f"{'='*50}", flush=True)
            print(f"総キャスト数: {len(infos)}", flush=True)
            print(f"成功: {success_count}", flush=True)
            print(f"失敗: {fail_count}", flush=True)
            print(f"リトライ推奨: {retry_count}", flush=True)
            print(f"スキップ: {skip_count}", flush=True)
            print(f"{'='*50}", flush=True)
        
        print("\nキテネテスト完了", flush=True)
        
    except Exception as e:
        print(f"エラーが発生しました: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)
