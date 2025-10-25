import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import heaven
from database import heaven_schedule_db_manager

# 全キャストのスケジュールを取得・更新
print("=== 全キャストスケジュール更新開始 ===")
result = heaven.get_heaven_schedule(headless=True)

if result['success']:
    print(f"✓ スケジュール取得完了")
    print(f"総キャスト数: {result['total_casts']}")
    
    # DBにスケジュールを比較・更新
    print("\n=== データベース更新処理開始 ===")
    updated_casts = heaven_schedule_db_manager.batch_update_heaven_schedules(result['schedule_data_list'])
    
    print(f"✓ DB更新完了")
    print(f"更新されたキャスト数: {len(updated_casts)}")
    
    if updated_casts:
        print(f"\n更新されたキャスト:")
        for i, cast_name in enumerate(updated_casts, 1):
            print(f"  {i}. {cast_name}")
    else:
        print("\n更新されたキャストはありません（全て同じスケジュール）")
    
else:
    print("✗ スケジュール取得に失敗しました")

print("\n=== 全キャストスケジュール更新完了 ===")