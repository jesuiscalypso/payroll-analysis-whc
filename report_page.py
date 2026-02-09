from pprint import pprint
from report_body import ReportBody
from report_header import ReportHeader

class ReportPage:

    lines: list[str]
    header: ReportHeader
    body: ReportBody

    def __init__(self, text: str):
        self.lines = text.split("\n")
        self.header = ReportHeader(self.get_header_lines())
        self.body = ReportBody(self.get_body_lines())

    def get_header_lines(self):
        return self.lines[0:7]
    
    def get_body_lines(self):
        return self.lines[8:]



