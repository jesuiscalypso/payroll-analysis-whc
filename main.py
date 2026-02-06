from pprint import pprint
import pdfplumber
from report_page import ReportPage

if __name__ == '__main__':
    print('Hello, world!')
    with pdfplumber.open('detalle.pdf') as pdf:
            # for page in pdf.pages:
        page = pdf.pages[0]
        text = page.extract_text()
        report_page = ReportPage(text)
        pprint(report_page.header.get_property('report_date'))
