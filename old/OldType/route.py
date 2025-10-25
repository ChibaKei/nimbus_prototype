import flet as ft
from flet import *
from gui_pages.page_home import home_view
from gui_pages.page_blog_register import page_blog_register
from gui_pages.page_blog_manage import page_blog_manage
from gui_pages.page_shake_blog_register import page_shake_blog_register
from gui_pages.page_shake_blog_manage import page_shake_blog_manage
from gui_pages.page_kg_auto import kg_auto_view
from gui_pages.page_okini_talk_auto import okini_talk_auto_view
from profile_create_main import pfc_view
# ここに他のページが追加される

def main(page: ft.Page):
    page.title = "Auto Kitene"
    page.window_width = 1200
    page.window_height = 1200
    page.window_resizable = True
    page.window_maximizable = True
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO

    # ルートの定義
    routes = {
        "/": home_view,
        "/blog/register": page_blog_register,
        "/blog/manage": page_blog_manage,
        "/shake_blog/register": page_shake_blog_register,
        "/shake_blog/manage": page_shake_blog_manage,
        "/kg/auto": kg_auto_view,
        "/okini_talk": okini_talk_auto_view,
        "/pfc": pfc_view,
    }

    def route_change(route):
        try:
            page.views.clear()
            if page.route == "/":
                page.views.append(routes[page.route](page))
            elif page.route in routes:
                page.views.append(routes[page.route](page))
            page.update()
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            # エラーを表示するためのビュー
            error_view = ft.View(
                page.route,
                [
                    ft.AppBar(title=ft.Text("エラー"), bgcolor=ft.colors.RED),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("ページの読み込み中にエラーが発生しました", size=20, color=ft.colors.RED),
                            ft.Text(f"エラー内容: {str(e)}", color=ft.colors.RED),
                            ft.ElevatedButton(
                                "Homeに戻る",
                                icon=ft.icons.HOME,
                                on_click=lambda _: page.go("/")
                            )
                        ]),
                        padding=20
                    )
                ]
            )
            page.views.append(error_view)
            page.update()

    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)