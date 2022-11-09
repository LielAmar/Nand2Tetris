"""
This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import os
import sys
import typing

from Parser import Parser
from CodeWriter import CodeWriter
from Constants import *

def translate_file(input_file: typing.TextIO, output_file: typing.TextIO) -> None:
  """
  Translates a single file.

    Args:
      input_file (typing.TextIO): the file to translate.
      output_file (typing.TextIO): writes all output to this file.
  """

  parser = Parser(input_file)
  code_writer = CodeWriter(output_file)

  # Setting the file name & debug flag
  code_writer.set_file_name(os.path.splitext(os.path.basename(input_file.name))[0])

  # Parsing the file
  while parser.has_more_commands():
    parser.advance()
    command_type = parser.command_type()
  
    if command_type == "C_ARITHMETIC":
      code_writer.write_arithmetic(parser.arg1())

    elif command_type in ["C_PUSH", "C_POP"]:
      code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())

  """
  We propose implementing the basic VM translator in two stages. This will
  allow you to unit-test your implementation incrementally, using the test
  programs we supplied you. In what follows, when we say "your VM
  translator should implement some VM command" we mean "your VM translator
  should translate the given VM command into a sequence of assembly
  commands that accomplish the same task".
  
  Stage I: Handling stack arithmetic commands: 
  The first version of your basic VM translator should implement the nine
  arithmetic / logical commands of the VM language as well as the VM
  command push constant x.
  The latter command is the generic push command for which the first
  argument is constant and the second argument is some non-negative integer
  x. This command comes handy at this early stage, since it helps provide
  values for testing the implementation of the arithmetic / logical VM
  commands. For example, in order to test how your VM translator handles
  the VM add command, we can test how it handles the VM code:
  push constant 3
  push constant 5 
  add
  The other arithmetic and logical commands are tested similarly:
  add, sub, neg, and, or, not, shiftleft, shiftright, eq, gt, lt
  This stage can be tested using SimpleAdd, which is relatively simple, and
  StackTest, which is slightly more complex.

  Stage II: Handling memory access commands: 
  The next version of your basic VM translator should include a full
  implementation of the VM language's push and pop commands, handling the
  eight memory segments described in chapter 7. We suggest breaking this
  stage into the following sub-stages:
  - You have already handled the constant segment;
  - Next, handle the segments local, argument, this, and that. This can be
  tested using BasicTest.
  - Next, handle the pointer and temp segments, in particular allowing
  modification of the bases of the this and that segments. This can be
  tested using PointerTest.
  - Finally, handle the static segment. This can be tested using StaticTest.

  Testing:
  We supply VM programs designed to unit-test the staged implementation
  proposed above. For each program Xxx we supply four files. The Xxx.vm
  file contains the program's VM code. The XxxVME.tst script allows running
  the program on the supplied VM emulator, to experiment with the program’s
  intended operation. After translating the program using your VM
  translator, the supplied Xxx.tst script and Xxx.cmp compare file allow
  testing the translated assembly code on the supplied CPU emulator.
  For each one of the five test programs supplied above, follow these steps:
  - To get acquainted with the intended behavior of the supplied test
  program Xxx.vm, run it on the supplied VM emulator using the supplied
  XxxVME.tst script.
  - Use your VM translator to translate the supplied Xxx.vm file. The
  result should be a new text file containing Hack assembly code, named
  Xxx.asm.
  - Inspect the Xxx.asm program generated by your VM translator. If there
  are visible syntax (or any other) errors, debug and fix your VM translator.
  - To check if the generated code performs properly, use the supplied
  Xxx.tst and Xxx.cmp files to run the Xxx.asm program on the supplied CPU
  emulator. If there are any problems, debug and fix your VM translator.
  
  Implementation Order: 
  The supplied test programs were carefully planned to test the incremental
  features introduced by each development stage of your basic VM
  translator. Therefore, it's important to implement your translator in the
  proposed order, and to test it using the appropriate test programs at
  each stage. Implementing a later stage before an early one may cause the
  test programs to fail.

  Tools:
  Before setting out to develop your VM translator, we recommend getting
  acquainted with the virtual machine architecture model and language. As
  mentioned above, this can be done by running, and experimenting with, the
  supplied .vm test programs using the supplied VM emulator.
  
  The VM emulator: 
  This program, located in your nand2tetris/tools directory, is designed to
  execute VM programs in a direct and visual way, without having to first
  translate them into machine language. For example, you can use the
  supplied VM emulator to see - literally speaking - how push and pop
  commands effect the stack. And, you can use the simulator to execute any
  one of the supplied .vm test programs.
  For more information, see the VM emulator tutorial in the lectures and in
  the submission page.
  """
  pass


if "__main__" == __name__:
  # Parses the input path and calls translate_file on each input file.
  # This opens both the input and the output files!
  # Both are closed automatically when the code finishes running.
  # If the output file does not exist, it is created automatically in the
  # correct path, using the correct filename.
  if not len(sys.argv) == 2:
    sys.exit("Invalid usage, please use: VMtranslator <input path>")
  
  argument_path = os.path.abspath(sys.argv[1])
  
  if os.path.isdir(argument_path):
    files_to_translate = [
      os.path.join(argument_path, filename) for filename in os.listdir(argument_path)
    ]
    
    output_path = os.path.join(argument_path, os.path.basename(argument_path))
  else:
    files_to_translate = [argument_path]
    output_path, extension = os.path.splitext(argument_path)
  
  output_path += ".asm"
    
  with open(output_path, 'w') as output_file:
    for input_path in files_to_translate:
      filename, extension = os.path.splitext(input_path)
        
      if extension.lower() != ".vm":
        continue
        
      with open(input_path, 'r') as input_file:
        translate_file(input_file, output_file)
