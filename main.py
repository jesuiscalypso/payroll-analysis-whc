from typing import Literal
import pdfplumber
import bank_account_exporter
from report_page import ReportPage
import report_page
from dataclasses import dataclass

from page_operations import get_report_page, get_tables
import argparse

import spreadsheet_exporter

@dataclass
class CliArguments:
    filename: str
    pages_to_process: list[int] | None
    export_format: Literal['worksheet', 'accounts'] | None
    export_filename: str

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

    parser.add_argument(
        "--export_format",
        type=str,
        default="worksheet",
        nargs="?",
        choices=["worksheet", "accounts"],
    )

    parser.add_argument(
        "--export_filename",
        type=str,
        default="nomina",
        nargs="?",
    )

    return parser

def parse_cli_arguments(parser: argparse.ArgumentParser):

    args = parser.parse_args()

    return CliArguments(
        filename=args.filename,
        pages_to_process=args.pages,
        export_format=args.export_format,
        export_filename=args.export_filename,
    ) 

if __name__ == '__main__':
    processed_pages: list[ReportPage] =[]

    parser = setup_parser()
    arguments = parse_cli_arguments(parser)
    print("Opening PDF file... (this might take a while)")
    with pdfplumber.open(path_or_fp=arguments.filename, pages=arguments.pages_to_process) as pdf:
            # for page in pdf.pages:
        print("Processing pages...")
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
                # section.debug_operations()
            processed_pages.append(report_page)           

    if(arguments.export_format is not None):
        filename = arguments.export_filename
        if(arguments.export_format == 'worksheet'):
            print(f"Exporting '{filename}.xlsx'...")
            spreadsheet_exporter.export_styled_excel(pages=processed_pages, name=filename)
            print("Done!")
        elif(arguments.export_format == 'accounts'): 
            print(f"Exporting '{filename}_cuentas.xlsx'...")
            bank_account_exporter.export_bank_account_excel(pages=processed_pages, name=filename + "_cuentas")
            print("Done!")


