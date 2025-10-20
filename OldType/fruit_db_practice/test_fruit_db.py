#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
フルーツ価格データベースのテストファイル
CRUD操作の動作確認用
"""

import fruit_db

def test_crud_operations():
    """CRUD操作のテストを実行"""
    print("=" * 50)
    print("フルーツ価格データベース CRUD操作テスト")
    print("=" * 50)
    
    # データベース初期化
    print("\n1. データベース初期化")
    fruit_db.init_fruit_database()
    
    # CREATE（作成）テスト
    print("\n2. CREATE（作成）テスト")
    print("-" * 30)
    
    # フルーツを追加
    fruit_db.add_fruit("りんご", 150, "果物", "甘くて美味しい赤いりんご")
    fruit_db.add_fruit("バナナ", 100, "果物", "黄色くて栄養豊富")
    fruit_db.add_fruit("オレンジ", 200, "柑橘類", "ビタミンC豊富")
    fruit_db.add_fruit("ぶどう", 300, "果物", "高級な巨峰")
    fruit_db.add_fruit("いちご", 400, "ベリー類", "甘酸っぱい春の味")
    
    # 重複追加テスト（エラーになるはず）
    fruit_db.add_fruit("りんご", 200, "果物", "重複テスト")
    
    # READ（読み取り）テスト
    print("\n3. READ（読み取り）テスト")
    print("-" * 30)
    
    # 全フルーツ取得
    all_fruits = fruit_db.get_all_fruits()
    
    # 特定のフルーツ取得
    print("\n特定のフルーツ取得（ID: 1）:")
    fruit_db.get_fruit_by_id(1)
    
    # 検索テスト
    print("\n名前検索テスト（'りんご'）:")
    fruit_db.search_fruits_by_name("りんご")
    
    print("\n名前検索テスト（'ん'）:")
    fruit_db.search_fruits_by_name("ん")
    
    # UPDATE（更新）テスト
    print("\n4. UPDATE（更新）テスト")
    print("-" * 30)
    
    # 価格更新
    fruit_db.update_fruit(1, price=180)
    
    # 名前とカテゴリ更新
    fruit_db.update_fruit(2, name="バナナ（熟成）", category="熟成果物")
    
    # 説明更新
    fruit_db.update_fruit(3, description="新鮮なオレンジ、朝摘み")
    
    # 更新後の確認
    print("\n更新後のフルーツ詳細:")
    fruit_db.get_fruit_by_id(1)
    fruit_db.get_fruit_by_id(2)
    
    # 統計情報
    print("\n5. 統計情報")
    print("-" * 30)
    fruit_db.get_fruit_statistics()
    
    # DELETE（削除）テスト
    print("\n6. DELETE（削除）テスト")
    print("-" * 30)
    
    # 特定のフルーツ削除
    fruit_db.delete_fruit(4)  # ぶどうを削除
    
    # 存在しないIDの削除テスト
    fruit_db.delete_fruit(999)
    
    # 削除後の確認
    print("\n削除後の全フルーツ一覧:")
    fruit_db.get_all_fruits()
    
    # 最終統計
    print("\n7. 最終統計")
    print("-" * 30)
    fruit_db.get_fruit_statistics()

def test_advanced_operations():
    """高度な操作のテスト"""
    print("\n" + "=" * 50)
    print("高度な操作テスト")
    print("=" * 50)
    
    # カテゴリ別の価格分析
    print("\nカテゴリ別分析:")
    all_fruits = fruit_db.get_all_fruits()
    
    categories = {}
    for fruit in all_fruits:
        category = fruit[3] or "未分類"
        price = fruit[2]
        
        if category not in categories:
            categories[category] = []
        categories[category].append(price)
    
    for category, prices in categories.items():
        if prices:
            avg_price = sum(prices) / len(prices)
            print(f"  {category}: 平均価格 {avg_price:.0f}円 ({len(prices)}件)")

def interactive_mode():
    """対話モード（手動テスト用）"""
    print("\n" + "=" * 50)
    print("対話モード")
    print("=" * 50)
    print("以下のコマンドが使用できます:")
    print("  add <名前> <価格> [カテゴリ] [説明] - フルーツ追加")
    print("  list - 全フルーツ表示")
    print("  get <ID> - 特定フルーツ表示")
    print("  search <名前> - 名前検索")
    print("  update <ID> <項目> <値> - 更新")
    print("  delete <ID> - 削除")
    print("  stats - 統計表示")
    print("  quit - 終了")
    
    while True:
        try:
            command = input("\nコマンドを入力してください: ").strip().split()
            if not command:
                continue
                
            if command[0] == "quit":
                break
            elif command[0] == "add" and len(command) >= 3:
                name = command[1]
                price = int(command[2])
                category = command[3] if len(command) > 3 else None
                description = command[4] if len(command) > 4 else None
                fruit_db.add_fruit(name, price, category, description)
            elif command[0] == "list":
                fruit_db.get_all_fruits()
            elif command[0] == "get" and len(command) >= 2:
                fruit_id = int(command[1])
                fruit_db.get_fruit_by_id(fruit_id)
            elif command[0] == "search" and len(command) >= 2:
                name = command[1]
                fruit_db.search_fruits_by_name(name)
            elif command[0] == "update" and len(command) >= 4:
                fruit_id = int(command[1])
                field = command[2]
                value = command[3]
                
                if field == "name":
                    fruit_db.update_fruit(fruit_id, name=value)
                elif field == "price":
                    fruit_db.update_fruit(fruit_id, price=int(value))
                elif field == "category":
                    fruit_db.update_fruit(fruit_id, category=value)
                elif field == "description":
                    fruit_db.update_fruit(fruit_id, description=value)
                else:
                    print("無効な項目です。name, price, category, description のいずれか")
            elif command[0] == "delete" and len(command) >= 2:
                fruit_id = int(command[1])
                fruit_db.delete_fruit(fruit_id)
            elif command[0] == "stats":
                fruit_db.get_fruit_statistics()
            else:
                print("無効なコマンドです。help でヘルプを表示")
        except ValueError:
            print("数値が必要な箇所で無効な値が入力されました")
        except KeyboardInterrupt:
            print("\n終了します")
            break
        except Exception as e:
            print(f"エラー: {e}")

if __name__ == "__main__":
    # 自動テスト実行
    test_crud_operations()
    
    # 高度な操作テスト
    test_advanced_operations()
    
    # 対話モード（オプション）
    print("\n対話モードを開始しますか？ (y/n): ", end="")
    try:
        if input().lower().startswith('y'):
            interactive_mode()
    except KeyboardInterrupt:
        pass
    
    print("\nテスト完了！")
