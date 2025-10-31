import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import heaven
from database import cast_db_manager

# 最大7キャストまで処理
result = heaven.get_pdeco_info(max_casts=20)
print(f"取得結果: {result}")

# データベースに保存
if result != "failed":
    success = cast_db_manager.save_casts_info(result)
    if success:
        print("データベースへの保存が完了しました")
        
        # 保存されたデータを確認
        saved_data = cast_db_manager.get_casts_info()
        print(f"保存されたデータ: {len(saved_data)}件")
        for data in saved_data:
            print(data)
    else:
        print("データベースへの保存に失敗しました")