import flet as ft
from profile_copy import ProfileCopy
import heaven

def pfc_view(page: ft.Page):
    page.title = "プロフィールコピー"

    def profile_create(e):
        result2.value = "プロフィール作成中"
        result2.update()
        # インスタンスを作成
        obj = ProfileCopy(name.value, mail.value)

        # メソッドを呼び出す
        obj.profile_paste_fuja()
        obj.profile_paste_delija()
        obj.profile_paste_town()
        obj.profile_paste_ekichika()
        t_mail = obj.town_mail_signup()
        e_mail = obj.ekichika_mail_signup()
        d_mail = obj.delija_mail_signup()
        #f_mail = obj.fuja_mail_signup()
        obj.town_mail_cc(e_mail)
        obj.town_mail_cc(d_mail)  
        #obj.town_mail_cc(f_mail)  
        h_info = heaven.pdeco_create(name.value)
        r_info = [t_mail, e_mail, d_mail, h_info[0], h_info[1], h_info[2], h_info[3]]#f_mail,
        print(r_info)
        # 必要な情報を変数に格納
        genji_name = name.value
        heaven_url = h_info[3]
        user_id = h_info[1]
        password = h_info[2]
        email_address = t_mail
        print(t_mail)
        # テンプレートを定義
        template = f"""
源氏名: {genji_name}
ヘブン（姫デコ）
URL: {heaven_url}
ID: {user_id}
PW: {password}
メールアドレス: {email_address}

※当日や前乗り時間は後ほど指定させて頂きます。"""

        result2.value = template
        result2.update()

    name = ft.TextField(label="キャスト名")
    mail = ft.TextField(label="メールアドレス")
    result2 = ft.TextField(
            label="log",
            multiline=True,
            min_lines=1,
            max_lines=20,
        )
    copy = ft.ElevatedButton("PFC", icon=ft.Icons.GAVEL, on_click=profile_create)
    home_button = ft.ElevatedButton("Homeに戻る", icon=ft.icons.HOME, on_click=lambda e: page.go("/"))
    
    return ft.View(
        "/pfc",
        [
            ft.AppBar(
                title=ft.Text("プロフィールコピー"),
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[home_button]
            ),
            ft.Container(
                content=ft.Column([
                    name,
                    mail,
                    copy,
                    result2,
                ]),
                padding=20
            )
        ]
    )

#ft.app(target=main)#, view=ft.WEB_BROWSER