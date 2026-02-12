import pdfplumber
from report_page import ReportPage
import report_page
from dataclasses import dataclass

from page_operations import get_report_page, get_tables
import argparse

@dataclass
class CliArguments:
    filename: str
    pages_to_process: list[int] | None

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Wyndham Concorde Payroll Analyzer",
        description="Parses a PDF file containing payroll data exported from the internal system"
    )

    parser.add_argument("filename")

    parser.add_argument(
        "--pages",
        nargs="*",
        type=int,
        help="Array (list) of pages to be processed. Defaults to all pages"
    )

    return parser

def parse_cli_arguments(parser: argparse.ArgumentParser):

    args = parser.parse_args()

    return CliArguments(
        filename=args.filename,
        pages_to_process=args.pages
    ) 

if __name__ == '__main__':
    processed_pages: list[ReportPage] =[]

    parser = setup_parser()
    arguments = parse_cli_arguments(parser)

    with pdfplumber.open(path_or_fp=arguments.filename, pages=arguments.pages_to_process) as pdf:
            # for page in pdf.pages:
        for i in range(0,len(pdf.pages)):
            page = pdf.pages[i]
            # print(f"Processing page {page.page_number}")
            report_page = get_report_page(page)

            tables = get_tables(page)

            num_tables = len(tables)
            num_sec = len(report_page.body.sections)
            if(num_tables != num_sec):
                print(f"Employee section {num_sec} and table mismatch {num_tables}")
            else:
                # zipped_values = itertools.product(report_page.body.sections, tables)
                zipped_values = zip(report_page.body.sections, tables)
                for pair in zipped_values:
                    # print("Employee", pair[0])
                    # print("Raw operations", pair[1])
                    pair[0].set_raw_operations(pair[1])  
            for section in report_page.body.sections:
                # section.debug_raw_operations()
                section.process_operations()
                section.debug_operations()
            processed_pages.append(report_page)           


    section_count = 0

    for page in processed_pages:
        section_count = section_count + len(page.body.sections)

    print(f"Counted {section_count}")
