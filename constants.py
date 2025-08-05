from enum import Enum

class Action(Enum):
    CREATE_TEMPLATE_ORDER = "create_template_order"
    MERGE_REPORT = "merge_report"
    REPORT_MESSAGE = "report_message"


class Sheet(Enum):
    ARROWS = "Arrows"
    DECLENSION = "declension"
    LEAVE = "ВІДПУ"
    BASE_2 = "base_2"


class CaseLanguage(Enum):
    ACCUSATIVE = "accusative"
    DATIVE = "dative"
