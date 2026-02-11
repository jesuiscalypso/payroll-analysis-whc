import itertools
from pprint import pprint
from typing import List
import pdfplumber
from pdfplumber.page import Page
from report_page import ReportPage
import report_page

def test_filter(obj):
    if(obj['object_type'] == 'char'):
        if obj['text'] == '' or obj['text'] == ' ':
            return False
    return True

type GetTablesReturn = list[list[List[str | None]]]


def get_tables(page: Page) -> GetTablesReturn:
        # Table processing
        base_char = page.chars[0] # Every character here is the same size so it doesn't really matter which
        # Manually determine the right and left boundary for the table
        rightmost_line:int = max(c['x1'] for c in page.chars)
        leftmost_line: int = min(c['x1'] for c in page.chars)
        # Explicitly define vertical lines in order to deal with the weirdness that comes with a text table
        code_line = leftmost_line + (base_char['width'] * 4.5)
        balance_line = rightmost_line - (base_char['width'] * 10)
        deduction_line = balance_line - (base_char['width'] * 18)
        assignment_line = deduction_line - (base_char['width'] * 20)
        wages_line = assignment_line - (base_char['width'] * 22)
        value_line = wages_line - (base_char['width'] * 16)
        factor_line = value_line - (base_char['width'] * 26)
        quantity_line = factor_line - (base_char['width'] * 14)

        table_settings = {
            'vertical_strategy': 'explicit',
            'horizontal_strategy': 'text',
            "explicit_vertical_lines": [leftmost_line, rightmost_line, code_line, balance_line, deduction_line, assignment_line, wages_line, value_line, factor_line, quantity_line],
            "min_words_horizontal":3,
            "snap_x_tolerance": 20,
            "snap_y_tolerance":7,
        }

        # Cropping the page for table extraction
        crop_width = float(page.width)
        crop_height = float(page.height)
        cropped_page = page.crop(
            (
                #x0
                0 * crop_width,
                #top
                0.28 * crop_height,
                #x1
                1 * crop_width,
                #bottom
                1 * crop_height
            )
        )

        filtered_page = cropped_page.filter(test_filter)
        # im = filtered_page.to_image()
        # debug_image = im.reset().debug_tablefinder(table_settings)
        # debug_image.show() 
        tables = filtered_page.find_tables(table_settings)
        separated_tables: GetTablesReturn = []
        for table in tables:
            slice_indices = [0]
            row_index = 0
            columns_of_interest_index = (1,2,3, 4) 
            extracted_table = table.extract()
            # print(extracted_table)
            for row in extracted_table: 
                # print(row)
                string_of_interest = 'TOTAL'
                row_max_index = len(row) - 1
                text_options = [row[i] if i <= row_max_index else None for i in columns_of_interest_index]
                option_contains_string_of_interest = [True for opt in text_options if opt is not None and opt.find(string_of_interest) != -1]
                found_string = any(result is True for result in option_contains_string_of_interest)
                # print(text)
                if(found_string):
                    # We found the end of a section, now we have to determine whether there are more, or this is the last one.
                    if(row_index == len(extracted_table) - 1):
                        slice_indices.append(row_index)
                    else:
                        slice_indices.append(row_index + 2)
                row_index = row_index + 1    
            sliding_initial_point = 0
            # print(slice_indices)
            for index in slice_indices:
                if(index == 0):
                    continue;
                sliced_table = extracted_table[sliding_initial_point:index]

                sliding_initial_point = index  
                # Discard any erroneous tables that might have been created by accident
                # i.e.: An orphaned totals table, which we don't care about as it's not related to a single employee    
                first_row = sliced_table[0]
                # print(first_row)
                if(first_row[0] == None or first_row[0] == ' ' or first_row[0] == ''):
                    continue
                separated_tables.append(sliced_table)

        return separated_tables

def get_report_page(page: Page) -> ReportPage:
    text = page.extract_text()
        
    report_page = ReportPage(text)
    return report_page


if __name__ == '__main__':
    processed_pages: list[ReportPage] =[]
    with pdfplumber.open(path_or_fp='detalle.pdf') as pdf:
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
