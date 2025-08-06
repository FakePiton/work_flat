import flet as ft

from services.data import PandasDataRepository
from services.actions import (
    NewOrder, 
    Vacation,
    MergePDF,
)
from constants import Action
from services.report_message import ReportMessage


class Controller:
    def __init__(self, pandas_data_repository: PandasDataRepository):
        self.pandas_data_repository = pandas_data_repository

    def run_actions(self, name_action: str, text_panel: ft.Text):
        method = self.get_actions(name_action=name_action)
        if not method:
            text_panel.value = "Дія не знайдена"
            return
        
        method(text_panel=text_panel)

    def get_actions(self, name_action: str):
        dict_actions = {
            Action.CREATE_TEMPLATE_ORDER.name: self.run_create_order,
            Action.MERGE_REPORT.name: self.run_merge_report,
            Action.REPORT_MESSAGE.name: self.run_report_message,
        }
        return dict_actions.get(name_action)

    def run_create_order(self, text_panel: ft.Text):
        new_order = NewOrder(self.pandas_data_repository)
        vacation = Vacation(self.pandas_data_repository)
        
        new_order.create_template()
        vacation.overdue_leave_check()

        text = new_order.text_info + "\n\n" + vacation.text_info
        text_panel.value = text

    @staticmethod
    def run_merge_report(text_panel: ft.Text):
        merge_pdf = MergePDF()
        merge_pdf.merge_report()
        text_panel.value = merge_pdf.text_info

    def run_report_message(self, text_panel: ft.Text):
        report_message = ReportMessage(
            sheets=self.pandas_data_repository.sheets,
            pd_data_repository=self.pandas_data_repository,
        )
        text_panel.value = report_message.get_report()
