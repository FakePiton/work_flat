import flet as ft
from constants import Action, Sheet
from services.controller import Controller
from services.data import PandasDataRepository
from settings import PATH_EXCEL


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ADAPTIVE

    def submit_click(e):
        progress_bar.visible = True
        page.update()

        controller = Controller(pandas_data_repository=page.pandas_data_repository)
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

    pandas_data_repository = PandasDataRepository()
    pandas_data_repository.read_all_sheets(
        file_path=PATH_EXCEL,
        target_sheets=[
            Sheet.ARROWS.value,
            Sheet.DECLENSION.value,
            Sheet.LEAVE.value,
            Sheet.BASE_2.value,
        ]
    )
    page.pandas_data_repository = pandas_data_repository

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
