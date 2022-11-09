"""This file is part of nand2tetris, as taught in The Hebrew University,
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

def translate_file(input_file: typing.TextIO, output_file: typing.TextIO, 
    bootstrap: bool) -> None:
  """Translates a single file.

  Args:
    input_file (typing.TextIO): the file to translate.
    output_file (typing.TextIO): writes all output to this file.
    bootstrap (bool): if this is True, the current file is the 
      first file we are translating.
  """

  parser = Parser(input_file)
  code_writer = CodeWriter(output_file)

  # Setting the file name & debug flag
  code_writer.set_file_name(os.path.splitext(os.path.basename(input_file.name))[0])

  # Writing the bootstrap code if we've received bootstrap = True
  if bootstrap:
    code_writer.write_init()

  # Parsing the file
  while parser.has_more_commands():
    parser.advance()
    command_type = parser.command_type()
  
    if command_type == "C_ARITHMETIC":
      code_writer.write_arithmetic(parser.arg1())

    elif command_type in ["C_PUSH", "C_POP"]:
      code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())

    elif command_type == "C_LABEL":
      code_writer.write_label(parser.arg1())
      
    elif command_type == "C_GOTO":
      code_writer.write_goto(parser.arg1())
    elif command_type == "C_IF":
      code_writer.write_if(parser.arg1())

    elif command_type == "C_FUNCTION":
      code_writer.write_function(parser.arg1(), parser.arg2())
    elif command_type == "C_CALL":
      code_writer.write_call(parser.arg1(), parser.arg2())
    elif command_type == "C_RETURN":
      code_writer.write_return()

  """
  In this project, we will extend the basic translator developed in project
  7 to a full-scale VM-to-Hack translator which will conform to the VM
  Specification, Part II (book section 8.2) and to the Standard VM-on-Hack
  Mapping, Part II (book section 8.3.1). To do this, you can use your
  submission for project 7 as a template. If you implemented everything
  correctly, the parser from project 7 can be used as-is, without any
  modifications. But, you will need to add the following functions to your
  CodeWriter: write_label, write_goto, write_if, write_function,
  write_call, write_return.
  
  We recommend completing the implementation of the VM translator in two
  stages. 
    1. First, implement and test the translation of the VM language's
    branching commands. This stage can be tested using the basic test
    BasicLoop and the slightly more advanced FibonacciSeries.
  2. Next, implement and test the translation of the function call and
  return commands. "SimpleFunction" is a basic test for this step, while
  "NestedCall" is slightly more advanced, and also contains in-depth
  instructions on how to run the test (in NestedCall.html) and step-by-step
  visualizations of the stack's state in NestedCallStack.html.
  3. Finally, add the bootstrap code, which initializes the SP to 256, and
  calls the function "Sys.init". After this step, some previous tests will
  stop working, specifically BasicLoop, FibonacciSeries and SimpleFunction!
  In order to test your implementation, you can use the FibonacciElement
  test, which includes a relatively simple recursive function, and the
  StaticsTest test, which includes multiple classes that utilize static
  variables.
  This will allow you to unit-test your implementation incrementally, using
  the test programs we supplied you with.
  
  For each one of the five test programs, follow these steps:
  - To get acquainted with the intended behavior of the supplied test
  program Xxx.vm, run it on the supplied VM emulator using the supplied
  XxxVME.tst script (if the program consists of one ore more files residing
  in a directory, load the *entire* directory into the VM emulator and
  proceed to execute the code).)
  - Use your VM translator to translate the supplied Xxx.vm file, or Xxx
  directory, as needed. The result should be a new text file containing
  Hack assembly code. The name of this file should be Xxx.asm.
  - Inspect the translated Xxx.asm program. If there are visible syntax (or
  any other) errors, debug and fix your VM translator.
  - To check if the translated code performs properly, use the supplied
  Xxx.tst and Xxx.cmp files to run the translated Xxx.asm program on the
  supplied CPU emulator. If there are any problems, debug and fix your VM
  translator.

  Implementation order:
  The supplied test programs were carefully planned to test the incremental
  features introduced by each stage in your VM implementation. Therefore,
  it's important to implement your VM translator in the proposed order, and
  to test it using the supplied test programs at each stage. Implementing a
  later stage before an early one may cause the test programs to fail.

  Initialization:
  In order for the translated VM code to execute on the host computer
  platform, the translated code stream (written in the machine language of
  the host platform) must include some bootstrap code that maps the stack
  on the host RAM and starts executing the code proper. The first three
  test programs in this project assume that the bootstrap code was not yet
  implemented, and include test scripts that effect the necessary
  initializations (as was done in project 7). The last two test programs
  assume that the bootstrap code is generated by the VM translator. In
  other words, the assembly code that the final version of your VM
  translator generates must start with some code that sets the stack
  pointer and calls the Sys.init function. Sys.init will then call the
  Main.main function, and the program will start running (similar to how
  Java's JVM always looks for, and starts executing, a method named main).
  
  Use your VM translator to translate the VM programs supplied as tests,
  yielding corresponding programs written in the Hack assembly language.
  When executed on the supplied CPU emulator, the translated code generated
  by your VM translator should deliver the results mandated by the test
  scripts and compare files supplied.

  Tools:
  Before setting out to extend your basic VM translator, we recommend
  playing with the supplied .vm test programs. This will allow you to
  experiment with branching and function call-and-return commands, using
  the supplied VM emulator.
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
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    bootstrap = True
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file, bootstrap)
            bootstrap = False

