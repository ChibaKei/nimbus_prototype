import flet as ft
from flet import *
import os
import shutil
from datetime import datetime
from blog_db import add_blog, get_all_blogs

def page_blog_register(page: ft.Page):
    # 画像保存先の設定
    IMAGE_DIR = "vanilla_blog/image"
    os.makedirs(IMAGE_DIR, exist_ok=True)

    # ステータス表示用のテキスト
    status_text = ft.Text("", color=ft.Colors.RED)

    def handle_register(e, title, content, image_path):
        if not title:
            status_text.value = "タイトルを入力してください"
            status_text.color = ft.Colors.RED
            page.update()
            return

        if not content:
            status_text.value = "本文を入力してください"
            status_text.color = ft.Colors.RED
            page.update()
            return

        try:
            # 画像がある場合は保存
            saved_image_path = None
            if image_path:
                # 投稿数を取得して連番を生成
                blogs = get_all_blogs()
                next_num = len(blogs) + 1
                num_str = str(next_num).zfill(2)
                ext = os.path.splitext(image_path)[1]
                new_filename = f"image{num_str}{ext}"
                saved_image_path = os.path.join(IMAGE_DIR, new_filename)
                # 画像をコピー
                shutil.copy2(image_path, saved_image_path)

            # 記事をDBに保存
            add_blog(title, content, saved_image_path)
            
            status_text.value = "記事を登録しました"
            status_text.color = ft.Colors.GREEN
            page.update()
            # 記事登録成功後、Blog_manageページに遷移
            page.go("/blog/manage")
        except Exception as ex:
            status_text.value = f"記事登録に失敗しました: {ex}"
            status_text.color = ft.Colors.RED
            page.update()

    # 画像選択用の変数
    selected_image_path = None

    def handle_image_pick(e: ft.FilePickerResultEvent):
        nonlocal selected_image_path
        if e.files:
            selected_image_path = e.files[0].path
            image_preview.src = selected_image_path
            page.update()

    # ファイル選択ダイアログ
    file_picker = ft.FilePicker(
        on_result=handle_image_pick
    )
    page.overlay.append(file_picker)

    # 画像プレビュー
    image_preview = ft.Image(
        width=200,
        height=200,
        fit=ft.ImageFit.COVER,
        visible=False
    )

    # タイトル入力
    title_input = ft.TextField(
        label="タイトル",
        width=600,
        border=ft.InputBorder.UNDERLINE
    )

    # 本文入力
    content_input = ft.TextField(
        label="本文",
        width=600,
        height=200,
        multiline=True,
        border=ft.InputBorder.UNDERLINE
    )

    # 画像選択ボタン
    image_button = ft.ElevatedButton(
        "画像を選択",
        icon=ft.icons.IMAGE,
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["jpg", "jpeg", "png"]
        )
    )

    # 記事登録ボタン
    register_button = ft.ElevatedButton(
        "記事を登録",
        icon=ft.icons.SAVE,
        on_click=lambda e: handle_register(
            e,
            title_input.value,
            content_input.value,
            selected_image_path
        )
    )

    # Homeに戻るボタン
    home_button = ft.ElevatedButton(
        "Homeに戻る",
        icon=ft.icons.HOME,
        on_click=lambda _: page.go("/")
    )

    # レイアウト
    return ft.View(
        "/blog/register",
        [
            ft.AppBar(
                title=ft.Text("ブログ記事登録"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[home_button]
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("新規記事作成", size=30, weight=ft.FontWeight.BOLD),
                        title_input,
                        content_input,
                        ft.Row([image_button, image_preview]),
                        ft.Row([register_button], alignment=ft.MainAxisAlignment.END),
                        status_text
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20
            )
        ]
    )

# 単体起動する場合
if __name__ == "__main__":
    ft.app(target=page_blog_register)
