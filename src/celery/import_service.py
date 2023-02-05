import os

from openpyxl.styles import Border, Font, NamedStyle, Side
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from src.config import UPLOADS_DIR
from src.services.base_servises import AbstractImportClass


class ImportXLS(AbstractImportClass):
    def __init__(self, filename: str = "Result", sheet_name: str = "Menus") -> None:
        self.filename = ".".join([filename, "xls"])
        self.sheet_name = sheet_name

    def make_import(self, data) -> str:
        wb = Workbook()
        ws = wb.active
        ws.title = self.sheet_name
        rows = self._set_xls_data(data, ws)
        self._set_table_style(ws, rows)
        path = os.path.join(UPLOADS_DIR, self.filename)
        wb.save(path)
        return path

    def _set_table_style(self, ws: Worksheet, count_rows: int) -> None:
        ws.column_dimensions["A"].width = 5
        ws.column_dimensions["B"].width = 10
        ws.column_dimensions["C"].width = 20
        ws.column_dimensions["D"].width = 25
        ws.column_dimensions["E"].width = 60
        ws.column_dimensions["F"].width = 10
        name_style = NamedStyle(name="highlight")
        name_style.font = Font(bold=True, size=13)
        bd = Side(style="thin", color="000000")
        name_style.border = Border(left=bd, right=bd, bottom=bd, top=bd)
        for row in range(1, count_rows + 1):
            for col in ["A", "B", "C", "D", "E", "F"]:
                cell = "".join([col, str(row)])
                ws[cell].style = name_style

    def _set_xls_data(self, data: list, ws: Worksheet) -> int:
        menu: str = ""
        submenu: str = ""
        m_count, s_count, d_count, rows = 1, 1, 1, 0
        for r in data:
            if r["menu_title"] != menu:
                menu = r["menu_title"]
                ws.append([m_count, r["menu_title"], r["menu_description"]])
                m_count += 1
                rows += 1
            if r["submenu_title"] != submenu:
                submenu = r["submenu_title"]
                ws.append(["", s_count, r["submenu_title"], r["submenu_description"]])
                s_count += 1
                d_count = 1
                rows += 1
            ws.append(["", "", d_count, r["title"], r["description"], r["price"]])
            d_count += 1
            rows += 1
        return rows
