import flet as ft


def get_home_view(page: ft.Page):
    return ft.View(
        route="/",
        controls=[
            ft.Text("Головна сторінка"),
            ft.ElevatedButton("Перейти до /about", on_click=lambda _: page.go("/about"))
        ]
    )

