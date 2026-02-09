from datetime import datetime
from decimal import Decimal
from report_dataclasses import Bank, Employee, Position, Situation
from utils import extract_excerpt
class EmployeeSection:
    __lines: list[str]
    employee: Employee

    def __init__(self, lines: list[str]):
        self.__lines = lines
        self.employee = self.__get_employee(self.__lines)
    
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

