from datetime import datetime
import pandas as pd
from constants import Sheet, CaseLanguage


class PandasDataRepository:
    def __init__(self) -> None:
        self.sheets = None

    def read_all_sheets(self, target_sheets: list[str], file_path: str):
        self.sheets = pd.read_excel(file_path, sheet_name=target_sheets)

    def get_person_by_id(self, person_id: int) -> dict | None:
        base_2 = self.sheets[Sheet.BASE_2.value]
        columns_names = base_2.columns.tolist()

        result = base_2[base_2[columns_names[1]] == person_id]

        if not result.empty:
            return result.iloc[0]
        else:
            return None

    def get_order_number_by_date(self, date: datetime.date) -> int | None:
        declension_sheet = self.sheets[Sheet.DECLENSION.value]
        result = declension_sheet[declension_sheet["дата"].dt.date == date]

        if not result.empty:
            return int(result.iloc[0]["№ наказу"])
        else:
            return None

    def get_overdue_leave(self) -> dict | None:
        leave_sheet = self.sheets[Sheet.LEAVE.value]
        now = datetime.now()

        leave_sheet["00:00:00.1"] = pd.to_datetime(
            leave_sheet["00:00:00.1"],
            format="%d.%m.%Y",
            errors="coerce",
        )

        result = leave_sheet[
            (leave_sheet["Unnamed: 0"].notna()) &
            (leave_sheet["Unnamed: 22"].isna()) &
            (leave_sheet["00:00:00.1"].dt.date <= now.date())
        ]

        if not result.empty:
            return result
        else:
            return None

    def get_overdue_vlk(self):
        hv_sheet = self.sheets[Sheet.HV.value]
        now = datetime.now()

        hv_sheet["Unnamed: 12"] = pd.to_datetime(
            hv_sheet["Unnamed: 12"],
            format="%d.%m.%Y",
            errors="coerce",
        )

        result = hv_sheet[
            (hv_sheet["Unnamed: 28"].notna()) &
            (hv_sheet["Unnamed: 12"].dt.date <= now.date())
        ]

        if not result.empty:
            return result
        else:
            return None


    def get_rank_case(
        self,
        rank_str: str,
        case_language: CaseLanguage,
    ) -> str:
        declension_sheet = self.sheets[Sheet.DECLENSION.value]
        tag_contract = " військової служби за контрактом"
        if tag_contract in rank_str:
            rank_str = rank_str.replace(tag_contract, "")

        result = declension_sheet[declension_sheet["Звання називний"].str.strip() == rank_str.strip()]

        if case_language == CaseLanguage.ACCUSATIVE:
            return result["✪ вибери!"].iloc[0]
        elif case_language == CaseLanguage.DATIVE:
            return result["Звання давальний"].iloc[0]

    def get_full_name_case(
        self,
        person_id: int,
        case_language: CaseLanguage,
    ) -> str:
        person = self.get_person_by_id(person_id)

        if case_language == CaseLanguage.ACCUSATIVE:
            return person.iloc[111]
        elif case_language == CaseLanguage.DATIVE:
            return person.iloc[105]

    def get_position_case(
        self,
        position_str: str,
        case_language: CaseLanguage,
    ) -> str:
        sh_sheet = self.sheets[Sheet.SH.value]
        result = sh_sheet[sh_sheet["Повна посада"].str.strip() == position_str.strip()]

        if case_language == CaseLanguage.ACCUSATIVE:
            return result["знахідний (без в/ч)"].iloc[0]
        elif case_language == CaseLanguage.DATIVE:
            return result["давальний (без в/ч)"].iloc[0]


    def get_rank_full_name_position_case(
        self,
        rank_str: str,
        person_id: int,
        position_str: str,
        case_language: CaseLanguage,
    ):
        rank = self.get_rank_case(rank_str, case_language)
        full_name = self.get_full_name_case(person_id, case_language)
        position = self.get_position_case(position_str, case_language)
        return rank, full_name, position
