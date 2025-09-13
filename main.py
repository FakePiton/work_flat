import threading
import flet as ft
from constants import Action
from services.controller import Controller
from services.data import get_pandas_data_repository
from settings import PATH_EXCEL, PATH_EXCEL_PDF, PATH_IRKA_DIRKA_ORDER


def after_startup(progress_bar: ft.ProgressBar, page: ft.Page):
    progress_bar.visible = True
    page.update()

    page.pandas_data_repository = get_pandas_data_repository()

    progress_bar.visible = False
    page.update()


def main(page: ft.Page):
    page.title = "Flet App: Наказіст 1+"
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="Налаштування"),
            ft.NavigationBarDestination(icon=ft.Icons.APPS, label="Сервіси"),
        ],
        selected_index=1,
        on_change=lambda e: show_page(e.control.selected_index)
    )

    progress = ft.ProgressBar(visible=False)

    settings_view = ft.Column([
        progress,
        ft.Text("Налаштування додатку", size=20),
        ft.TextField(label="Шлях до штатки", value=PATH_EXCEL),
        ft.TextField(label="Шлях до файлів PDF", value=PATH_EXCEL_PDF),
        ft.TextField(label="Шлях до папки з наказами", value=PATH_IRKA_DIRKA_ORDER),
    ])

    service_buttons = [progress] + [
        ft.ElevatedButton(text=service.name, on_click=lambda e, s=service.name: open_service_actions(s))
        for service in Action
    ]
    services_view = ft.Column([
        ft.Text("Список сервісів", size=20),
        *service_buttons
    ])

    content = ft.Container(content=settings_view)
    page.add(content)

    def show_page(index):
        if index == 0:
            content.content = settings_view
        elif index == 1:
            content.content = services_view
        page.update()

    def open_service_actions(service_name):
        text_panel = ft.Text(
            theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
            selectable=True,
            no_wrap=False,
            max_lines=None,
            overflow=ft.TextOverflow.CLIP,
        )
        scrollable_text = ft.Column(
            controls=[text_panel],
            scroll="auto",
            expand=True,
            height=400,
        )
        date_picker = ft.DatePicker()
        button_date_picker = ft.ElevatedButton(
            "Pick date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: page.open(date_picker),
        )

        def run_service():
            progress.visible = True
            page.update()

            controller = Controller(pandas_data_repository=page.pandas_data_repository)
            controller.run_actions(
                name_action=service_name,
                text_panel=text_panel,
                page=page,
                date_picker_date=date_picker.value,
            )

            progress.visible = False
            errors = page.pandas_data_repository.errors
            if errors:
                page.open(ft.SnackBar(ft.Text("\n- ".join(errors)), bgcolor=ft.Colors.RED))
            page.update()

        column_list_objects = [
            ft.Text(f"Дії для {service_name}", size=20),
            progress,
            ft.ElevatedButton(
                "Запустити",
                on_click=lambda e: threading.Thread(target=run_service).start()
            ),
            scrollable_text,
        ]

        if service_name == Action.REPORT_MESSAGE.name:
            column_list_objects.insert(2, button_date_picker)

        actions_view = ft.Column(column_list_objects)

        content.content = actions_view
        page.update()

    show_page(1)
    after_startup(progress, page)

ft.app(target=main)
