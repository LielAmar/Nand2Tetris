"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing

from Constants import *

class VMWriter:
  """
  Writes VM commands into a file. Encapsulates the VM command syntax.
  """

  def __init__(self, output_stream: typing.TextIO) -> None:
    """
    Creates a new file and prepares it for writing VM commands.
    """
    
    self.output = output_stream


  def write_push(self, segment: str, index: int) -> None:
    """
    Writes a VM push command.

    Args:
      segment (str): the segment to push to, can be "CONST", "ARG", 
      "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
      index (int): the index to push to.
    """

    self.__write_command__("push", SEGMENTS[segment], index)

  def write_pop(self, segment: str, index: int) -> None:
    """
    Writes a VM pop command.

    Args:
      segment (str): the segment to pop from, can be "CONST", "ARG", 
      "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
      index (int): the index to pop from.
    """

    self.__write_command__("pop", SEGMENTS[segment], index)

  def write_arithmetic(self, command: str) -> None:
    """
    Writes a VM arithmetic command.

    Args:
      command (str): the command to write, can be "ADD", "SUB", "NEG", 
      "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT".
    """

    self.__write_command__(ARITHMETIC_COMMANDS[command])

  def write_label(self, label: str) -> None:
    """
    Writes a VM label command.

    Args:
      label (str): the label to write.
    """

    self.__write_command__("label", label)

  def write_goto(self, label: str) -> None:
    """
    Writes a VM goto command.

    Args:
      label (str): the label to go to.
    """

    self.__write_command__("goto", label)

  def write_if(self, label: str) -> None:
    """
    Writes a VM if-goto command.

    Args:
      label (str): the label to go to.
    """

    self.__write_command__("if-goto", label)

  def write_call(self, name: str, n_args: int) -> None:
    """
    Writes a VM call command.

    Args:
      name (str): the name of the function to call.
      n_args (int): the number of arguments the function receives.
    """

    self.__write_command__("call", name, str(n_args))

  def write_function(self, name: str, n_locals: int) -> None:
    """
    Writes a VM function command.

    Args:
      name (str): the name of the function.
      n_locals (int): the number of local variables the function uses.
    """

    # self.__write_blank_line()
    self.__write_command__("function", name, str(n_locals))

  def write_return(self) -> None:
    """
    Writes a VM return command.
    """

    self.__write_command__("return")


  def __write_command__(self, cmd, arg1="", arg2="") -> None:
    """
    Writes a single VM command to the output file.
    """

    self.output.write(f"{cmd} {arg1} {arg2}\n")

  def __write_blank_line(self) -> None:
    """
    Writes a blank line to the output file.
    """

    self.output.write("\n")