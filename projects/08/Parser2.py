"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser2:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """
    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        self.input_lines = input_file.read().splitlines()
        self.code_line = 0
        self.current_line = 0
        self.current_com = ""
        if self.has_more_commands():
            self.current_com = self.input_lines[0]
            if self.current_com == "" or self.current_com[0] == '/':
                self.advance()
                self.code_line = 0
            # self.current_com = self.current_com.replace(" ", "")
            tmp = self.current_com
            tmp = tmp.split("//")
            self.current_com = tmp[0]


    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        if self.current_line >= len(self.input_lines):
            return False
        return True

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        self.current_line += 1
        if not self.has_more_commands():
            return
        self.current_com = self.input_lines[self.current_line]
        while self.current_com == "" or self.current_com[0] == '/':
            self.current_line += 1
            if not self.has_more_commands():
                return
            self.current_com = self.input_lines[self.current_line]
        if self.current_com[0] != '(':
            self.code_line += 1
        # self.current_com = self.current_com.replace(" ","")
        tmp = self.current_com
        tmp = tmp.split("//")
        self.current_com = tmp[0]
    # def __init__(self, input_file: typing.TextIO) -> None:
    #     """Gets ready to parse the input file.
    #
    #     Args:
    #         input_file (typing.TextIO): input file.
    #     """
    #     # Your code goes here!
    #     # A good place to start is:
    #     # input_lines = input_file.read().splitlines()
    #     pass
    #
    # def has_more_commands(self) -> bool:
    #     """Are there more commands in the input?
    #
    #     Returns:
    #         bool: True if there are more commands, False otherwise.
    #     """
    #     # Your code goes here!
    #     pass
    #
    # def advance(self) -> None:
    #     """Reads the next command from the input and makes it the current
    #     command. Should be called only if has_more_commands() is true. Initially
    #     there is no current command.
    #     """
    #     # Your code goes here!
    #     pass

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        arith = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]
        if self.current_com[0:3] in arith or self.current_com[0:2] in arith:
            return "C_ARITHMETIC"
        elif "pop" in self.current_com[0:3]:
            return "C_POP"
        elif "push" in self.current_com[0:4]:
            return "C_PUSH"
        elif "label" in self.current_com[0:5]:
            return "C_LABEL"
        elif "if" in self.current_com[0:2]:
            return "C_IF"
        elif "goto" == self.current_com[0:4]:
            return "C_GOTO"
        elif "function" in self.current_com[0:8]:
            return "C_FUNCTION"
        elif "return" in self.current_com[0:6]:
            return "C_RETURN"
        elif "call" in self.current_com[0:4]:
            return "C_CALL"

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        if self.command_type() == "C_ARITHMETIC":
            tmp = self.current_com.split()
            return tmp[0]
        tmp = self.current_com.split()
        return tmp[1]


    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        tmp = self.current_com.split()
        return int(tmp[2])
