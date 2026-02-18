from openpyxl import Workbook
from openpyxl.utils import get_column_letter 

def extract_excerpt(line: str, start_substring: str, end_substring: str | None = None):
    return line[line.find(start_substring)+len(start_substring):line.find(end_substring) if end_substring is not None else None].strip()


def normalize_widths(workbook: Workbook):

    for ws in workbook:
        for column in ws.columns:
            column_letter = get_column_letter(column[0].column)
            max_length = 0
            for cell in column:
                try:
                    if cell.value:
                        val_len = len(str(cell.value))
                        if val_len > max_length: max_length = val_len
                except: pass
            
            # Limit width to 60 to prevent extreme cases
            ws.column_dimensions[column_letter].width = min(max_length + 2, 60)

