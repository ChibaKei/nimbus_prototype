#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import io

# Windows環境での文字化け対策
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("テスト開始", flush=True)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    print("モジュールインポート中...", flush=True)
    from database import cast_db_manager
    print("cast_db_manager インポート成功", flush=True)
    
    from core import pdeco
    print("pdeco インポート成功", flush=True)
    
    print("データベースから情報を取得中...", flush=True)
    infos = cast_db_manager.get_casts_info()
    print(f"取得したキャスト数: {len(infos)}", flush=True)
    
    if not infos:
        print("キャスト情報が見つかりませんでした。", flush=True)
        sys.exit(0)
    
    print(f"最初のキャストを処理: {infos[0]}", flush=True)
    if len(infos[0]) >= 4:
        print(f"キャスト名: {infos[0][0]}, ID: {infos[0][2]}, パスワード: {infos[0][3]}", flush=True)
        
except Exception as e:
    print(f"エラー: {e}", flush=True)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("テスト完了", flush=True)

