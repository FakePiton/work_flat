import flet as ft

from services.excel import ExcelData
from services.actions import (
    NewOrder, 
    Vacation,
    MergePDF,
)
from constants import Action


class Controller:
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

    @staticmethod
    def run_create_order(text_panel: ft.Text):
        excel_data = ExcelData()
        new_order = NewOrder(excel_data)
        vacation = Vacation(excel_data)
        
        new_order.create_template()
        vacation.overdue_leave_check()

        text = new_order.text_info + "\n\n" + vacation.text_info
        text_panel.value = text

    @staticmethod
    def run_merge_report(text_panel: ft.Text):
        merge_pdf = MergePDF()
        merge_pdf.merge_report()
        text_panel.value = merge_pdf.text_info

    @staticmethod
    def run_report_message(self, text_panel: ft.Text):
        pass
