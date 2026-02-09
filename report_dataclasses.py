from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
@dataclass
class Company:
    id: str
    name: str

@dataclass
class OrganizationalUnit:
    id: str
    name: str

@dataclass
class Payroll:
    id: str
    name: str

@dataclass
class Period:
    start: datetime
    end: datetime
    descriptor: str
    long_descriptor: str

@dataclass
class Position:
    id: str
    name: str

@dataclass
class Situation:
    name: str
    comment: str
    departure_date: datetime | None
    return_date: datetime | None

@dataclass
class Bank:
    id: str | None
    name: str | None

@dataclass 
class Employee:
    id: str
    full_name: str
    identification: str
    entry_date: datetime
    exit_date: datetime | None
    position: Position
    group: str
    situation: Situation
    salary: Decimal
    bank: Bank
    account_number: str | None


@dataclass
class PaymentConcept:
    id: str
    name: str


