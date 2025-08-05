import os
from dotenv import load_dotenv

load_dotenv()

PATH_EXCEL = os.getenv("PATH_EXCEL")
PATH_TEMPLATE_DOCX = os.getenv("PATH_TEMPLATE_DOCX")
PATH_IRKA_DIRKA_ORDER = os.getenv("PATH_IRKA_DIRKA_ORDER")
PATH_EXCEL_PDF = os.getenv("PATH_EXCEL_PDF")
