import re
from enum import Enum


class Patterns(Enum):
    LOGIN = r'^[a-zA-Z0-9_]{3,12}$'
    PASSWORD = r'^[a-zA-Z0-9_@#$%^&+=]{8,24}$'


def validateWithPattern(pattern, value):
  return re.fullmatch(pattern, value) != None


