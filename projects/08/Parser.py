"""
This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing

from Constants import *

class Parser:
  """
  Handles the parsing of a single .vm file, and encapsulates access to the
  input code. It reads VM commands, parses them, and provides convenient 
  access to their components. 
  In addition, it removes all white space and comments.
  """

  def __init__(self, input_file: typing.TextIO) -> None:
    """
    Gets ready to parse the input file.

      Args:
        input_file (typing.TextIO): input file.
    """

    self.lines = input_file.read().splitlines()
    self.current_line_number = -1
    self.current_command = None

  def has_more_commands(self) -> bool:
    """
    Are there more commands in the input?

      Returns:
        bool: True if there are more commands, False otherwise.
    """

    for i in range(self.current_line_number + 1, len(self.lines)):
      if self.is_command(self.lines[i]):
        return True

    return False

  def advance(self) -> None:
    """
    Reads the next command from the input and makes it the current 
    command. Should be called only if has_more_commands() is true. Initially
    there is no current command.
    """
    
    if self.has_more_commands():
      self.current_line_number += 1

      while not self.is_command(self.lines[self.current_line_number]):
        self.current_line_number += 1
    
      # Load current command without comments and white spaces
      self.current_command = self.lines[self.current_line_number]
      self.current_command = self.current_command.split("//")[0].strip()

  def command_type(self) -> CommandType:
    """
      Returns:
        str: the type of the current VM command.
        "C_ARITHMETIC" is returned for all arithmetic commands.
        For other commands, can return:
        "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
        "C_RETURN", "C_CALL".
    """

    if self.current_command in ARITHMETIC_COMMANDS:
      return CommandType.C_ARITHMETIC
    elif PUSH_COMMAND in self.current_command:
      return CommandType.C_PUSH
    elif POP_COMMAND in self.current_command:
      return CommandType.C_POP
    elif LABEL_COMMAND in self.current_command:
      return CommandType.C_LABEL
    # Checking if-goto before goto
    elif IF_COMMAND in self.current_command:
      return CommandType.C_IF
    elif GOTO_COMMAND in self.current_command:
      return CommandType.C_GOTO
    elif FUNCTION_COMMAND in self.current_command:
      return CommandType.C_FUNCTION
    elif RETURN_COMMAND in self.current_command:
      return CommandType.C_RETURN
    elif CALL_COMMAND in self.current_command:
      return CommandType.C_CALL

  def arg1(self) -> str:
    """
      Returns:
        str: the first argument of the current command. In case of 
        "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
        Should not be called if the current command is "C_RETURN".
    
    """

    if self.command_type() == CommandType.C_ARITHMETIC:
      return self.current_command
    elif self.command_type != CommandType.C_RETURN:
      return self.current_command.split(" ")[1]

  def arg2(self) -> int:
    """
      Returns:
        int: the second argument of the current command. Should be
        called only if the current command is "C_PUSH", "C_POP", 
        "C_FUNCTION" or "C_CALL".
    """

    if self.command_type() == CommandType.C_PUSH \
        or self.command_type() == CommandType.C_POP \
        or self.command_type() == CommandType.C_FUNCTION \
        or self.command_type() == CommandType.C_CALL:
      return int(self.current_command.split(" ")[2])
      

  def is_command(self, line: str) -> bool:
    """
    Checks if the given line is a valid command.
      
      Args:
        line (str): line to check.

      Returns:
        bool: True if the line is a command, False otherwise.
    """

    if not line or line.startswith("//") or line == "\n":
      return False
        
    return True