import heaven
import town
import ekichika
import delija
import time
import datetime
import random
import threading
import utilites
import schedule



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
            print(str(gal_name) + result)
            break
        else:
            print("失敗:" + str(i) + result)
            retries += 1
            i -= 1
    if retries == max_retries:
        failed_gal.append(gal_name)

if not failed_gal:
    print("Auto-Kiteneが正常終了しました。")
else:
    print("Auto-Kiteneが正常終了しました。以下が失敗者のリスト。姫デコログインしてみて、手動で実行推奨")
    for j in range(len(failed_gal)):
        print(failed_gal[j])
end_time = time.time()
execution_time = end_time - start_time
print(f"実行時間: {execution_time:.2f}秒")