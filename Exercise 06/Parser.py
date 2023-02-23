"""
This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing

from enum import Enum

class CommandType(Enum):
  A_COMMAND = "A_COMMAND"
  C_COMMAND = "C_COMMAND"
  L_COMMAND = "L_COMMAND"

class Parser:
  """
  Encapsulates access to the input code. Reads an assembly language 
  command, parses it, and provides convenient access to the commands 
  components (fields and symbols). In addition, removes all white space and 
  comments.
  """

  def __init__(self, input_file: typing.TextIO) -> None:
    """
    Opens the input file and gets ready to parse it.

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
    Reads the next command from the input and makes it the current command.
    Should be called only if has_more_commands() is true.
    """

    if self.has_more_commands():
      self.current_line_number += 1

      while not self.is_command(self.lines[self.current_line_number]):
        self.current_line_number += 1
    
      # Load current command without comments and white spaces
      self.current_command = self.lines[self.current_line_number].replace(' ', '')
      self.current_command = self.current_command.split("//")[0].strip()

  def command_type(self) -> CommandType:
    """
      Returns:
        str: the type of the current command:
        "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
        "C_COMMAND" for dest=comp;jump
        "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
    """

    if self.current_command[0] == "@":
      return CommandType.A_COMMAND
    elif self.current_command[0] == "(":
      return CommandType.L_COMMAND
    
    return CommandType.C_COMMAND


  def symbol(self) -> str:
    """
      Returns:
        str: the symbol or decimal Xxx of the current command @Xxx or
        (Xxx). Should be called only when command_type() is "A_COMMAND" or 
        "L_COMMAND".
    """

    command_type = self.command_type()

    if command_type == CommandType.C_COMMAND:
      return None
    
    if command_type == CommandType.A_COMMAND:
      return self.current_command[1:]
    
    return self.current_command[1:-1]

  def dest(self) -> str:
    """
      Returns:
        str: the dest mnemonic in the current C-command. Should be called 
        only when commandType() is "C_COMMAND".
    """

    if self.command_type() != CommandType.C_COMMAND:
      return None
    
    dest = self.current_command.split("=")

    if len(dest) == 1:
      return None

    return dest[0]

  def comp(self) -> str:
    """
      Returns:
        str: the comp mnemonic in the current C-command. Should be called 
        only when commandType() is "C_COMMAND".
    """

    if self.command_type() != CommandType.C_COMMAND:
      return None
    
    comp = self.current_command.split("=")

    if len(comp) == 1:
      return comp[0].split(";")[0]

    return comp[1].split(";")[0]

  def jump(self) -> str:
    """
      Returns:
        str: the jump mnemonic in the current C-command. Should be called 
        only when commandType() is "C_COMMAND".
    """

    if self.command_type() != CommandType.C_COMMAND:
      return None
    
    jump = self.current_command.split(";")

    if len(jump) == 1:
      return None

    return jump[1]


  def is_command(self, line: str) -> bool:
    """
    Checks if the given line is a valid command.
      
      Args:
        line (str): line to check.

      Returns:
        bool: True if the line is a command, False otherwise.
    """

    line = line.replace(' ', '')

    if not line or line.startswith("//") or line == "\n":
      return False
        
    return True

  def reset(self) -> None:
    """
    Resets the parser to the first command.
    """

    self.current_line_number = -1
    self.current_command = None