# """This file is part of nand2tetris, as taught in The Hebrew University,
# and was written by Aviv Yaish according to the specifications given in  
# https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
# and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
# Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
# """
# import os
# import sys
# import typing
# from Parser import Parser
# from CodeWriter import CodeWriter
# from Constants import *


# def translate_file(
#         input_file: typing.TextIO, output_file: typing.TextIO,
#         bootstrap: bool) -> None:
#     """Translates a single file.

#     Args:
#         input_file (typing.TextIO): the file to translate.
#         output_file (typing.TextIO): writes all output to this file.
#     """
#     # Your code goes here!
#     """
#     We propose implementing the basic VM translator in two stages. This will
#     allow you to unit-test your implementation incrementally, using the test
#     programs we supplied you. In what follows, when we say "your VM
#     translator should implement some VM command" we mean "your VM translator
#     should translate the given VM command into a sequence of assembly
#     commands that accomplish the same task".
    
#     Stage I: Handling stack arithmetic commands: 
#     The first version of your basic VM translator should implement the nine
#     arithmetic / logical commands of the VM language as well as the VM
#     command push constant x.
#     The latter command is the generic push command for which the first
#     argument is constant and the second argument is some non-negative integer
#     x. This command comes handy at this early stage, since it helps provide
#     values for testing the implementation of the arithmetic / logical VM
#     commands. For example, in order to test how your VM translator handles
#     the VM add command, we can test how it handles the VM code:
#     push constant 3
#     push constant 5 
#     add
#     The other arithmetic and logical commands are tested similarly:
#     add, sub, neg, and, or, not, shiftleft, shiftright, eq, gt, lt
#     This stage can be tested using SimpleAdd, which is relatively simple, and
#     StackTest, which is slightly more complex.

#     Stage II: Handling memory access commands: 
#     The next version of your basic VM translator should include a full
#     implementation of the VM language's push and pop commands, handling the
#     eight memory segments described in chapter 7. We suggest breaking this
#     stage into the following sub-stages:
#     - You have already handled the constant segment;
#     - Next, handle the segments local, argument, this, and that. This can be
#     tested using BasicTest.
#     - Next, handle the pointer and temp segments, in particular allowing
#     modification of the bases of the this and that segments. This can be
#     tested using PointerTest.
#     - Finally, handle the static segment. This can be tested using StaticTest.

