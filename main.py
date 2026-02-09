from pprint import pprint
import pdfplumber
from report_page import ReportPage

if __name__ == '__main__':
    processed_pages: list[ReportPage] =[]
    with pdfplumber.open(path_or_fp='detalle.pdf') as pdf:
            # for page in pdf.pages:
        for i in range(0,len(pdf.pages)):
            page = pdf.pages[i]
            print(f"Processing page {i+1}")
            text = page.extract_text()
            report_page = ReportPage(text)
            header = report_page.header
            body=report_page.body
            # print(header.date,header.payroll, header.company, header.period, header.organizational_unit)
            processed_pages.append(report_page)

    section_count = 0

    for page in processed_pages:
        section_count = section_count + len(page.body.sections)

    print(f"Counted {section_count}")
