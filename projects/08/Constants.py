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

class CommonCommand(Enum):
  SAVE_LAST_ITEM_TO_D = "save_last_item_to_d",
  SAVE_2ND_TO_LAST_ITEM_TO_D = "save_2nd_to_last_item_to_d",

  GO_TO_LAST_ITEM = "go_to_last_item",
  GO_TO_2ND_TO_LAST_ITEM = "go_to_2nd_to_last_item",

  REDUCE_SP_BY_1 = "reduce_sp_by_1",
  INCREASE_SP_BY_1 = "increase_sp_by_1",

ARITHMETIC_COMMANDS = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not", "shiftleft", "shiftright"]
PUSH_COMMAND = "push"
POP_COMMAND = "pop"
LABEL_COMMAND = "label"
GOTO_COMMAND = "goto"
IF_COMMAND = "if-goto"
FUNCTION_COMMAND = "function"
RETURN_COMMAND = "return"
CALL_COMMAND = "call"