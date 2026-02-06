from pprint import pprint
from report_header import ReportHeader

class ReportPage:

    lines: list[str]
    header: ReportHeader
    def __init__(self, text: str):
        self.lines = text.split("\n")
        self.header = ReportHeader(self.get_header_lines())

    def debug_lines(self):
        pprint(self.lines)

    def get_header_lines(self):
        return self.lines[0:7]



