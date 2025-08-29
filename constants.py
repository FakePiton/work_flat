from enum import Enum

class Action(Enum):
    CREATE_TEMPLATE_ORDER = "create_template_order"
    MERGE_REPORT = "merge_report"
    REPORT_MESSAGE = "report_message"
    RESET_DB = "reset_db"


class Sheet(Enum):
    ARROWS = "Arrows"
    DECLENSION = "declension"
    LEAVE = "ВІДПУ"
    BASE_2 = "base_2"
    SH = "sh"
    HV = "ХВ"


class CaseLanguage(Enum):
    ACCUSATIVE = "accusative"  # знахідний
    DATIVE = "dative"  # давальний
