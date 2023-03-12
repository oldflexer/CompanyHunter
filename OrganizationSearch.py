import datetime
from dataclasses import dataclass


@dataclass
class OrganizationSearch:
    """Class that represents filtered organization search"""
    search_type: str
    work: str
    is_phone: str
    is_www: str
    is_email: str
    is_branch: str
    staff_min: int
    staff_max: int
    reestr_min: str
    reestr_max: str
    okato: str
    okved: str
    p1_min: int
    p1_max: int
    p2_min: int
    p2_max: int
    p3_min: int
    p3_max: int
    sort: str
    page: int
