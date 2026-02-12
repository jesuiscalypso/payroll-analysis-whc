from openpyxl import Workbook 

def extract_excerpt(line: str, start_substring: str, end_substring: str | None = None):
    return line[line.find(start_substring)+len(start_substring):line.find(end_substring) if end_substring is not None else None].strip()