#     Testing:
#     We supply VM programs designed to unit-test the staged implementation
#     proposed above. For each program Xxx we supply four files. The Xxx.vm
#     file contains the program's VM code. The XxxVME.tst script allows running
#     the program on the supplied VM emulator, to experiment with the program’s
#     intended operation. After translating the program using your VM
#     translator, the supplied Xxx.tst script and Xxx.cmp compare file allow
#     testing the translated assembly code on the supplied CPU emulator.
#     For each one of the five test programs supplied above, follow these steps:
#     - To get acquainted with the intended behavior of the supplied test
#     program Xxx.vm, run it on the supplied VM emulator using the supplied
#     XxxVME.tst script.
#     - Use your VM translator to translate the supplied Xxx.vm file. The
#     result should be a new text file containing Hack assembly code, named
#     Xxx.asm.
#     - Inspect the Xxx.asm program generated by your VM translator. If there
#     are visible syntax (or any other) errors, debug and fix your VM translator.
#     - To check if the generated code performs properly, use the supplied
#     Xxx.tst and Xxx.cmp files to run the Xxx.asm program on the supplied CPU
#     emulator. If there are any problems, debug and fix your VM translator.
    
#     Implementation Order: 
#     The supplied test programs were carefully planned to test the incremental
#     features introduced by each development stage of your basic VM
#     translator. Therefore, it's important to implement your translator in the
#     proposed order, and to test it using the appropriate test programs at
#     each stage. Implementing a later stage before an early one may cause the
#     test programs to fail.

#     Tools:
#     Before setting out to develop your VM translator, we recommend getting
#     acquainted with the virtual machine architecture model and language. As
#     mentioned above, this can be done by running, and experimenting with, the
#     supplied .vm test programs using the supplied VM emulator.
    
#     The VM emulator: 
#     This program, located in your nand2tetris/tools directory, is designed to
#     execute VM programs in a direct and visual way, without having to first
#     translate them into machine language. For example, you can use the
#     supplied VM emulator to see - literally speaking - how push and pop
#     commands effect the stack. And, you can use the simulator to execute any
#     one of the supplied .vm test programs.
#     For more information, see the VM emulator tutorial in the lectures and in
#     the submission page.
#     """
#     vm_code = Parser(input_file)
#     writer = CodeWriter(output_file)
#     input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
#     writer.set_file_name(input_filename)
#     writer.write_init()
#     while vm_code.has_more_commands():
#         c_type = vm_code.command_type()
#         if c_type != "C_RETURN:
#             arg1 = vm_code.arg1()
#             if c_type == "C_ARITHMETIC:
#                 writer.write_arithmetic(arg1)
#             elif c_type == "C_POP or c_type == "C_PUSH:
#                 arg2 = vm_code.arg2()
#                 writer.write_push_pop(c_type, arg1, arg2)
#             elif c_type == "C_GOTO:
#                 writer.write_goto(arg1)
#             elif c_type == "C_IF:
#                 writer.write_if(arg1)
#             elif c_type == "C_LABEL:
#                 writer.write_label(arg1)
#             elif c_type == "C_FUNCTION:
#                 arg2 = vm_code.arg2()
#                 writer.write_function(arg1,arg2)
#             elif c_type == "C_CALL:
#                 arg2 = vm_code.arg2()
#                 writer.write_call(arg1, arg2)
#         else:
#             writer.write_return()
#         vm_code.advance()


# if "__main__" == __name__:
#     # Parses the input path and calls translate_file on each input file.
#     # This opens both the input and the output files!
#     # Both are closed automatically when the code finishes running.
#     # If the output file does not exist, it is created automatically in the
#     # correct path, using the correct filename.
#     if not len(sys.argv) == 2:
#         sys.exit("Invalid usage, please use: VMtranslator <input path>")
#     argument_path = os.path.abspath(sys.argv[1])
#     if os.path.isdir(argument_path):
#         files_to_translate = [
#             os.path.join(argument_path, filename)
#             for filename in os.listdir(argument_path)]
#         output_path = os.path.join(argument_path, os.path.basename(
#             argument_path))
#     else:
#         files_to_translate = [argument_path]
#         output_path, extension = os.path.splitext(argument_path)
#     output_path += ".asm"
#     bootstrap = True
#     with open(output_path, 'w') as output_file:
#         for input_path in files_to_translate:
#             filename, extension = os.path.splitext(input_path)
#             if extension.lower() != ".vm":
#                 continue
#             with open(input_path, 'r') as input_file:
#                 translate_file(input_file, output_file, bootstrap)
#             bootstrap = False