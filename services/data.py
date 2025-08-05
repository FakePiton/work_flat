import pandas as pd
from constants import Sheet, CaseLanguage


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

    # def get_person_cases_by_id(
    #     self,
    #     person_id: int,
    #     case_language: CaseLanguage,
    # ) -> dict | None:
    #     pass

# p = PandasData(PATH_EXCEL)
# p.read_all_sheets(target_sheets=["Arrows", "declension", "ВІДПУ"])
#
# print(p.sheets)
