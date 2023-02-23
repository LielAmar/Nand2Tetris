"""
This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing

from Constants import *


actions = {
  # Saves the last item in the stack in the D-Register
  "SAVE_LAST_ITEM": [
    "@SP",   # Going to address 0, to get the pointer of the stack
    "A=M-1", # Going to the address of the last item in the stack
    "D=M",   # Saving the last item in the stack
  ],

  # Saves the 2nd to last item in the stack in the D-Register
  "SAVE_PENULT_ITEM": [
    "@SP",   # Going to address 0, to get the pointer of the stack
    "A=M-1", # Going to the address of the last item in the stack
    "A=A-1", # Going to the item before the last item in the stack
    "D=M",   # Saving the 2nd to last item in the stack
  ],

  # Changes the A-Register to point to the last item in the stack
  "GO_TO_LAST_ITEM": [
    "@SP",   # Going to address 0, to get the pointer of the stack
    "A=M-1", # Going to the address of the last item in the stack
  ],

  # Changes the A-Register to point to the 2nd to last item in the stack
  "GO_TO_PENULT_ITEM": [
    "@SP",   # Going to address 0, to get the pointer of the stack
    "A=M-1", # Going to the address of the last item in the stack
    "A=A-1", # Going to the item before the last item in the stack
  ],

  # Reduces the SP value by 1
  "REDUCE_SP": [
    "@SP",   # Going to address 0, to get the pointer of the stack
    "M=M-1", # Decreasing the stack pointer by 1
  ],
    
  # Increases the SP value by 1
  "INCREASE_SP": [
    "@SP",   # Going to address 0, to get the pointer of the stack
    "M=M+1", # Increasing the stack pointer by 1
  ]
}


class CodeWriter:
  """
  Translates VM commands into Hack assembly code.
  """

  # A static variable to save the current command id
  command_id = 0

  def __init__(self, output_stream: typing.TextIO) -> None:
    """Initializes the CodeWriter.

      Args:
        output_stream (typing.TextIO): output stream.
    """

    self.output_stream = output_stream

    self.filename = ""
    self.function_name = ""

    self.call_id = 0


  def set_file_name(self, filename: str) -> None:
    """
    Informs the code writer that the translation of a new VM file is started.

      Args:
        filename (str): The name of the VM file.
    """

    self.filename = filename
    self.function_name = ""


  def write_arithmetic(self, command: str) -> None:
    """
    Writes assembly code that is the translation of the given
    arithmetic command. For the commands eq, lt, gt, you should correctly
    compare between all numbers our computer supports, and we define the
    value "true" to be -1, and "false" to be 0.

      Args:
        command (str): an arithmetic command.
    """
    
    CodeWriter.command_id += 1

    lines = []
    lines.append(f"// {command}")

    # Adding the last 2 items in the stack
    if command == "add":
      lines.extend(actions["SAVE_LAST_ITEM"])
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("M=M+D")
      lines.extend(actions["REDUCE_SP"])

    # Subtracting the last 2 items in the stack
    elif command == "sub":
      lines.extend(actions["SAVE_LAST_ITEM"])
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("M=M-D")
      lines.extend(actions["REDUCE_SP"])
    
    # Negating the last item in the stack
    elif command == "neg":
      lines.extend(actions["GO_TO_LAST_ITEM"])
      lines.append("M=-M")

    # Chaning the last item in the stack to 'not' item
    elif command == "not":
      lines.extend(actions["GO_TO_LAST_ITEM"])
      lines.append("M=!M")

    # Checking if the last 2 items in the stack are true
    elif command == "and":
      lines.extend(actions["SAVE_LAST_ITEM"])
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("M=D&M")
      lines.extend(actions["REDUCE_SP"])

    # Checking if one of the last 2 items in the stack is true
    elif command == "or":
      lines.extend(actions["SAVE_LAST_ITEM"])
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("M=D|M")
      lines.extend(actions["REDUCE_SP"])

    # Shifting the last item in the stack left
    elif command == "shiftleft":
      lines.extend(actions["GO_TO_LAST_ITEM"])
      lines.append("M=M<<")

    # Shifting the last item in the stack right
    elif command == "shiftright":
      lines.extend(actions["GO_TO_LAST_ITEM"])
      lines.append("M=M>>")

    # Checking if the last 2 items in the stack are equal
    elif command == "eq":
      lines.extend(actions["SAVE_LAST_ITEM"])
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("D=M-D")

      lines.append(f"@TRUE{CodeWriter.command_id}")
      lines.append("D;JEQ")

      lines.append(f"(FALSE{CodeWriter.command_id})")
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("M=0")
      lines.append(f"@END{CodeWriter.command_id}")
      lines.append("0;JMP")

      lines.append(f"(TRUE{CodeWriter.command_id})")
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("M=-1")

      lines.append(f"(END{CodeWriter.command_id})")
      lines.extend(actions["REDUCE_SP"])

    # Checking if the 2nd to last item is greater than the last item
    elif command == "gt":
      # ===== Checks if the numbers have different signs (to avoid overflow) ===== #

      # Get the last item
      lines.extend(actions["SAVE_LAST_ITEM"])

      # If the last item is negative, we want to check if
      # the 2nd to last item is positive (or zero)
      lines.append(f"@CHECK_SECOND_ITEM_POSITIVE{CodeWriter.command_id}")
      lines.append("D;JLT") # JLE

      # Otherwise, the last item is positive (or zero), we want to check if
      #  the 2nd to last item is negative
      lines.extend(actions["SAVE_PENULT_ITEM"])

      # If the second item is negative, then the last item is greater,
      # so we want to jump to FALSE
      lines.append(f"@FALSE{CodeWriter.command_id}")
      lines.append("D;JLT")

      # If the second item is positive, we want to run the subtraction
      lines.append(f"@CODE_START{CodeWriter.command_id}")
      lines.append("0;JMP")

      # We check if the 2nd to last item is positive (or zero)
      lines.append(f"(CHECK_SECOND_ITEM_POSITIVE{CodeWriter.command_id})")
      lines.extend(actions["SAVE_PENULT_ITEM"])

      # If the second item is positive, then the last item is smaller,
      # so we want to jump to TRUE
      lines.append(f"@TRUE{CodeWriter.command_id}")
      lines.append("D;JGE")


      # ===== Checks if first item is greater by subtracting ===== #
      lines.append(f"(CODE_START{CodeWriter.command_id})")
      lines.extend(actions["SAVE_LAST_ITEM"])
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("D=D-M")

      lines.append(f"@TRUE{CodeWriter.command_id}")
      lines.append("D;JLT")

      lines.append(f"(FALSE{CodeWriter.command_id})")
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("M=0")
      lines.append(f"@END{CodeWriter.command_id}")
      lines.append("0;JMP")

      lines.append(f"(TRUE{CodeWriter.command_id})")
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("M=-1")

      lines.append(f"(END{CodeWriter.command_id})")
      lines.extend(actions["REDUCE_SP"])

    # Checking if the 2nd to last item is smaller than the last item
    elif command == "lt":
      # ===== Checks if the numbers have different signs (to avoid overflow) ===== #

      # Get the last item
      lines.extend(actions["SAVE_LAST_ITEM"])

      # If the last item is negative, we want to check if
      # the 2nd to last item is positive (or zero)
      lines.append(f"@CHECK_SECOND_ITEM_POSITIVE{CodeWriter.command_id}")
      lines.append("D;JLT") # JLE

      # Otherwise, the last item is positive (or zero), we want to check if
      #  the 2nd to last item is negative
      lines.extend(actions["SAVE_PENULT_ITEM"])

      # If the second item is negative, then the last item is greater,
      # so we want to jump to TRUE
      lines.append(f"@TRUE{CodeWriter.command_id}")
      lines.append("D;JLT")

      # If the second item is positive, we want to run the subtraction
      lines.append(f"@CODE_START{CodeWriter.command_id}")
      lines.append("0;JMP")

      # We check if the 2nd to last item is positive (or zero)
      lines.append(f"(CHECK_SECOND_ITEM_POSITIVE{CodeWriter.command_id})")
      lines.extend(actions["SAVE_PENULT_ITEM"])

      # If the second item is positive, then the last item is smaller,
      # so we want to jump to FALSE
      lines.append(f"@FALSE{CodeWriter.command_id}")
      lines.append("D;JGE")


      # ===== Checks if first item is greater by subtracting ===== #
      lines.append(f"(CODE_START{CodeWriter.command_id})")
      lines.extend(actions["SAVE_LAST_ITEM"])
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("D=D-M") # item1 - item0

      lines.append(f"@TRUE{CodeWriter.command_id}")
      lines.append("D;JGT")

      lines.append(f"(FALSE{CodeWriter.command_id})")
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("M=0")
      lines.append(f"@END{CodeWriter.command_id}")
      lines.append("0;JMP")

      lines.append(f"(TRUE{CodeWriter.command_id})")
      lines.extend(actions["GO_TO_PENULT_ITEM"])
      lines.append("M=-1")

      lines.append(f"(END{CodeWriter.command_id})")
      lines.extend(actions["REDUCE_SP"])

    self.__write_to_file(lines)

  def write_push_pop(self, command: str, segment: str, index: int) -> None:
    """
    Writes assembly code that is the translation of the given
    command, where command is either C_PUSH or C_POP.

      Args:
        command (str): "C_PUSH" or "C_POP".
        segment (str): the memory segment to operate on.
        index (int): the index in the memory segment.
    """

    lines = []
    lines.append(f"// {command} {segment} {index}")

    if command == "C_PUSH":
      if segment == "local":
        lines.extend(self.__write_push_from_segment(index, "LCL"))
      elif segment == "argument":
        lines.extend(self.__write_push_from_segment(index, "ARG"))
      elif segment == "this":
        lines.extend(self.__write_push_from_segment(index, "THIS"))
      elif segment == "that":
        lines.extend(self.__write_push_from_segment(index, "THAT"))
      elif segment == "constant":
        lines.extend(self.__write_push_from_constant(index))
      elif segment == "static":
        lines.extend(self.__write_push_from_address(f"{self.filename.upper()}.{index}"))
      elif segment == "pointer":
        if index == 0:
          lines.extend(self.__write_push_from_address("THIS"))
        elif index == 1:
          lines.extend(self.__write_push_from_address("THAT"))
      elif segment == "temp":
        lines.extend(self.__write_push_from_address(f"R{5 + index}"))

    elif command == "C_POP":
      if segment == "local":
        lines.extend(self.__write_pop_to_segment(index, "LCL"))
      elif segment == "argument":
        lines.extend(self.__write_pop_to_segment(index, "ARG"))
      elif segment == "this":
        lines.extend(self.__write_pop_to_segment(index, "THIS"))
      elif segment == "that":
        lines.extend(self.__write_pop_to_segment(index, "THAT"))
      elif segment == "static":
        lines.extend(self.__write_pop_to_address(f"{self.filename.upper()}.{index}"))
      elif segment == "pointer":
        if index == 0:
          lines.extend(self.__write_pop_to_address("THIS"))
        elif index == 1:
          lines.extend(self.__write_pop_to_address("THAT"))
      elif segment == "temp":
        lines.extend(self.__write_pop_to_address(f"R{5+index}"))
        
    self.__write_to_file(lines)


  def write_label(self, label: str) -> None:
    pass

  def write_goto(self, label: str) -> None:
    pass

  def write_if(self, label: str) -> None:
    pass


  def write_function(self, function_name: str, n_vars: int) -> None: 
    pass

  def write_call(self, function_name: str, n_args: int) -> None:
    pass

  def write_return(self) -> None:
    pass


  # ===== UTILITIES ===== #
  def __write_to_file(self, lines: list[str]) -> None:
    """
    Writes the given lines to the output file.
    """

    for line in lines:
      if self.output_stream != None:
        self.output_stream.write(line + "\n")


  def __write_push_from_segment(self, index: int, pointer: str) -> list[str]:
    """
    Writes assembly code that pushes the value of
    the given segment and index to the stack.

      Args:
        index (int): the index in the memory segment
        pointer (str): the pointer to the memory segment to use
    """

    lines = []
    lines.append(f"@{index}")
    lines.append("D=A")
    lines.append(f"@{pointer}")
    lines.append("A=M+D")
    lines.append("D=M")

    lines.append("@SP")
    lines.append("A=M")
    lines.append("M=D")

    lines.extend(actions["INCREASE_SP"])

    return lines

  def __write_push_from_address(self, address: str) -> list[str]:
    """
    Writes assembly code that pushes the value in
    the given address to the stack.

      Args:
        address (int): the address to use
    """

    lines = []
    lines.append(f"@{address}")
    lines.append("D=M")

    lines.append("@SP")
    lines.append("A=M")
    lines.append("M=D")

    lines.extend(actions["INCREASE_SP"])

    return lines

  def __write_push_from_constant(self, constant: int) -> list[str]:
    """
    Writes assembly code that pushes the constant given to the stack.

      Args:
        constant (int): the constant to use
    """

    lines = []
    lines.append(f"@{constant}")
    lines.append("D=A")

    lines.append("@SP")
    lines.append("A=M")
    lines.append("M=D")

    lines.extend(actions["INCREASE_SP"])

    return lines


  def __write_pop_to_segment(self, index: int, segment: str) -> list[str]:
    """
    Writes assembly code that sets the value of
    the given segment and index to the last item in the stack.

      Args:
        index (int): the index in the memory segment
        pointer (str): the pointer to the memory segment to use
    """

    lines = []

    # Saving target location in the given segment
    lines.append(f"@{segment}")
    lines.append("D=M")
    lines.append(f"@{index}")
    lines.append("D=D+A")

    lines.append(f"@R13")
    lines.append("M=D")

    # Popping item from SP and saving it in the address saved in R13
    lines.extend(actions["SAVE_LAST_ITEM"])
    
    lines.append("@R13")
    lines.append("A=M")
    lines.append("M=D")

    lines.extend(actions["REDUCE_SP"])

    return lines

  def __write_pop_to_address(self, address: str) -> list[str]:
    """
    Writes assembly code that sets the value of
    the given address to the last item in the stack.

      Args:
        address (int): the address to use
    """

    lines = []

    # Popping item from SP and saving it in the address saved in R13
    lines.extend(actions["SAVE_LAST_ITEM"])
    
    lines.append(f"@{address}")
    lines.append("M=D")

    lines.extend(actions["REDUCE_SP"])

    return lines
