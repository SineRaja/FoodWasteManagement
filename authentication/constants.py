import enum
from Address.constants import Cities


class Gender(enum.Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class UserType(enum.Enum):
    DONOR = "DONOR"
    NGO = "NGO"
