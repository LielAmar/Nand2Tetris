from curses.ascii import SP
from enum import Enum
from re import M

class CommandType(Enum):
  C_ARITHMETIC = "C_ARITHMETIC",
  C_PUSH = "C_PUSH",
  C_POP = "C_POP",
  C_LABEL = "C_LABEL",
  C_GOTO = "C_GOTO",
  C_IF = "C_IF",
  C_FUNCTION = "C_FUNCTION",
  C_RETURN = "C_RETURN",
  C_CALL = "C_CALL"

ARITHMETIC_COMMANDS = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not", "shiftleft", "shiftright"]
PUSH_COMMAND = "push"
POP_COMMAND = "pop"