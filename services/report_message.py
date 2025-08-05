from constants import Sheet
from datetime import datetime
import pandas as pd
from services.data import PandasDataRepository
from collections import defaultdict


class ReportMessage:
    def __init__(self, sheets, pd_data_repository: PandasDataRepository):
        self.sheets = sheets
        self.text_info = ""
        self.pd_data_repository = pd_data_repository
        self.today = datetime.today()

        self.text_enlisted_in_a_military_unit = ""
        self.text_prescription = ""
        self.text_change_position = ""
        self.ranks = defaultdict(list)

    def get_report(self):
        number_order = self.pd_data_repository.get_order_number_by_date(
            date=self.today.date(),
        )

        if number_order is None:
            return "Errro: Номера наказа не знайдено!!!"

        text = (
            f"Бажаю здоров'я!\n"
            f"‼№{number_order} Зміни за {self.today.strftime("%d.%m.%Y")} ‼\n"
        )

        self.get_arrows_sheet(str(number_order))

        elements = [
            self.text_enlisted_in_a_military_unit,
            self.text_prescription,
            self.text_change_position,
        ]

        for element in elements:
            if element:
                text += f"\n {element}"

        if self.ranks:
            for key in self.ranks.keys():
                text += f"\n{key}"
                for value in self.ranks[key]:
                    text += value

        return text

    def get_arrows_sheet(self, number_order: str):
        arrows = self.sheets[Sheet.ARROWS.value]

        arrows["Unnamed: 7"] = pd.to_datetime(
            arrows["Unnamed: 7"],
            dayfirst=True,
            format="%d.%m.%Y",
            errors="coerce",
        )

        methods = {
            "ПРИБУВ": self._get_enlisted_in_a_military_unit,
            "РОЗПОРЯДЖ": self._get_prescription,
            "ПОСАДА": self._get_change_position,
            "ЗВАННЯ": self._get_rank,
        }

        result = arrows[
            (arrows["Unnamed: 6"] == number_order) &
            (arrows["Unnamed: 7"].dt.year == self.today.year) &
            (
                arrows["ПЕРЕВ"].isin(methods.keys())
            )
        ]

        for row in result.itertuples(index=True):
            methods.get(row[2])(row)

    def _get_enlisted_in_a_military_unit(self, row):
        if not self.text_enlisted_in_a_military_unit:
            self.text_enlisted_in_a_military_unit = (
                "*Зараховані до списку особового складу:* \n"
            )

        person_id,  position = row._56.split("_")
        person = self.pd_data_repository.get_person_by_id(int(person_id))

        full_name, position_title = person.iloc[103].split(",")

        self.text_enlisted_in_a_military_unit += (
            f"- {full_name} призначено на посаду{position_title}\n"
        )

    def _get_prescription(self, row):
        if not self.text_prescription:
            self.text_prescription = (
                "*Виведено в розпорядження командира військової частини А4862:* \n"
            )

        person_id, _ = row._56.split("_")
        person = self.pd_data_repository.get_person_by_id(int(person_id))

        full_name= person.iloc[102]
        self.text_prescription += f"- {full_name} {row._5}\n"

    def _get_rank(self, row):
        title = f"*Присвоєні {row._19} військові звання: {row._6}:*\n"

        person_id, _ = row._57.split("_")
        person = self.pd_data_repository.get_person_by_id(int(person_id))
        full_name = person.iloc[109]
        self.ranks[title].append(f"- {full_name}\n")

    def _get_change_position(self, row):
        if not self.text_change_position:
            self.text_change_position = f"*Переміщення по посадам:*\n"

        person_id, position = row._56.split("_")
        person = self.pd_data_repository.get_person_by_id(int(person_id))

        full_name, position_title = person.iloc[103].split(",")
        self.text_change_position += (
            f"- {full_name} {row._5} призначено на посаду{position_title}\n"
        )
