import flet as ft
from heaven import okini_talk_auto
import threading

def okini_talk_auto_view(page: ft.Page):
    page.title = "Okini Talk"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # 入力フィールド
    name_input = ft.TextField(
        label="キャスト名",
        autofocus=True,
        width=600,
        border=ft.InputBorder.UNDERLINE
    )

    content_input = ft.TextField(
        label="コンテンツ",
        multiline=True,
        expand=1,
        width=600,
        height=200,
        border=ft.InputBorder.UNDERLINE
    )

    # ステータスメッセージ
    status_text = ft.Text("", color=ft.Colors.RED)

    # フォーム送信ボタン
    def handle_submit(e):
        cast = name_input.value
        content = content_input.value

        if cast and content:
            # ボタンを無効化して処理中であることを示す
            submit_button.disabled = True
            submit_button.text = "処理中..."
            status_text.value = f"'{cast}'のオキニトーク自動化を開始しています..."
            status_text.color = ft.Colors.BLUE
            page.update()

            # 別スレッドで自動化処理を実行
            def run_automation():
                try:
                    okini_talk_auto(cast, content)
                    # 成功時の処理
                    page.clean()
                    status_text.value = f"'{cast}'のオキニトーク自動化が完了しました"
                    status_text.color = ft.Colors.GREEN
                except Exception as error:
                    # エラー時の処理
                    status_text.value = f"エラーが発生しました: {str(error)}"
                    status_text.color = ft.Colors.RED
                finally:
                    # ボタンを再度有効化
                    submit_button.disabled = False
                    submit_button.text = "送信"
                    page.update()

            # 別スレッドで実行
            thread = threading.Thread(target=run_automation)
            thread.daemon = True
            thread.start()
        else:
            status_text.value = "すべてのフィールドを入力してください。"
            status_text.color = ft.Colors.RED
            page.update()

    submit_button = ft.ElevatedButton(
        "送信",
        icon=ft.icons.SEND,
        on_click=handle_submit
    )

    # Homeに戻るボタン
    home_button = ft.ElevatedButton(
        "Homeに戻る",
        icon=ft.icons.HOME,
        on_click=lambda _: page.go("/")
    )

    # メインのレイアウト
    return ft.View(
        "/okini_talk",
        [
            ft.AppBar(
                title=ft.Text("オキニトーク自動化"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[home_button]
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("オキニトーク自動化", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Divider(),
                    name_input,
                    content_input,
                    ft.Row([
                        submit_button
                    ], alignment=ft.MainAxisAlignment.START),
                    status_text
                ]),
                padding=20
            )
        ]
    )

# 単体起動する場合
if __name__ == "__main__":
    ft.app(target=okini_talk_auto_view)
