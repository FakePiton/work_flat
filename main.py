import flet as ft
from constants import Action
from services.controller import Controller


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ADAPTIVE

    def submit_click(e):
        progress_bar.visible = True
        page.update()

        controller = Controller()
        controller.run_actions(
            name_action=drop_down.value,
            text_panel=text_panel,
        )

        progress_bar.visible = False
        page.update()
    
    progress_bar = ft.ProgressBar(visible=False)
    text_panel = ft.Text(
        theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
        selectable=True,
        no_wrap=False,
        max_lines=None,
        overflow=ft.TextOverflow.CLIP,
    )
    drop_down = ft.Dropdown(options=[ft.DropdownOption(action.name) for action in Action], expand=True)
    submit = ft.ElevatedButton("Submit", on_click=submit_click)
    

    page.add(
       ft.Column(
            controls=[
                ft.Container(
                    content=drop_down,
                    expand=True,
                    height=50
                ),
                ft.Container(
                    content=submit,
                    expand=True,
                    height=50
                ),
                ft.Container(
                    content=progress_bar,
                    expand=False,
                ),
                ft.Container(
                    content=text_panel,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
        )
    )
ft.app(main)
