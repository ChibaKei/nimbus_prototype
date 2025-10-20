import flet as ft
from flet import *
from blog_db import get_all_blogs, delete_blog
import os

def page_blog_manage(page: ft.Page):
    # 記事一覧を表示するリスト
    blog_list = ft.ListView(
        expand=True,
        spacing=5,  # カード間の間隔を縮小
        padding=10,  # パディングを縮小
        auto_scroll=True,
        height=page.window_height - 200
    )

    def load_blogs():
        blog_list.controls.clear()
        blogs = get_all_blogs()
        
        # IDの降順でソート
        blogs.sort(key=lambda x: x[0], reverse=True)
        
        for blog in blogs:
            id, title, content, image_path, created_at = blog
            
            # 画像がある場合は表示
            image = None
            if image_path and os.path.exists(image_path):
                image = ft.Image(
                    src=image_path,
                    width=60,  # 画像サイズを縮小
                    height=60,  # 画像サイズを縮小
                    fit=ft.ImageFit.COVER
                )
            
            # 記事カード
            card = ft.Card(
                content=ft.Container(
                    content=ft.Row([  # ColumnからRowに変更して横並びに
                        ft.Container(
                            content=image if image else ft.Text("画像なし"),
                            padding=5
                        ),
                        ft.Column([  # テキスト情報を縦に配置
                            ft.Text(f"ID: {id}", size=12, color=ft.colors.GREY),
                            ft.Text(title, size=16, weight=ft.FontWeight.BOLD),
                            ft.Row([  # ボタンを横に配置
                                ft.ElevatedButton(
                                    "編集",
                                    icon=ft.icons.EDIT,
                                    style=ft.ButtonStyle(
                                        padding=5,
                                        shape=ft.RoundedRectangleBorder(radius=5)
                                    ),
                                    on_click=lambda e, id=id: handle_edit(e, id)
                                ),
                                ft.ElevatedButton(
                                    "削除",
                                    icon=ft.icons.DELETE,
                                    style=ft.ButtonStyle(
                                        padding=5,
                                        shape=ft.RoundedRectangleBorder(radius=5)
                                    ),
                                    on_click=lambda e, id=id: handle_delete(e, id)
                                )
                            ])
                        ], spacing=2)  # 要素間の間隔を縮小
                    ]),
                    padding=5  # パディングを縮小
                )
            )
            blog_list.controls.append(card)
        page.update()

    def handle_edit(e, blog_id):
        # TODO: 編集機能の実装
        pass

    def handle_delete(e, blog_id):
        try:
            delete_blog(blog_id)
            load_blogs()  # 一覧を再読み込み
        except Exception as ex:
            print(f"削除に失敗しました: {ex}")

    # ブログ登録ページへの遷移ボタン
    register_button = ft.ElevatedButton(
        "ブログ登録ページ",
        icon=ft.icons.ADD,
        on_click=lambda _: page.go("/blog/register")
    )

    # Homeに戻るボタン
    home_button = ft.ElevatedButton(
        "Homeに戻る",
        icon=ft.icons.HOME,
        on_click=lambda _: page.go("/")
    )

    # 初期表示
    load_blogs()

    # レイアウト
    return ft.View(
        "/blog/manage",
        [
            ft.AppBar(
                title=ft.Text("ブログ管理"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[home_button]
            ),
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        register_button
                    ], alignment=ft.MainAxisAlignment.END),
                    blog_list
                ]),
                padding=20,
                expand=True
            )
        ]
    )

# 単体起動する場合
if __name__ == "__main__":
    ft.app(target=page_blog_manage) 