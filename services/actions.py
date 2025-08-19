import os

from services.data import PandasDataRepository
from docxtpl import DocxTemplate

from datetime import datetime, timedelta
from babel.dates import format_date
from settings import (
    PATH_TEMPLATE_DOCX, 
    PATH_IRKA_DIRKA_ORDER, 
    PATH_EXCEL_PDF,
)
from PyPDF2 import PdfMerger


class NewOrder:
    def __init__(self, pd_data_repository: PandasDataRepository):
        self.pd_data_repository = pd_data_repository
        self.text_info = ""


    @staticmethod
    def format_ukrainian_date(date):
        day = date.strftime("%d")
        month_year = format_date(date, format="MMMM yyyy", locale='uk')
        return f"{day} {month_year}"


    def get_path_irka_dirka(self, date: datetime):
        dir_name_year = f"{date.year}(samba)"
        dir_name_month = f"{date.strftime('%m')} накази"

        path_year = os.path.join(PATH_IRKA_DIRKA_ORDER, dir_name_year)

        if not os.path.exists(path_year):
            self.text_info += f"Папка не найдена. Створюємо папку: {path_year} \n"
            os.makedirs(path_year)

        path_mount = os.path.join(PATH_IRKA_DIRKA_ORDER, dir_name_year, dir_name_month)
        if not os.path.exists(path_mount):
            self.text_info += f"Папка не найдена. Створюємо папку: {path_mount} \n"
            os.makedirs(path_mount)

        return path_mount

    def create_template(self):
        tpl = DocxTemplate(PATH_TEMPLATE_DOCX)

        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        formatted_date = self.format_ukrainian_date(tomorrow)

        number = self.pd_data_repository.get_order_number_by_date(date=now.date())
        today_str = now.date().strftime("%d.%m.%Y")

        row = {
            "date": today_str,
            "number": number,
            "date_prod": formatted_date,
        }

        tpl.render(row)
        
        path_irka_dirka = self.get_path_irka_dirka(date=now)
        
        file_name = f"\НАКАЗ №{number} від {today_str} в процесі.docx"
        new_file = f"{path_irka_dirka}{file_name}"

        if os.path.isfile(new_file):
            self.text_info += f"Файл вже існує:{new_file} \n"
            return None

        tpl.save(f"{path_irka_dirka}{file_name}")
        self.text_info += f"Шаблон створено: {file_name}"


class Vacation:
    def __init__(self, pd_data_repository: PandasDataRepository):
        self.pd_data_repository = pd_data_repository
        self.text_info = ""

    def overdue_leave_check(self):
        leaves = self.pd_data_repository.get_overdue_leave()

        if leaves is None:
            return self.text_info
        self.text_info = (
            f"Військово службовці які повинні повернутися з відпустки: \n {'-' * 40} \n"
        )

        for row in leaves.itertuples(index=True):
            self.text_info += (
                f"ПІБ: {row[2]}\n"
                f"Підрозділ: {row[3]}\n"
                f"Тип відпустки: {row[4]}\n"
                f"Запланована дата прибуття: {row[22].strftime("%d.%m.%Y")}\n"
                f"{'-' * 40}\n"
            )


class MergePDF:
    def __init__(self):
        self.text_info = ""

    def merge_report(self):
        output_path = os.path.join(PATH_EXCEL_PDF, "obiednany_koshtorys.pdf")

        merger = PdfMerger()

        for filename in sorted(os.listdir(PATH_EXCEL_PDF)):
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(PATH_EXCEL_PDF, filename)
                merger.append(full_path)
                self.text_info += f"Додано: {filename}\n"
        merger.write(output_path)
        merger.close()



