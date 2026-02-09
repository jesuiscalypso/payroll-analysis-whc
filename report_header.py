from pprint import pprint
from typing import Callable, Literal
from datetime import datetime
from report_dataclasses import  Company, OrganizationalUnit, Period, Payroll

type ReportHeaderDictKeys = Literal[
'report_date', 
'report_period', 
'report_period_long', 
'period_end_date', 
'period_start_date', 
"company_id", 
"company", 
"payroll_id", 
"payroll", 
'organizational_unit_id', 
'organizational_unit']

class ReportHeader:
    __lines: list[str]
    __header_dict: dict[ReportHeaderDictKeys, str]

    date: datetime
    period: Period
    company: Company
    organizational_unit: OrganizationalUnit
    payroll: Payroll
    
    def __init__(self, lines: list[str]):
        self.__lines = lines
        self.__header_dict = self.__get_header_dict()
        self.__set_fields(self.__header_dict)

    def __set_fields(self, dictionary: dict[ReportHeaderDictKeys, str]):

        date_format = "%d/%m/%Y"

        to_datetime: Callable[[str], datetime] = lambda date_str : datetime.strptime(date_str, date_format)

        self.date = to_datetime(dictionary['report_date'])

        self.period = Period(
            start=to_datetime(dictionary['period_start_date']),
            end=to_datetime(dictionary['period_end_date']),
            descriptor=dictionary['report_period'],
            long_descriptor=dictionary['report_period_long']
        )

        self.payroll = Payroll(
            id=dictionary['payroll_id'],
            name=dictionary['payroll']
        )
        
        self.company = Company(
            id=dictionary['company_id'],
            name=dictionary['company']
        )
        
        self.organizational_unit = OrganizationalUnit(
            id=dictionary['organizational_unit_id'],
            name=dictionary['organizational_unit']
        )

    def __get_header_dict(self) -> dict[ReportHeaderDictKeys, str]:
        header_dict: dict[ReportHeaderDictKeys, str] = {}
        # Get the report's date
        first_line = self.__lines[0]
        report_date = first_line.split(":", 2)[-1].strip()
        header_dict['report_date'] = report_date

        # Get the report's period (the date range for which it is valid)
        fifth_line = self.__lines[4]
        report_period = fifth_line[fifth_line.find(':')+1:fifth_line.find('DEL')].strip().replace(' ', '')
        period_start_date = fifth_line[fifth_line.find('DEL')+3:fifth_line.find('AL')].strip().replace(' ', '')
        period_end_date = fifth_line[fifth_line.find('AL')+2:fifth_line.find('NOMINA')].strip().replace(' ', '')
        report_period_long = fifth_line[fifth_line.find('NOMINA')+6:].strip()

        header_dict['report_period'] = report_period
        header_dict['report_period_long'] = report_period_long
        header_dict['period_start_date'] = period_start_date
        header_dict['period_end_date'] = period_end_date

        # Get the report's company

        sixth_line = self.__lines[5]
        company_id, company = sixth_line[sixth_line.find(':')+1: sixth_line.find('NOMINA')].strip().split(' ', 1)
        payroll_id, payroll = sixth_line[sixth_line.find('NOMINA:')+7:sixth_line.find('DIST')].strip().split(' ', 1)

        header_dict['company_id'] = company_id
        header_dict['company'] = company
        header_dict['payroll_id'] = payroll_id
        header_dict['payroll'] = payroll

        # Get the report's organizational identifier

        seventh_line = self.__lines[6]
        organizational_unit_id, organizational_unit = seventh_line[seventh_line.find(":")+1:].strip().split(" ", 1)

        header_dict['organizational_unit_id'] = organizational_unit_id
        header_dict['organizational_unit'] = organizational_unit

        return header_dict

    def debug_header_dict(self): 
        pprint(self.__header_dict)
    

