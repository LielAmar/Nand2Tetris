"""
This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

from http.client import OK
import typing

from Constants import *

class CodeWriter:
  """
  Translates VM commands into Hack assembly code.
  """

  def __init__(self, output_stream: typing.TextIO) -> None:
    """Initializes the CodeWriter.

      Args:
        output_stream (typing.TextIO): output stream.
    """

    self.output_stream = output_stream
    self.filename = ""
    self.command_id = 0

  def set_file_name(self, filename: str) -> None:
    """
    Informs the code writer that the translation of a new VM file is started.

      Args:
        filename (str): The name of the VM file.
    """

    # Your code goes here!
    # This function is useful when translating code that handles the
    # static segment.
    # To avoid problems with Linux/Windows/MacOS differences with regards
    # to filenames and paths, you are advised to parse the filename in
    # the function "translate_file" in Main.py using python's os library,
    # For example, using code similar to:
    # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
    self.filename = filename
    self.command_id = 0

  def write_arithmetic(self, command: str) -> None:
    """
    Writes assembly code that is the translation of the given
    arithmetic command. For the commands eq, lt, gt, you should correctly
    compare between all numbers our computer supports, and we define the
    value "true" to be -1, and "false" to be 0.

      Args:
        command (str): an arithmetic command.
    """
    
    self.command_id += 1
    lines = []
    lines.append(f"// {command}")

    # Adding the last 2 items in the stack
    if command == "add":
      lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("M=M+D")
      lines.extend(self.get_common_command(CommonCommand.REDUCE_SP_BY_1))

    # Subtracting the last 2 items in the stack
    elif command == "sub":
      lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("M=M-D")
      lines.extend(self.get_common_command(CommonCommand.REDUCE_SP_BY_1))
    
    # Negating the last item in the stack
    elif command == "neg":
      lines.extend(self.get_common_command(CommonCommand.GO_TO_LAST_ITEM))
      lines.append("M=-M")

    # Chaning the last item in the stack to 'not' item
    elif command == "not":
      lines.extend(self.get_common_command(CommonCommand.GO_TO_LAST_ITEM))
      lines.append("M=!M")

    # Checking if the last 2 items in the stack are true
    elif command == "and":
      lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("M=D&M")
      lines.extend(self.get_common_command(CommonCommand.REDUCE_SP_BY_1))

    # Checking if one of the last 2 items in the stack is true
    elif command == "or":
      lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("M=D|M")
      lines.extend(self.get_common_command(CommonCommand.REDUCE_SP_BY_1))

    # Shifting the last item in the stack left
    elif command == "shiftleft":
      lines.extend(self.get_common_command(CommonCommand.GO_TO_LAST_ITEM))
      lines.append("M=M<<")

    # Shifting the last item in the stack right
    elif command == "shiftright":
      lines.extend(self.get_common_command(CommonCommand.GO_TO_LAST_ITEM))
      lines.append("M=M>>")

    # TODO: eq, gt and lt are exactly the same. Might wanna refactor
    # also, make sure to handle overflow. Meaning if one number is positive and
    # one number is negative, simply return the negative instead of subtracting
    # and checking if the result is negative, 'cause this might lead to overflow.

    # Checking if the last 2 items in the stack are equal
    elif command == "eq":
      lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("D=M-D")

      lines.append(f"@TRUE{self.command_id}")
      lines.append("D;JEQ")

      lines.append(f"(FALSE{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("M=0")
      lines.append(f"@END{self.command_id}")
      lines.append("0;JMP")

      lines.append(f"(TRUE{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("M=-1")

      lines.append(f"(END{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.REDUCE_SP_BY_1))

    # Checking if the 2nd to last item is greater than the last item
    elif command == "gt":
      # item0 (182)
      # item1 (181)
      #
      # item0 > item1  <=> item1 - item0 < 0

      # ===== Checks if the numbers have different signs (to avoid overflow) ===== #

      # Get the last item
      lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))

      # If the last item is negative, we want to check if
      # the 2nd to last item is positive (or zero)
      lines.append(f"@CHECK_SECOND_ITEM_POSITIVE{self.command_id}")
      lines.append("D;JLT") # JLE

      # Otherwise, the last item is positive (or zero), we want to check if
      #  the 2nd to last item is negative
      lines.extend(self.get_common_command(CommonCommand.SAVE_2ND_TO_LAST_ITEM_TO_D))

      # If the second item is negative, then the last item is greater,
      # so we want to jump to FALSE
      lines.append(f"@FALSE{self.command_id}")
      lines.append("D;JLT")

      # If the second item is positive, we want to run the subtraction
      lines.append(f"@CODE_START{self.command_id}")
      lines.append("0;JMP")

      # We check if the 2nd to last item is positive (or zero)
      lines.append(f"(CHECK_SECOND_ITEM_POSITIVE{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.SAVE_2ND_TO_LAST_ITEM_TO_D))

      # If the second item is positive, then the last item is smaller,
      # so we want to jump to TRUE
      lines.append(f"@TRUE{self.command_id}")
      lines.append("D;JGE")


      # ===== Checks if first item is greater by subtracting ===== #
      lines.append(f"(CODE_START{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("D=D-M")

      lines.append(f"@TRUE{self.command_id}")
      lines.append("D;JLT")

      lines.append(f"(FALSE{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("M=0")
      lines.append(f"@END{self.command_id}")
      lines.append("0;JMP")

      lines.append(f"(TRUE{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("M=-1")

      lines.append(f"(END{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.REDUCE_SP_BY_1))

    # Checking if the 2nd to last item is smaller than the last item
    elif command == "lt":
      # item0 (182)
      # item1 (181)
      # item0 < item1  <=> item1 - item0 > 0

      # ===== Checks if the numbers have different signs (to avoid overflow) ===== #

      # Get the last item
      lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))

      # If the last item is negative, we want to check if
      # the 2nd to last item is positive (or zero)
      lines.append(f"@CHECK_SECOND_ITEM_POSITIVE{self.command_id}")
      lines.append("D;JLT") # JLE

      # Otherwise, the last item is positive (or zero), we want to check if
      #  the 2nd to last item is negative
      lines.extend(self.get_common_command(CommonCommand.SAVE_2ND_TO_LAST_ITEM_TO_D))

      # If the second item is negative, then the last item is greater,
      # so we want to jump to TRUE
      lines.append(f"@TRUE{self.command_id}")
      lines.append("D;JLT")

      # If the second item is positive, we want to run the subtraction
      lines.append(f"@CODE_START{self.command_id}")
      lines.append("0;JMP")

      # We check if the 2nd to last item is positive (or zero)
      lines.append(f"(CHECK_SECOND_ITEM_POSITIVE{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.SAVE_2ND_TO_LAST_ITEM_TO_D))

      # If the second item is positive, then the last item is smaller,
      # so we want to jump to FALSE
      lines.append(f"@FALSE{self.command_id}")
      lines.append("D;JGE")


      # ===== Checks if first item is greater by subtracting ===== #
      lines.append(f"(CODE_START{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("D=D-M") # item1 - item0

      lines.append(f"@TRUE{self.command_id}")
      lines.append("D;JGT")

      lines.append(f"(FALSE{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("M=0")
      lines.append(f"@END{self.command_id}")
      lines.append("0;JMP")

      lines.append(f"(TRUE{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.GO_TO_2ND_TO_LAST_ITEM))
      lines.append("M=-1")

      lines.append(f"(END{self.command_id})")
      lines.extend(self.get_common_command(CommonCommand.REDUCE_SP_BY_1))

    # Write all the lines we've created to the output file
    for line in lines:
      print(line)
      if self.output_stream != None:
        self.output_stream.write(line + "\n")

  def write_push_pop(self, command: CommandType, segment: str, index: int) -> None:
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

    if command == CommandType.C_PUSH:
      if segment == "local":
        lines.extend(self.write_push_from_segment(index, "LCL"))
      elif segment == "argument":
        lines.extend(self.write_push_from_segment(index, "ARG"))
      elif segment == "this":
        lines.extend(self.write_push_from_segment(index, "THIS"))
      elif segment == "that":
        lines.extend(self.write_push_from_segment(index, "THAT"))
      elif segment == "constant":
        lines.extend(self.write_push_from_constant(index))
      elif segment == "static":
        lines.extend(self.write_push_from_segment_direct(f"{self.filename.upper()}.{index}"))
      elif segment == "pointer":
        if index == 0:
          lines.extend(self.write_push_from_address("THIS"))
        elif index == 1:
          lines.extend(self.write_push_from_address("THAT"))
      elif segment == "temp":
        # TODO: might need to add a check to see if index is in range (5-12)
        lines.extend(self.write_push_from_address(f"R{5+index}"))

    elif command == CommandType.C_POP:
      if segment == "local":
        lines.extend(self.write_pop_to_segment(index, "LCL"))
      elif segment == "argument":
        lines.extend(self.write_pop_to_segment(index, "ARG"))
      elif segment == "this":
        lines.extend(self.write_pop_to_segment(index, "THIS"))
      elif segment == "that":
        lines.extend(self.write_pop_to_segment(index, "THAT"))
      elif segment == "static":
        lines.extend(self.write_pop_to_segment_direct(f"{self.filename.upper()}.{index}"))
      elif segment == "pointer":
        if index == 0:
          lines.extend(self.write_pop_to_address("THIS"))
        elif index == 1:
          lines.extend(self.write_pop_to_address("THAT"))
      elif segment == "temp":
        lines.extend(self.write_pop_to_address(f"R{5+index}"))
        
    # Write all the lines we've created to the output file
    for line in lines:
      print(line)
      if self.output_stream != None:
        self.output_stream.write(line + "\n")

  def write_label(self, label: str) -> None:
    """
    Writes assembly code that affects the label command.
    Let "foo" be a function within the file Xxx.vm. The handling of
    each "label bar" command within "foo" generates and injects the symbol
    "Xxx.foo$bar" into the assembly code stream.
    When translating "goto bar" and "if-goto bar" commands within "foo",
    the label "Xxx.foo$bar" must be used instead of "bar".

      Args:
        label (str): the label to write.
    """
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    pass

  def write_goto(self, label: str) -> None:
    """
    Writes assembly code that affects the goto command.

      Args:
        label (str): the label to go to.
    """
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    pass

  def write_if(self, label: str) -> None:
    """
    Writes assembly code that affects the if-goto command.

      Args:
        label (str): the label to go to.
    """
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    pass

  def write_function(self, function_name: str, n_vars: int) -> None:
    """
    Writes assembly code that affects the function command.
    The handling of each "function foo" command within the file Xxx.vm
    generates and injects a symbol "Xxx.foo" into the assembly code stream,
    that labels the entry-point to the function's code.
    In the subsequent assembly process, the assembler translates this
    symbol into the physical address where the function code starts.

      Args:
        function_name (str): the name of the function.
        n_vars (int): the number of local variables of the function.
    """
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    pass

  def write_call(self, function_name: str, n_args: int) -> None:
    """
    Writes assembly code that affects the call command.
    Let "foo" be a function within the file Xxx.vm.
    The handling of each "call" command within foo's code generates and
    injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
    "i" is a running integer (one such symbol is generated for each "call"
    command within "foo").
    This symbol is used to mark the return address within the caller's
    code. In the subsequent assembly process, the assembler translates this
    symbol into the physical memory address of the command immediately
    following the "call" command.

      Args:
        function_name (str): the name of the function to call.
        n_args (int): the number of arguments of the function.
    """
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    pass

  def write_return(self) -> None:
    """
    Writes assembly code that affects the return command.
    """
    # This is irrelevant for project 7,
    # you will implement this in project 8!
    pass


  def get_common_command(self, command: CommandType) -> list[str]:
    """
    Returns a list of lines that are common to all commands.
    """

    if command == CommonCommand.SAVE_LAST_ITEM_TO_D:
      return [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "D=M",   # Saving the last item in the stack
      ]

    elif command == CommonCommand.SAVE_2ND_TO_LAST_ITEM_TO_D:
      return [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "A=A-1", # Going to the item before the last item in the stack
        "D=M",   # Saving the 2nd to last item in the stack
      ]

    elif command == CommonCommand.GO_TO_LAST_ITEM:
      return [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
      ]

    elif command == CommonCommand.GO_TO_2ND_TO_LAST_ITEM:
      return [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "A=A-1", # Going to the item before the last item in the stack
      ]

    elif command == CommonCommand.REDUCE_SP_BY_1:
      return [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "M=M-1", # Decreasing the stack pointer by 1
      ]
    
    elif command == CommonCommand.INCREASE_SP_BY_1:
      return [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "M=M+1", # Increasing the stack pointer by 1
      ]


  # ===== READ/WRITE UTILS ===== #
  def write_push_from_segment(self, index: int, pointer: str) -> list[str]:
    """
    Writes assembly code that affects the push command, where the
    segment is "{pointer}".

      Args:
        index (int): the index in the memory segment.
        pointer (str): the pointer to the memory segment to use.
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

    lines.extend(self.get_common_command(CommonCommand.INCREASE_SP_BY_1))

    return lines

  def write_push_from_segment_direct(self, pointer: str) -> list[str]:
    """
    Writes assembly code that affects the push command, where the
    segment is "{pointer}".

      Args:
        pointer (str): the pointer to the memory segment to use.
    """

    lines = []
    lines.append(f"@{pointer}")
    lines.append("D=M")

    lines.append("@SP")
    lines.append("A=M")
    lines.append("M=D")

    lines.extend(self.get_common_command(CommonCommand.INCREASE_SP_BY_1))

    return lines

  def write_push_from_constant(self, constant: int) -> list[str]:
    """
    Writes assembly code that affects the push command, where the
    segment is "{pointer}".

      Args:
        pointer (str): the pointer to the memory segment to use.
    """

    lines = []
    lines.append(f"@{constant}")
    lines.append("D=A")

    lines.append("@SP")
    lines.append("A=M")
    lines.append("M=D")

    lines.extend(self.get_common_command(CommonCommand.INCREASE_SP_BY_1))

    return lines

  def write_push_from_address(self, address: str) -> list[str]:
    """
    Writes assembly code that affects the push command, where the
    segment is "{pointer}".

      Args:
        index (int): the index in the memory segment.
        pointer (str): the pointer to the memory segment to use.
    """

    lines = []
    lines.append(f"@{address}")
    lines.append("D=M")

    lines.append("@SP")
    lines.append("A=M")
    lines.append("M=D")

    lines.extend(self.get_common_command(CommonCommand.INCREASE_SP_BY_1))

    return lines

  def write_pop_to_segment(self, index: int, segment: str) -> list[str]:
    """
    Writes assembly code that affects the pop command, where the
    segment is "{pointer}".

      Args:
        index (int): the index in the memory segment.
        pointer (str): the pointer to the memory segment to use.
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
    lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))
    
    lines.append("@R13")
    lines.append("A=M")
    lines.append("M=D")

    lines.extend(self.get_common_command(CommonCommand.REDUCE_SP_BY_1))

    return lines

  def write_pop_to_segment_direct(self, pointer: str) -> list[str]:
    """
    Writes assembly code that affects the pop command, where the
    segment is "{pointer}".

      Args:
        pointer (str): the pointer to the memory segment to use.
    """

    lines = []

    # Popping item from SP and saving it in the address saved in R13
    lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))
    
    lines.append(f"@{pointer}")
    lines.append("M=D")

    lines.extend(self.get_common_command(CommonCommand.REDUCE_SP_BY_1))

    return lines

  def write_pop_to_address(self, address: str) -> list[str]:
    """
    Writes assembly code that affects the pop command, through an address".

      Args:
        address (int): the address to use
    """

    lines = []

    # Popping item from SP and saving it in the address saved in R13
    lines.extend(self.get_common_command(CommonCommand.SAVE_LAST_ITEM_TO_D))
    
    lines.append(f"@{address}")
    lines.append("M=D")

    lines.extend(self.get_common_command(CommonCommand.REDUCE_SP_BY_1))

    return lines
