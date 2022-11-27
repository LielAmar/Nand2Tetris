"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

from JackTokenizer import *
from Constants import *

class CompilationEngine:
    """
    Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, tokenizer: JackTokenizer, output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """

        self.tokenizer: JackTokenizer = tokenizer
        self.output = output_stream

        self.recursion_depth = 0

        # We are promised that the jack files given are valid.
        # Therefore, the first token is always the keyword 'class'.
        # We'll then execute our compilation recursively from compile_class()
        # and on
        self.compile_class()

    def __write_line(self, line):
        self.output.write((TAB * self.recursion_depth) + line + "\n")

    def __write_open_tag(self, tag):
        self.output.write((TAB * self.recursion_depth) + f"<{tag}>\n")
        
        self.recursion_depth += 1

    def __write_close_tag(self, tag):
        self.recursion_depth -= 1

        self.output.write((TAB * self.recursion_depth) + f"</{tag}>\n")


    def compile_class(self) -> None:
        """Compiles a complete class."""

        self.__write_open_tag("class")

        # Writing the first 3 tags. For example: 'class Main {'
        for _ in range(3):
            self.__write_line(self.tokenizer.token_tag())
            self.tokenizer.advance()
        
        # Writing the all classVarDec tags
        while self.tokenizer.keyword() == "static" or self.tokenizer.keyword() == "field":
            self.compile_class_var_dec()
            
        # Writing the all subroutine tags
        while self.tokenizer.keyword() == "constructor" or \
                self.tokenizer.keyword() == "function" or \
                self.tokenizer.keyword() == "method":
            self.compile_subroutine()
        
        self.__write_close_tag("class")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        pass

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """

        if self.tokenizer.keyword() == "constructor":
            self.__constructor_subroutine()
        elif self.tokenizer.keyword() == "function":
            self.__function_subroutine()
        elif self.tokenizer.keyword() == "method":
            self.__method_subroutine()

    def __constructor_subroutine(self):
        pass

    def __function_subroutine(self):
        pass

    def __method_subroutine(self):
        pass

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        pass

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        pass

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        pass

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        pass

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        pass

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        pass

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        pass

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        pass

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        pass

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        pass

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        pass
