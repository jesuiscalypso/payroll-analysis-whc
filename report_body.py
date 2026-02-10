from pprint import pprint
from typing import Literal, NamedTuple
from employee_section import EmployeeSection
from collections import deque

type EmployeeDataDictKeys = Literal[
    'id',
    'full_name',
    'identification',
    'entry_date',
    'departure_date',
    'position_id',
    'position',
    'group_id',
    'group_descriptor',
    'situation_id',
    'situation',
    'situation_comment',
    'situation_departure_date',
    'situation_arrival_date',
    'salary',
    'bank_id',
    'bank',
    'account_number',
]

type RawEmployeeSection = list[str]

#Tuple is false if the set isn't terminated, but true if it is
class RawPageEmployeeSections(NamedTuple): 
    terminated: bool 
    sections: list[RawEmployeeSection]

class ReportBody:
    __lines: list[str]
    __raw_sections: RawPageEmployeeSections
    sections: list[EmployeeSection]

    def __init__(self, lines: list[str]):
        self.__lines = lines
        self.__raw_sections = self.__get_raw_employee_sections(self.__lines)
        try:
            self.sections = self.__get_employee_sections(self.__raw_sections)
        except Exception as e:
            print(e)
            self.sections = []
    
    def __get_raw_employee_sections(self, lines: list[str]) -> RawPageEmployeeSections:
        
        sections: list[RawEmployeeSection] = []
        current_section: list[str] = []
        terminated = True
        previous_page_unterminated = False
        current_section_relative_index = 0;

        for line in lines:
            # print(terminated, previous_page_unterminated, current_section_relative_index)
            # We can't find the start of the section in the start of this page, 
            # Which means we're continuiong on from the previous one
            if current_section_relative_index == 0 and line.find("TRABAJADOR:") == -1:
                print("Could not find trabajador", line)
                terminated = False
                previous_page_unterminated = True
            # We found the start of the section, flip the flag
            elif line.find("TRABAJADOR:") != -1:
                if(previous_page_unterminated is False):
                    terminated = False
                current_section.append(line)
            # We found the end of the section, flip the flag
            elif line.find("TOTAL POR TRABAJADOR") != -1:
                if previous_page_unterminated is False:
                    terminated = True
                current_section.append(line)
                sections.append(current_section)
                current_section = []
                current_section_relative_index = 0
            # Check for any of the exit cases which we don't want to process
            elif line.find("TOTAL POR UNIDAD ORGANIZATIVA") != -1:
                break;
            else:
                current_section.append(line)

            current_section_relative_index = current_section_relative_index + 1

        return RawPageEmployeeSections(terminated, sections)

    def __get_employee_sections(self, raw_sections: RawPageEmployeeSections):
        if(raw_sections.terminated is False):
            raise Exception("Cannot parse an unterminated section, please merge with the next unterminated page until you have a terminated collection")
        sections = [EmployeeSection(section) for section in raw_sections.sections]
        return sections
