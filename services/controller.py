import flet as ft

from services.data import PandasDataRepository
from services.actions import (
    NewOrder, 
    Vacation,
    MergePDF,
)
from constants import Action, Sheet
from services.report_message import ReportMessage
from settings import PATH_EXCEL


class Controller:
    def __init__(self, pandas_data_repository: PandasDataRepository):
        self.pandas_data_repository = pandas_data_repository

    def run_actions(self, **kwargs):
        name_action: str = kwargs.get("name_action")
        text_panel: ft.Text = kwargs.get("text_panel")

        method = self.get_actions(name_action=name_action)
        if not method:
            text_panel.value = "Дія не знайдена"
            return
        
        method(**kwargs)

    def get_actions(self, name_action: str):
        dict_actions = {
            Action.CREATE_TEMPLATE_ORDER.name: self.run_create_order,
            Action.MERGE_REPORT.name: self.run_merge_report,
            Action.REPORT_MESSAGE.name: self.run_report_message,
            Action.RESET_DB.name: self.run_reset_db,
        }
        return dict_actions.get(name_action)

    def run_create_order(self, **kwargs):
        text_panel: ft.Text = kwargs.get("text_panel")

        new_order = NewOrder(self.pandas_data_repository)
        vacation = Vacation(self.pandas_data_repository)
        
        new_order.create_template()
        vacation.overdue_leave_check()

        text = new_order.text_info + "\n\n" + vacation.text_info
        text_panel.value = text

    @staticmethod
    def run_merge_report(**kwargs):
        text_panel: ft.Text = kwargs.get("text_panel")

        merge_pdf = MergePDF()
        merge_pdf.merge_report()
        text_panel.value = merge_pdf.text_info

    def run_report_message(self, **kwargs):
        text_panel: ft.Text = kwargs.get("text_panel")

        report_message = ReportMessage(
            sheets=self.pandas_data_repository.sheets,
            pd_data_repository=self.pandas_data_repository,
        )
        text_panel.value = report_message.get_report()

    @staticmethod
    def run_reset_db(**kwargs):
        text_panel: ft.Text = kwargs.get("text_panel")
        page: ft.Page = kwargs.get("page")

        pandas_data_repository = PandasDataRepository()
        pandas_data_repository.read_all_sheets(
            file_path=PATH_EXCEL,
            target_sheets=[
                Sheet.ARROWS.value,
                Sheet.DECLENSION.value,
                Sheet.LEAVE.value,
                Sheet.BASE_2.value,
                Sheet.SH.value,
            ]
        )
        page.pandas_data_repository = pandas_data_repository
        text_panel.value = "Обновлено успішно"
