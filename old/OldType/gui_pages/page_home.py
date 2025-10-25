import flet as ft

def home_view(page: ft.Page):
    page.title = "自動化ツール"
    page.window_width = 800
    page.window_height = 600
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    def create_container(text, color, icon, on_click):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=40, color=ft.Colors.WHITE),
                ft.Text(text, size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            margin=10,
            padding=20,
            alignment=ft.alignment.center,
            bgcolor=color,
            width=180,
            height=180,
            border_radius=10,
            ink=True,
            on_click=on_click,
            animate=ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT),
            on_hover=lambda e: handle_hover(e, color)
        )

    def handle_hover(e, base_color):
        if e.data == "true":  # ホバー開始
            e.control.bgcolor = ft.Colors.with_opacity(0.8, base_color)
        else:  # ホバー終了
            e.control.bgcolor = base_color
        e.control.update()

    def navigate_to_blog_manage(e):
        print("ブログ管理ページへ遷移")
        page.go("/blog/manage")

    def navigate_to_shake_blog_manage(e):
        print("Shakeブログ管理ページへ遷移")
        page.go("/shake_blog/manage")

    def navigate_to_kg_auto(e):
        print("キテネギフトページへ遷移")
        page.go("/kg/auto")

    def navigate_to_profile_create(e):
        print("プロフィール拡散ページへ遷移")
        page.go("/pfc")

    def navigate_to_okini_talk(e):
        print("オキニトークページへ遷移")
        page.go("/okini_talk")

    # カードの作成
    blog_manage_card = create_container(
        "ブログ管理",
        ft.Colors.BLUE,
        ft.Icons.ARTICLE,
        navigate_to_blog_manage
    )

    shake_blog_manage_card = create_container(
        "Shakeブログ管理",
        ft.Colors.INDIGO,
        ft.Icons.ARTICLE_OUTLINED,
        navigate_to_shake_blog_manage
    )

    kg_auto_card = create_container(
        "キテネギフト",
        ft.Colors.GREEN,
        ft.Icons.CARD_GIFTCARD,
        navigate_to_kg_auto
    )

    profile_create_card = create_container(
        "プロフィール拡散",
        ft.Colors.PURPLE,
        ft.Icons.PERSON,
        navigate_to_profile_create
    )

    okini_talk_card = create_container(
        "オキニトーク",
        ft.Colors.ORANGE,
        ft.Icons.CHAT,
        navigate_to_okini_talk
    )

    return ft.View(
        "/",
        [
            ft.AppBar(title=ft.Text("Auto Kitene"), bgcolor=ft.Colors.ON_SURFACE_VARIANT),
            ft.Container(
                content=ft.Column([
                    ft.Text("Auto Kitene", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Divider(),
                    ft.Row([
                        ft.Column([
                            blog_manage_card,
                            shake_blog_manage_card,
                            kg_auto_card
                        ]),
                        ft.Column([
                            profile_create_card,
                            okini_talk_card
                        ])
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ]),
                padding=20
            )
        ]
    )

# 単体起動する場合
if __name__ == "__main__":
    ft.app(target=home_view)