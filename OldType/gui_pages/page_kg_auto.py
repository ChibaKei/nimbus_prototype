import flet as ft
from heaven import heaven_kg_auto
import threading

def kg_auto_view(page: ft.Page):
    page.title = "キテネギフト自動化"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # ステータスメッセージ
    status_text = ft.Text("", color=ft.Colors.RED)

    # 実行ボタン
    def run_auto_click(e):
        # ボタンを無効化して処理中であることを示す
        run_button.disabled = True
        run_button.text = "処理中..."
        status_text.value = "キテネギフト自動化を開始しています..."
        status_text.color = ft.Colors.BLUE
        page.update()

        # 別スレッドで自動化処理を実行
        def run_automation():
            try:
                heaven_kg_auto()
                # 成功時の処理
                status_text.value = "キテネギフト自動化が完了しました"
                status_text.color = ft.Colors.GREEN
            except Exception as error:
                # エラー時の処理
                status_text.value = f"エラーが発生しました: {str(error)}"
                status_text.color = ft.Colors.RED
            finally:
                # ボタンを再度有効化
                run_button.disabled = False
                run_button.text = "自動化実行"
                page.update()

        # 別スレッドで実行
        thread = threading.Thread(target=run_automation)
        thread.daemon = True
        thread.start()

    # 実行ボタン
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
    return ft.View(
        "/kg/auto",
        [
            ft.AppBar(
                title=ft.Text("キテネギフト自動化"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[home_button]
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("キテネギフト自動化", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Divider(),
                    ft.Text("この機能は、キテネギフトの自動化を実行します。", size=16, text_align=ft.TextAlign.CENTER),
                    ft.Text("ボタンを押すと自動で処理が開始されます。", size=14, text_align=ft.TextAlign.CENTER, color=ft.Colors.GREY),
                    ft.Divider(),
                    ft.Row([
                        run_button
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    status_text
                ]),
                padding=20
            )
        ]
    )

# 単体起動する場合
if __name__ == "__main__":
    ft.app(target=kg_auto_view)