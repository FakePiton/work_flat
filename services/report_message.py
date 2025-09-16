from constants import Sheet, CaseLanguage
from datetime import datetime
import pandas as pd
from services.data import PandasDataRepository
from collections import defaultdict


class ReportMessage:
    def __init__(self, sheets, pd_data_repository: PandasDataRepository):
        self.sheets = sheets
        self.text_info = ""
        self.pd_data_repository = pd_data_repository
        self.order_date = datetime.today()

        self.text_enlisted_in_a_military_unit = ""
        self.text_prescription = ""
        self.text_change_position = ""
        self.text_transfer = ""
        self.text_dismissal = ""
        self.ranks = defaultdict(list)

    def get_report(self, order_date: datetime | None = None):
        if order_date:
            self.order_date = order_date

        number_order = self.pd_data_repository.get_order_number_by_date(
            date=self.order_date.date(),
        )

        if number_order is None:
            return "Errro: Номера наказа не знайдено!!!"

        text = (
            f"Бажаю здоров'я!\n"
            f"‼№{number_order} Зміни за {self.order_date.strftime("%d.%m.%Y")} ‼\n"
        )

        self.get_arrows_sheet(str(number_order))

        elements = [
            self.text_enlisted_in_a_military_unit,
            self.text_prescription,
            self.text_change_position,
            self.text_transfer,
            self.text_dismissal,
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
            "ПЕРЕВ": self.get_transfer,
            "ЗВІЛЬН": self.get_dismissal,
        }

        result = arrows[
            (arrows["Unnamed: 6"] == number_order) &
            (arrows["Unnamed: 7"].dt.year == self.order_date.year) &
            (
                arrows["ПЕРЕВ"].isin(methods.keys())
            )
        ]

        for row in result.iterrows():
            methods.get(row[1].iloc[1])(row[1])

    def _get_enlisted_in_a_military_unit(self, row):
        if not self.text_enlisted_in_a_military_unit:
            self.text_enlisted_in_a_military_unit = (
                "*Зараховано до списку особового складу:* \n"
            )

        person_id,  _ = row.iloc[55].split("_")
        (
            rank_accusative,
            full_name_accusative,
            position_accusative
        ) = self.pd_data_repository.get_rank_full_name_position_case(
            person=int(person_id),
            rank_str=row.iloc[2],
            position_str=row.iloc[5],
            case_language=CaseLanguage.ACCUSATIVE,
        )

        self.text_enlisted_in_a_military_unit += (
            f"- {rank_accusative} {full_name_accusative} призначено на посаду {position_accusative}\n"
        )

    def _get_prescription(self, row):
        if not self.text_prescription:
            self.text_prescription = (
                "*Виведено в розпорядження командира військової частини А4862:* \n"
            )

        person_id, _ = row.iloc[55].split("_")

        rank_accusative = self.pd_data_repository.get_rank_case(
            rank_str=row.iloc[2],
            case_language=CaseLanguage.ACCUSATIVE,
        )
        full_name_accusative = self.pd_data_repository.get_full_name_case(
            person=int(person_id),
            case_language=CaseLanguage.ACCUSATIVE,
        )

        self.text_prescription += f"- {rank_accusative} {full_name_accusative} {row.iloc[4]}\n"

    def _get_rank(self, row):
        title = f"*Присвоєне {row.iloc[18]} військові звання: {row.iloc[5]}:*\n"

        person_id, _ = row.iloc[56].split("_")

        rank_dative = self.pd_data_repository.get_rank_case(
            rank_str=row.iloc[2],
            case_language=CaseLanguage.DATIVE,
        )
        full_name_dative = self.pd_data_repository.get_full_name_case(
            person=int(person_id),
            case_language=CaseLanguage.DATIVE,
        )

        self.ranks[title].append(f"- {rank_dative} {full_name_dative} {row.iloc[4]} \n")

    def _get_change_position(self, row):
        if not self.text_change_position:
            self.text_change_position = f"*Переміщення по посадам:*\n"

        person_id, position = row.iloc[55].split("_")

        rank_accusative = self.pd_data_repository.get_rank_case(
            rank_str=row.iloc[2],
            case_language=CaseLanguage.ACCUSATIVE,
        )
        full_name_accusative = self.pd_data_repository.get_full_name_case(
            person=int(person_id),
            case_language=CaseLanguage.ACCUSATIVE,
        )
        position_accusative = self.pd_data_repository.get_position_case(
            position_str=row.iloc[5],
            case_language=CaseLanguage.ACCUSATIVE,
        )

        self.text_change_position += (
            f"- {rank_accusative} {full_name_accusative} "
            f"{row.iloc[4]} призначено на посаду {position_accusative}\n"
        )

    def get_transfer(self, row):
        if not self.text_transfer:
            self.text_transfer = "*Переведено до інших військових частин:* \n"

        rank_accusative = self.pd_data_repository.get_rank_case(
            rank_str=row.iloc[2],
            case_language=CaseLanguage.ACCUSATIVE,
        )
        full_name_accusative = self.pd_data_repository.get_full_name_case(
            person=row.iloc[3],
            case_language=CaseLanguage.ACCUSATIVE,
        )

        self.text_transfer += f"- {rank_accusative} {full_name_accusative} {row.iloc[4]} \n"

    def get_dismissal(self, row):
        if not self.text_dismissal:
            self.text_dismissal = "*Звільнено з військової служби:* \n"

        rank_accusative = self.pd_data_repository.get_rank_case(
            rank_str=row.iloc[2],
            case_language=CaseLanguage.ACCUSATIVE,
        )
        full_name_accusative = self.pd_data_repository.get_full_name_case(
            person=row.iloc[3],
            case_language=CaseLanguage.ACCUSATIVE,
        )

        self.text_dismissal += f"- {rank_accusative} {full_name_accusative} {row.iloc[4]} \n"
