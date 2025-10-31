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

from core import heaven, pdeco, town
from database import cast_db_manager, heaven_schedule_db_manager


#heaven.heaven_login("2510021932","i7Qt5Jnj",False)
#heaven.heaven_store_update("2510021932","i7Qt5Jnj",False)
#pdeco.pdeco_login('あい', '61563696', '0316', False)
#print(pdeco.get_pdeco_easy_login('あい', '61563696', '0316', False))
#print(pdeco.pdeco_easy_login('あい', False))
#print(pdeco.heaven_kitene('あいす'))


if __name__ == "__main__":
    try:
        print("スクリプト開始", flush=True)
        print("キャスト情報を取得中...", flush=True)
        infos = cast_db_manager.get_casts_info()
        print(f"取得したキャスト数: {len(infos)}", flush=True)
        
        if not infos:
            print("キャスト情報が見つかりませんでした。", flush=True)
        else:
            for i, info in enumerate(infos):
                print(f"処理中 [{i+1}/{len(infos)}]: {info}", flush=True)
                if len(info) >= 4:
                    try:
                        result = pdeco.get_pdeco_easy_login(info[0], info[2], info[3], False)
                        print(f"結果: {result}", flush=True)
                    except Exception as inner_e:
                        print(f"get_pdeco_easy_login でエラー: {inner_e}", flush=True)
                        traceback.print_exc()
                else:
                    print(f"エラー: キャスト情報の形式が不正です。要素数: {len(info)}", flush=True)
        print("スクリプト終了", flush=True)
    except Exception as e:
        print(f"エラーが発生しました: {e}", flush=True)
        traceback.print_exc()

#driver = town.town_login("dieselchiba@central-agent.co.jp", "dieselchiba", False)
#print(driver.current_url)
#town.town_cast_pickup(cast_index=8)