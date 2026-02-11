from datetime import datetime
from decimal import Decimal
from typing import List
from report_dataclasses import Bank, Employee, Position, Situation
from report_operation_row import OperationRow
from utils import extract_excerpt
from pprint import pprint
import pandas as pd

type RawOperations = list[List[str|None]]

class EmployeeSection:
    __lines: list[str]
    __raw_operations: RawOperations | None
    employee: Employee
    operations: pd.DataFrame | None

    def __init__(self, lines: list[str]):
        self.__lines = lines
        # pprint(lines)
        self.employee = self.__get_employee(self.__lines)
        # self.operations = [OperationRow(line) for line in self.__get_operation_lines(self.__lines)]
        self.operations = None
        self.__raw_operations = None

    def __get_operation_lines(self, lines: list[str]):
        return lines[5:-1]

    def set_raw_operations(self, ops: RawOperations):
        cleaned_rows = self.__clean_raw_operations(ops)
        # print("cleaned rows", cleaned_rows)
        self.__raw_operations = cleaned_rows

    def process_operations(self):
        if(self.__raw_operations is None):
            raise Exception('Attempted to process raw operations when the value is None')
        columns = ['CODIGO CONCEPTO', 'CONCEPTO', 'CANTIDAD', 'FACTOR', 'VALOR', 'SALARIO', 'ASIGNACION', 'DEDUCCION', 'SALDO']
        df = pd.DataFrame(self.__raw_operations, columns=columns) if len(self.__raw_operations) > 0 else pd.DataFrame()
        self.operations = df
    
    def __clean_raw_operations(self, ops: RawOperations):
        rows_to_keep: RawOperations = []
        for row in ops:
            first_cell = row[0]
            # print(first_cell)
            # We should only keep the rows that have some sort of concept number (ie. 10 PAGO)
            if(first_cell is None or len(first_cell) == 0):
                continue
            first_char = first_cell[0]
            # print(first_char)
            if not(first_char.isdigit()):
                continue
            rows_to_keep.append(row)
        # print('rows to keep', rows_to_keep)
        return rows_to_keep

    def debug_raw_operations(self):
        pprint(self.__raw_operations)

    def debug_operations(self):
        print(self.employee.identification)
        print(self.employee.full_name)
        print(self.employee.position.name)
        print(self.operations)
        print()
    
    def __get_employee(self, lines: list[str]):

        # Get employee name, identification and employment data
        first_line = lines[0];
        # id, full_name = first_line[first_line.find(':')+1:first_line.find('NRO')].strip().split(" ", 1)
        id, full_name = extract_excerpt(first_line, ":", "NRO").split(" ", 1)
        # identification = first_line[first_line.find('ID:')+3:first_line.find('INGRESO')].strip()
        identification = extract_excerpt(first_line, "ID:", "INGRESO")
        # entry_date = first_line[first_line.find('INGRESO:')+8:first_line.find('RETIRO')].strip()
        entry_date = extract_excerpt(first_line, "INGRESO:", "RETIRO");
        # exit_date = first_line[first_line.find('RETIRO:')+8:first_line.find('RETIRO')].strip()
        exit_date = extract_excerpt(first_line, "RETIRO:")
        # print(id, full_name, identification, entry_date, exit_date)

        # Get employee position and group
        second_line = lines[1];
        position_id, position = extract_excerpt(second_line, ":", "GRUPO:").split(" ", 1)
        group= extract_excerpt(second_line, "GRUPO:")
        # print(position_id, position, group)

        third_line = lines[2]
        situation = extract_excerpt(third_line, "SITUACION:", "SALIDA:")
        situation_departure = extract_excerpt(third_line, "SALIDA:", "REGRESO:")
        situation_return = extract_excerpt(third_line, "REGRESO:")

        # print(situation, situation_departure, situation_return)

        # Get the employee's salary
        fourth_line = lines[3]
        salary = extract_excerpt(fourth_line, "SUELDO:").replace(',','.')

        # print(salary)

        # Get the employee's bank details
        fifth_line = lines[4]
        bank_data = extract_excerpt(fifth_line, ":", "CTA")
        bank_id = ''
        bank = ''
        if len(bank_data) > 0:
            bank_id, bank = bank_data.split(" ", 1)
        account_number = extract_excerpt(fifth_line, "CTA.:")

        # print(bank_id, bank, account_number)

        date_format = "%d/%m/%Y"

        return Employee(
            id=id,
            full_name=full_name,
            identification=identification,
            entry_date=datetime.strptime(entry_date,date_format),
            exit_date= datetime.strptime(exit_date, date_format) if len(exit_date) > 0 else None,
            position= Position(
                id=position_id,
                name=position,
            ),
            group= group,
            situation= Situation(
                name=situation,
                comment="Placeholder", #TODO: Split the situation before creating the object instance
                departure_date=datetime.strptime(situation_departure, date_format) if len(situation_departure) > 0 else None,
                return_date=datetime.strptime(situation_return, date_format) if len(situation_return) > 0 else None,
            ),
            salary= Decimal(salary),
            bank= Bank(
                id= bank_id if len(bank_id) > 0 else None,
                name= bank if len(bank) > 0 else None,
            ),
            account_number= account_number if len(account_number) > 0 else None,
        )

