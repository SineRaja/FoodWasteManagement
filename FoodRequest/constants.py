import enum


class RequestStatus(enum.Enum):
    open = "OPEN"
    completed = "COMPLETED"
    cancelled = "CANCELLED"


class CompanyType(enum.Enum):
    hotel = "HOTEL"
    events = "EVENTS"
    college = "COLLEGE"
    others = "OTHERS"
