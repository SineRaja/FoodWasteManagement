import enum


class RequestStatus(enum.Enum):
    open = "OPEN"
    resolved = "RESOLVED"

class UserType(enum.Enum):
    DONOR = "DONOR"
    NGO = "NGO"