
class ReportHeader:
    __lines: list[str]
    __header_dict: dict[str, str]
    
    def __init__(self, lines: list[str]):
        self.__lines = lines
        self.__header_dict = self.__get_header_dict()

    def __get_header_dict(self) -> dict[str, str]:
        header_dict = {}
        first_line = self.__lines[0]
        report_date = first_line.split(":", 2)[-1].strip()

        header_dict['report_date'] = report_date

        return header_dict

    def get_property(self, key: str) -> str:
        property = self.__header_dict[key]
        if(property is None):
            raise Exception('Invalid key')
        return property
