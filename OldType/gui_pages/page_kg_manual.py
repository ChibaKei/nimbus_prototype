# ボタン
upload_button = ft.ElevatedButton(
    "画像を選択",
    icon=ft.icons.UPLOAD_FILE,
    on_click=on_upload_click
)

save_button = ft.ElevatedButton(
    "設定を保存",
    icon=ft.icons.SAVE,
    on_click=save_config_click
)

run_button = ft.ElevatedButton(
    "自動化実行",
    icon=ft.icons.PLAY_ARROW,
    on_click=run_auto_click
)

# Homeに戻るボタン
home_button = ft.ElevatedButton(
    "Homeに戻る",
    icon=ft.icons.HOME,
    on_click=lambda _: page.go("/")
)

# メインのレイアウト
return ft.Column([
    ft.Text("キテネギフト手動入力", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
    ft.Divider(),
    gift_name,
    gift_price,
    gift_description,
    ft.Row([
        upload_button,
        save_button,
        run_button,
        home_button
    ], alignment=ft.MainAxisAlignment.START),
    status_text,
    image_preview
]) 