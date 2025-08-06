from datetime import datetime
import pandas as pd
from constants import Sheet


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
