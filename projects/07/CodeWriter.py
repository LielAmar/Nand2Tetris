"""
This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing

class CodeWriter:
  """
  Translates VM commands into Hack assembly code.
  """

  def __init__(self, output_stream: typing.TextIO) -> None:
    """Initializes the CodeWriter.

      Args:
        output_stream (typing.TextIO): output stream.
    """

    self.output_steam = output_stream
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

    # Adding the last 2 items in the stack
    if command == "add":
      lines = [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "D=M",   # Saving the last item in the stack
        "A=A-1", # Going to the item before the last item in the stack
        "M=M+D", # Setting the 2nd to last item's value to the sum of the last 2 items
        "@SP",   # Going to address 0, to get the pointer of the stack
        "M=M-1", # Decreasing the stack pointer by 1
      ]

    # Subtracting the last 2 items in the stack
    elif command == "sub":
      lines = [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "D=M",   # Saving the last item in the stack
        "A=A-1", # Going to the item before the last item in the stack
        "M=M-D", # Setting the 2nd to last item's value to the sub of the last 2 items
        "@SP",   # Going to address 0, to get the pointer of the stack
        "M=M-1", # Decreasing the stack pointer by 1
      ]
    
    # Negating the last item in the stack
    elif command == "neg":
      lines = [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "M=-M",  # Setting the last item's value to the neg of the last item
      ]

    # Checking if one of the last 2 items in the stack is true
    elif command == "or":
      lines = [
        # Checking if the last item is -1 (true)
        "@SP",     # Going to address 0, to get the pointer of the stack
        "A=M-1",   # Going to the address of the last item in the stack
        "D=M+1",   # Checking if the last item is -1 (true)

          # If it is true, we jump to TRUE
        f"@TRUE{self.command_id}",   # Going to address TRUE
        "D;JEQ",   # If the last item was -1 (true), jump to TRUE

        # Checking if the item before the last item is true
        "@SP",     # Going to address 0, to get the pointer of the stack
        "A=M-1",   # Going to the address of the last item in the stack
        "A=A-1",   # Going to the item before the last item in the stack
        "D=M+1",   # Checking if the 2nd to last item is -1 (true)

          # If it is true, we jump to TRUE
        f"@TRUE{self.command_id}",   # Going to address TRUE
        "D;JEQ",   # If the last item was -1 (true), jump to TRUE 

        # If both items are false, we set the result to false and jump to end
        "@SP",     # Going to address 0, to get the pointer of the stack
        "A=M-1",   # Going to the address of the last item in the stack
        "A=A-1",   # Going to the item before the last item in the stack
        "M=0",     # Setting the 2nd to last item's value to 0
        f"@END{self.command_id}",   # Going to address END
        "0;JMP",   # Jump to END

        # If at least one is true, we set the result to true
        f"(TRUE{self.command_id})",   # Label for TRUE
        "@SP",     # Going to address 0, to get the pointer of the stack
        "A=M-1",   # Going to the address of the last item in the stack
        "A=A-1",   # Going to the item before the last item in the stack
        "M=-1",    # Setting the 2nd to last item's value to -1

        # Reducing SP by 1 and ending
        f"(END{self.command_id})",   # Label for END
        "@SP",     # Going to address 0, to get the pointer of the stack
        "M=M-1",   # Decreasing the stack pointer by 1
      ]

    # Chaning the last item in the stack to 'not' item
    elif command == "not":
      lines = [
        "@SP",     # Going to address 0, to get the pointer of the stack
        "A=M-1",   # Going to the address of the last item in the stack
        "M=!M",    # Setting the last item's value to not last item
      ]

    # Shifting the last item in the stack left
    elif command == "shiftleft":
      lines = [
        "@SP",     # Going to address 0, to get the pointer of the stack
        "A=M-1",   # Going to the address of the last item in the stack
        "M=M<<",    # Setting the last item's value to the left shift of the last item
      ]

    # Shifting the last item in the stack right
    elif command == "shiftleft":
      lines = [
        "@SP",     # Going to address 0, to get the pointer of the stack
        "A=M-1",   # Going to the address of the last item in the stack
        "M=M>>",    # Setting the last item's value to the left shift of the last item
      ]

    # Checking if the last 2 items in the stack are equal
    elif command == "eq":
      lines = [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "D=M",   # Saving the last item in the stack
        "A=A-1", # Going to the item before the last item in the stack
        "D=M-D", # Setting the 2nd to last item's value to the sub of the last 2 items
        f"@TRUE{self.command_id}", # Going to address TRUE
        "D;JEQ", # If the items are identical (D=0), jump to TRUE
        
        # Items are not equal
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "A=A-1", # Going to the item before the last item in the stack
        "M=0",   # Setting the 2nd to last item's value to 0
        f"@END{self.command_id}",  # Going to address END
        "0;JMP", # Jump to END

        # Items are equal
        f"(TRUE{self.command_id})", # Label for TRUE
        "@SP",    # Going to address 0, to get the pointer of the stack
        "A=M-1",  # Going to the address of the last item in the stack
        "A=A-1",  # Going to the item before the last item in the stack
        "M=-1",   # Setting the 2nd to last item's value to -1

        # Ending code by decreasing the stack pointer by 1
        f"(END{self.command_id})",  # Label for END
        "@SP",    # Going to address 0, to get the pointer of the stack
        "M=M-1",  # Decreasing the stack pointer by 1
      ]

    # Checking if the 2nd to last item is greater than the last item
    elif command == "gt":
      lines = [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "D=M",   # Saving the last item in the stack
        "A=A-1", # Going to the item before the last item in the stack
        "D=M-D", # Setting the 2nd to last item's value to the sub of the last 2 items

        f"@TRUE{self.command_id}", # Going to address TRUE
        "D;JGT", # If the 2nd to last item is smaller than the last item (D<0), jump to TRUE

        # Item is not greater
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "A=A-1", # Going to the item before the last item in the stack
        "M=0",   # Setting the 2nd to last item's value to 0 (false)
        f"@END{self.command_id}",  # Going to address END
        "0;JMP", # Jump to END

        # Item is greater
        f"(TRUE{self.command_id})", # Label for TRUE
        "@SP",    # Going to address 0, to get the pointer of the stack
        "A=M-1",  # Going to the address of the last item in the stack
        "A=A-1",  # Going to the item before the last item in the stack
        "M=-1",   # Setting the 2nd to last item's value to -1 (true)

        # Ending code by decreasing the stack pointer by 1
        f"(END{self.command_id})",  # Label for END
        "@SP",    # Going to address 0, to get the pointer of the stack
        "M=M-1",  # Decreasing the stack pointer by 1
      ]

    # Checking if the 2nd to last item is smaller than the last item
    elif command == "lt":
      lines = [
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "D=M",   # Saving the last item in the stack
        "A=A-1", # Going to the item before the last item in the stack
        "D=M-D", # Setting the 2nd to last item's value to the sub of the last 2 items

        f"@TRUE{self.command_id}", # Going to address TRUE
        "D;JLT", # If the 2nd to last item is smaller than the last item (D<0), jump to TRUE

        # Item is not smaller
        "@SP",   # Going to address 0, to get the pointer of the stack
        "A=M-1", # Going to the address of the last item in the stack
        "A=A-1", # Going to the item before the last item in the stack
        "M=0",   # Setting the 2nd to last item's value to 0 (false)
        f"@END{self.command_id}",  # Going to address END
        "0;JMP", # Jump to END

        # Item is smaller
        f"(TRUE{self.command_id})", # Label for TRUE
        "@SP",    # Going to address 0, to get the pointer of the stack
        "A=M-1",  # Going to the address of the last item in the stack
        "A=A-1",  # Going to the item before the last item in the stack
        "M=-1",   # Setting the 2nd to last item's value to -1 (true)

        # Ending code by decreasing the stack pointer by 1
        f"(END{self.command_id})",  # Label for END
        "@SP",    # Going to address 0, to get the pointer of the stack
        "M=M-1",  # Decreasing the stack pointer by 1
      ]

    # Write all the lines we've created to the output file
    for line in lines:
      self.output_stream.write(line + "\n")

  def write_push_pop(self, command: str, segment: str, index: int) -> None:
    """
    Writes assembly code that is the translation of the given
    command, where command is either C_PUSH or C_POP.

      Args:
        command (str): "C_PUSH" or "C_POP".
        segment (str): the memory segment to operate on.
        index (int): the index in the memory segment.
    """
    # Your code goes here!
    # Note: each reference to static i appearing in the file Xxx.vm should
    # be translated to the assembly symbol "Xxx.i". In the subsequent
    # assembly process, the Hack assembler will allocate these symbolic
    # variables to the RAM, starting at address 16.
    pass

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
