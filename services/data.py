from datetime import datetime

import pandas as pd
from constants import Sheet


class PandasDataRepository:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.sheets = None

    def read_all_sheets(self, target_sheets: list[str]):
        self.sheets = pd.read_excel(self.file_path, sheet_name=target_sheets)

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


from settings import PATH_EXCEL

pandas_data_repository = PandasDataRepository(PATH_EXCEL)
pandas_data_repository.read_all_sheets(
    target_sheets=[
        Sheet.ARROWS.value,
        Sheet.DECLENSION.value,
        Sheet.LEAVE.value,
        Sheet.BASE_2.value,
    ]
)

pandas_data_repository.get_overdue_leave()