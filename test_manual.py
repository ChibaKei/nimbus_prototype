import heaven
import nimbus_db_manager
import pdeco


#heaven.heaven_login("2510021932","i7Qt5Jnj",False)
#heaven.heaven_update("2510021932","i7Qt5Jnj",False)

# 最大7キャストまで処理
"""result = heaven.get_casts_info(max_casts=7)
print(f"取得結果: {result}")

# データベースに保存
if result != "failed":
    success = nimbus_db_manager.save_casts_info(result)
    if success:
        print("データベースへの保存が完了しました")
        
        # 保存されたデータを確認
        saved_data = nimbus_db_manager.get_casts_info()
        print(f"保存されたデータ: {len(saved_data)}件")
        for data in saved_data:
            print(data)
    else:
        print("データベースへの保存に失敗しました")"""

#pdeco.pdeco_login('あい', '61563696', '0316', False)
#print(pdeco.get_pdeco_easy_login('あい', '61563696', '0316', False))
"""infos = nimbus_db_manager.get_casts_info()
for info in infos:
    print(info)
    print(pdeco.get_pdeco_easy_login(info[0], info[2], info[3], False))"""
#print(pdeco.pdeco_easy_login('あい', False))
#print(pdeco.heaven_kitene('あいす'))
# 全キャストのスケジュールを取得・更新
print("=== 全キャストスケジュール更新開始 ===")
result = heaven.get_heaven_schedule(headless=True)

if result['success']:
    print(f"✓ スケジュール取得完了")
    print(f"総キャスト数: {result['total_casts']}")
    
    # DBにスケジュールを比較・更新
    print("\n=== データベース更新処理開始 ===")
    updated_casts = nimbus_db_manager.batch_update_heaven_schedules(result['schedule_data_list'])
    
    print(f"✓ DB更新完了")
    print(f"更新されたキャスト数: {len(updated_casts)}")
    
    if updated_casts:
        print(f"\n更新されたキャスト:")
        for i, cast_name in enumerate(updated_casts, 1):
            print(f"  {i}. {cast_name}")
    else:
        print("\n更新されたキャストはありません（全て同じスケジュール）")
    
    # 最初のキャストのスケジュールを表示（デバッグ用）
    if result['schedule_data_list']:
        first_cast = result['schedule_data_list'][0]
        print(f"\n=== サンプル（最初のキャスト） ===")
        print(f"キャスト名: {first_cast[0]}")
        print(f"スケジュール:")
        for i, day_schedule in enumerate(first_cast[1], 1):
            start_time = day_schedule[0] if day_schedule[0] else "休み"
            end_time = day_schedule[1] if day_schedule[1] else "休み"
            print(f"  日{i}: {start_time} - {end_time}")
else:
    print("✗ スケジュール取得に失敗しました")

print("\n=== 全キャストスケジュール更新完了 ===")