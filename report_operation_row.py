from decimal import Decimal
from report_dataclasses import PaymentConcept

class OperationRow:
    __line: str
    concept: PaymentConcept
    quantity: Decimal
    factor: Decimal
    value: Decimal
    wages: Decimal
    assignment: Decimal
    deduction: Decimal
    balance: Decimal

    def __init__(self, line: str):
        self.__line = line
        # self.__get_fields(self.__line)

    # def __get_fields(self, line: str):
       # print(line)


